# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import typing

from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.api_client import APIClient as MetaAPIClient
from gridmarkets_blender_addon.meta_plugin.api_schema import APISchema
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.gridmarkets.xml_api_schema_parser import XMLAPISchemaParser

from gridmarkets_blender_addon.meta_plugin.errors.invalid_email_error import InvalidEmailError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_access_key_error import InvalidAccessKeyError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_user_error import InvalidUserError
from gridmarkets_blender_addon.meta_plugin.errors.api_error import APIError
from gridmarkets_blender_addon.meta_plugin.errors.not_signed_in_error import NotSignedInError
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

from gridmarkets import EnvoyClient, Project as GMProject
from gridmarkets.errors import AuthenticationError, APIError as _APIError


class GridMarketsAPIClient(MetaAPIClient):

    def __init__(self):
        MetaAPIClient.__init__(self)
        self._envoy_client: typing.Optional[EnvoyClient] = None
        self._api_schema = XMLAPISchemaParser.parse()

        # used for caching projects
        self._cache_projects = None
        self._product_resolver = None

    def sign_in(self, user: User, skip_validation: bool = False) -> None:

        try:
            MetaAPIClient.sign_in(self, user)
        except InvalidEmailError as e:
            raise e
        except InvalidAccessKeyError as e:
            raise e
        except InvalidUserError as e:
            raise e

        self._envoy_client = EnvoyClient(email=user.get_auth_email(), access_key=user.get_auth_key())

    def sign_out(self) -> None:
        MetaAPIClient.sign_out(self)

    def is_user_signed_in(self) -> bool:
        return MetaAPIClient.is_user_signed_in(self)

    def connected(self) -> bool:
        raise NotImplementedError

    def get_signed_in_user(self) -> typing.Optional[User]:
        return MetaAPIClient.get_signed_in_user(self)

    def get_api_schema(self) -> APISchema:
        return self._api_schema

    @staticmethod
    def validate_credentials(auth_email: str, auth_access_key: str) -> bool:

        # check an email address has been entered
        has_email = isinstance(auth_email, str) and len(auth_email) > 0

        # check a auth key has been entered
        has_key = isinstance(auth_access_key, str) and len(auth_access_key) > 0

        if has_email and has_key:
            try:
                client = EnvoyClient(email=auth_email, access_key=auth_access_key)
                client.validate_auth()
            except AuthenticationError as e:
                raise InvalidUserError(message=e.user_message)
            except _APIError as e:
                e_msg = str(e.user_message)

                # pretty error message for common errors
                if e_msg.startswith("Unexpected error communicating with Envoy.Please start Envoy"):
                    e_msg = "Unable to connect to Envoy."

                raise APIError(message=e_msg)

        elif not (has_email or has_key):
            message = "No " + api_constants.COMPANY_NAME + " email address or access key provided."
            raise InvalidUserError(message=message)
        elif not has_email:
            message = "No " + api_constants.COMPANY_NAME + " email address provided."
            raise InvalidEmailError(message=message)
        elif not has_key:
            message = "No " + api_constants.COMPANY_NAME + " access key provided."
            raise InvalidAccessKeyError(message=message)

        return True

    def upload_project(self,
                       packed_project: PackedProject,
                       delete_local_files_after_upload: bool = False) -> RemoteProject:

        if not self.is_user_signed_in():
            raise NotSignedInError("Must be signed-in to upload a project.")

        project_dir = str(packed_project.get_root_dir())
        project_name = packed_project.get_name()

        gm_project = GMProject(project_dir, project_name)
        gm_project.add_folders(project_dir)

        self._envoy_client.upload_project_files(gm_project)

        return RemoteProject.convert_packed_project(packed_project)

    def get_root_directories(self, ignore_cache: bool = False) -> typing.List[str]:
        if ignore_cache or self._cache_projects is None:
            import requests
            r = requests.get(self._envoy_client.url + '/projects')
            json = r.json()
            projects = json.get("projects", [])
            projects = list(map(lambda project: project.get('name', ''), projects))
            projects = sorted(projects, key=lambda s: s.casefold())
            self._cache_projects = projects

        return self._cache_projects

    def get_product_versions(self, product: str, ignore_cache: bool = False) -> typing.List[str]:
        if ignore_cache or self._product_resolver is None:
            # get product resolver
            resolver = self._envoy_client.get_product_resolver()

            # cache all products
            self._product_resolver = resolver.get_all_types()

        # sorted by latest version to oldest version
        return sorted(self._product_resolver.get(product, {}).get("versions", []), key=lambda s: s.casefold(),
                      reverse=True)

    def get_remote_project_files(self, project_name: str):
        import requests
        r = requests.get(self._envoy_client.url + '/project/' + project_name + '/Files')
        json = r.json()
        all_files = json.get('project_files', {}).get('all_files', [])
        return sorted(map(lambda file: file.get('Name', ''), all_files), key=lambda s: s.casefold())

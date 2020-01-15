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

import copy
import typing

from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.api_client import APIClient as MetaAPIClient
from gridmarkets_blender_addon.meta_plugin.api_schema import APISchema
from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.gridmarkets.xml_api_schema_parser import XMLAPISchemaParser
from gridmarkets_blender_addon.meta_plugin.logging_coordinator import LoggingCoordinator
from gridmarkets_blender_addon.meta_plugin.utils import get_files_in_directory

from gridmarkets_blender_addon.meta_plugin.errors.invalid_email_error import InvalidEmailError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_access_key_error import InvalidAccessKeyError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_user_error import InvalidUserError
from gridmarkets_blender_addon.meta_plugin.errors.api_error import APIError
from gridmarkets_blender_addon.meta_plugin.errors.not_signed_in_error import NotSignedInError
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

import gridmarkets
from gridmarkets.errors import AuthenticationError, APIError as _APIError


class EnvoyProject:
    def __init__(self, name: str, deleting: bool, num_files: int, total_size: int, auto_downloading: bool,
                 watched_list: typing.List[str]):
        self._name = name
        self._deleting = deleting
        self._num_files = num_files
        self._total_size = total_size
        self._auto_downloading = auto_downloading
        self._watched_list = watched_list

    def get_name(self) -> str:
        return self._name

    def is_deleting(self) -> bool:
        return self._deleting

    def get_file_count(self) -> int:
        return self._num_files

    def get_total_size(self) -> int:
        return self._total_size

    def is_auto_downloading(self) -> bool:
        return self._auto_downloading

    def get_watched_list(self) -> typing.List[str]:
        return self._watched_list


class EnvoyFile:
    def __init__(self, check_sum:str, last_modified: str, name: str, key: str, size: int, fmt_name: str):
        self._check_sum = check_sum
        self._last_modified = last_modified
        self._name = name
        self._key = key
        self._size = size
        self._fmt_name = fmt_name

    def get_check_sum(self) -> str:
        return self._check_sum

    def get_last_modified(self) -> str:
        return self._last_modified

    def get_name(self) -> str:
        return self._name

    def get_key(self) -> str:
        return self._key

    def get_size(self) -> int:
        return self._size

    def get_fmt_name(self) -> str:
        return self._fmt_name


T = typing.TypeVar('T')


class CachedValue(typing.Generic[T]):
    def __init__(self, value: T, is_cached: bool = False):
        self._initial_value = copy.copy(value)
        self._value = value
        self._is_cached = is_cached

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T):
        self._value = value
        self._is_cached = True

    def is_cached(self) -> bool:
        return self._is_cached

    def reset_and_clear_cache(self):
        self._value = copy.copy(self._initial_value)
        self._is_cached = False


class GridMarketsAPIClient(MetaAPIClient):
    http_api_endpoint = "https://api.gridmarkets.com:8003/api/render/1.0/"

    def __init__(self, logging_coordinator: LoggingCoordinator):
        MetaAPIClient.__init__(self)
        self._signed_in: bool = False
        self._envoy_client: typing.Optional[gridmarkets.EnvoyClient] = None
        self._log = logging_coordinator.get_logger("GridMarketsAPIClient")

        # used for caching projects
        self._api_schema_cache = CachedValue(None)
        self._remote_projects_cache: CachedValue = CachedValue([])
        self._project_files_dictionary_cache = {}
        self._product_resolver: CachedValue = CachedValue(None)

    def clear_all_caches(self):
        self._log.info("Clearing cached API data")
        self._remote_projects_cache.reset_and_clear_cache()
        self._project_files_dictionary_cache.clear()
        self._product_resolver.reset_and_clear_cache()

    def sign_in(self, user: User, skip_validation: bool = False) -> None:
        self._log.info("Signing in as " + user.get_auth_email())

        try:
            MetaAPIClient.sign_in(self, user, skip_validation=skip_validation)
        except InvalidEmailError as e:
            raise e
        except InvalidAccessKeyError as e:
            raise e
        except InvalidUserError as e:
            raise e

        self._envoy_client = gridmarkets.EnvoyClient(email=user.get_auth_email(), access_key=user.get_auth_key())

        # refresh caches
        self.clear_all_caches()
        self.get_root_directories(ignore_cache=True)
        self.get_api_schema(ignore_cache=True)
        self._signed_in = True

    def sign_out(self) -> None:
        if self.is_user_signed_in():
            self._log.info("Signing out user " + self.get_signed_in_user().get_auth_email())

        MetaAPIClient.sign_out(self)
        self._signed_in = False

    def is_user_signed_in(self) -> bool:
        return self._signed_in

    def connected(self) -> bool:
        raise NotImplementedError

    def get_signed_in_user(self) -> typing.Optional[User]:
        return MetaAPIClient.get_signed_in_user(self)

    def get_api_schema(self, ignore_cache=False) -> APISchema:

        if ignore_cache or not self._api_schema_cache.is_cached():
            self._api_schema_cache.set_value(XMLAPISchemaParser.parse())

        return self._api_schema_cache.get_value()

    @staticmethod
    def validate_credentials(auth_email: str, auth_access_key: str) -> bool:

        # check an email address has been entered
        has_email = isinstance(auth_email, str) and len(auth_email) > 0

        # check a auth key has been entered
        has_key = isinstance(auth_access_key, str) and len(auth_access_key) > 0

        if has_email and has_key:
            try:
                client = gridmarkets.EnvoyClient(email=auth_email, access_key=auth_access_key)
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
                       upload_root_dir: bool,
                       delete_local_files_after_upload: bool = False) -> RemoteProject:

        if not self.is_user_signed_in():
            raise NotSignedInError("Must be signed-in to upload a project.")

        self._log.info("Uploading packed project")

        project_dir = str(packed_project.get_root_dir())
        project_name = packed_project.get_name()

        gm_project = gridmarkets.Project(project_dir, project_name)

        if upload_root_dir:
            # add all files to packed project files list
            files = get_files_in_directory(packed_project.get_root_dir())
            packed_project.add_files(files)

            self._log.info("Marking directory \"" + project_dir + "\" for upload.")
            gm_project.add_folders(project_dir)

        else:
            # get project files as strings
            files = list(map(lambda file: str(file), packed_project.get_files().copy()))

            for file in files:
                self._log.info("Marking \"" + file + "\" for upload.")

            gm_project.add_files(*files)

        self._envoy_client.upload_project_files(gm_project)

        # Todo - remove imports from blender add-on module
        from gridmarkets_blender_addon.blender_plugin.remote_project import convert_packed_project
        return convert_packed_project(packed_project)

    def submit_to_remote_project(self, remote_project: RemoteProject, job_preset: JobPreset) -> None:
        # Todo - remove blender plugin imports
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        if not self.is_user_signed_in():
            raise NotSignedInError("Must be signed-in to Submit a job.")

        self._log.info(
            "Preparing job " + job_preset.get_name() + " for submission to remote project " + remote_project.get_name())

        client = self._envoy_client
        project = gridmarkets.Project(str(remote_project.get_root_dir()), remote_project.get_name())

        self._log.info("Calculating Job parameters...")
        job_settings = {}
        for job_preset_attribute in job_preset.get_job_preset_attributes():
            key = job_preset_attribute.get_key()
            value = job_preset_attribute.eval(plugin, remote_project)
            job_settings[key] = value
            self._log.info("Job Parameter '" + key + "': " + str(value))

        job = gridmarkets.Job(**job_settings)

        # add job to project
        project.add_jobs(job)

        # submit the job to the remote project
        self._log.info(
            "Submitting job " + job_preset.get_name() + " to existing remote project " + remote_project.get_name())
        client.submit_project(project, skip_upload=True)

        self._log.info("Job submitted - See Render Manager for details")

    def get_cached_root_directories(self) -> typing.List[str]:
        return list(map(lambda x: x.get_name(), self._remote_projects_cache.get_value()))

    def get_root_directories(self, ignore_cache: bool = False) -> typing.List[str]:
        self._log.info("Getting root directories. ignore_cache=" + str(ignore_cache))

        if ignore_cache or not self._remote_projects_cache.is_cached():
            self.get_remote_projects(ignore_cache=True)

        return self.get_cached_root_directories()

    def get_remote_projects(self, ignore_cache=False) -> typing.List[EnvoyProject]:
        self._log.info("Getting Envoy Projects. ignore_cache=" + str(ignore_cache))

        if ignore_cache or not self._remote_projects_cache.is_cached():
            try:
                import requests
                r = requests.get(self._envoy_client.url + '/projects')
                json = r.json()
                projects = json.get("projects", [])

                envoy_projects = []

                for project in projects:
                    envoy_projects.append(EnvoyProject(project.get('name', ''),
                                                       project.get('deleting', False),
                                                       project.get('num_files', 0),
                                                       project.get('total_size', 0),
                                                       project.get('auto_downloading', False),
                                                       project.get('watched_list', [])))

                projects = sorted(envoy_projects, key=lambda s: s.get_name().casefold())

            except Exception as e:
                self._log.error("Could not make request to envoy API. " + str(e))
                self.sign_out()
                projects = []

            self._remote_projects_cache.set_value(projects)

        return self._remote_projects_cache.get_value()

    def get_product_versions(self, product: str, ignore_cache: bool = False) -> typing.List[str]:
        if ignore_cache or not self._product_resolver.is_cached():
            # get product resolver
            resolver = self._envoy_client.get_product_resolver()

            # cache all products
            self._product_resolver.set_value(resolver.get_all_types())

        # sorted by latest version to oldest version
        return sorted(self._product_resolver.get_value().get(product, {}).get("versions", []),
                      key=lambda s: s.casefold(), reverse=True)

    def get_closest_matching_product_version(self, product: str, product_version: str, ignore_cache: bool = False) -> \
            typing.Optional[str]:
        product_versions = self.get_product_versions(product, ignore_cache=ignore_cache)

        if not len(product_versions):
            return None

        # first check to see if the provided version exactly matches a version option
        for version_option in product_versions:
            if version_option == product_version:
                return version_option

        # if not then we are down to heuristics
        import difflib
        return difflib.get_close_matches(product_version, product_versions)[0]

    def get_remote_project_files(self, project_name: str, ignore_cache=False) -> typing.List[EnvoyFile]:
        """ Returns a list of Envoy File objects, if project does not exist it returns an empty list. """

        if ignore_cache or project_name not in self._project_files_dictionary_cache:
            import requests
            r = requests.get(self._envoy_client.url + '/project/' + project_name + '/Files')
            json = r.json()
            all_files = json.get('project_files', {}).get('all_files', [])

            envoy_files = []
            for file in all_files:
                envoy_files.append(EnvoyFile(
                    file.get('CheckSum', ''),
                    file.get('LastModified', ''),
                    file.get('Name', ''),
                    file.get('Key', ''),
                    file.get('Size', 0),
                    file.get('FmtName', ''),
                ))

            self._project_files_dictionary_cache[project_name] = envoy_files

        return self._project_files_dictionary_cache[project_name]

    def clear_project_files_cache(self):
        self._project_files_dictionary_cache.clear()

    def get_available_credits(self) -> int:
        import requests
        r = requests.get(self._envoy_client.url + '/credits-info')
        json = r.json()
        available_credits = json.get('credits_available', 0)
        return available_credits

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

__all__ = 'EnvoyProject', 'EnvoyFile', 'GridMarketsAPIClient'

import typing
import pathlib

from .remote_project import convert_packed_project
from .xml_api_schema_parser import XMLAPISchemaParser
from . import constants as api_constants
from ..api_client import APIClient as MetaAPIClient
from ..cached_value import CachedValue
from ..user_info import UserInfo
from ..machine_option import MachineOption
from ..product import Product
from ..utils import get_files_in_directory, get_exception_with_traceback
from ..errors import *
from .. import attribute_types

import gridmarkets
from gridmarkets.errors import AuthenticationError, APIError

if typing.TYPE_CHECKING:
    from . import RemoteProject
    from .. import FactoryCollection, User, APISchema, JobPreset, PackedProject, LoggingCoordinator, Plugin


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
    def __init__(self, check_sum: str, last_modified: str, name: str, key: str, size: int, fmt_name: str):
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


class GridMarketsAPIClient(MetaAPIClient):
    http_api_endpoint = "https://api.gridmarkets.com:8003/api/render/1.0/"

    def __init__(self,
                 plugin: 'Plugin',
                 logging_coordinator: 'LoggingCoordinator',
                 factory_collection: 'FactoryCollection'):

        MetaAPIClient.__init__(self, plugin)
        self._factory_collection = factory_collection
        self._signed_in: bool = False
        self._envoy_client: typing.Optional[gridmarkets.EnvoyClient] = None
        self._log = logging_coordinator.get_logger("GridMarketsAPIClient")

        # used for caching projects
        self._api_schema_cache = CachedValue(None)
        self._remote_projects_cache: CachedValue = CachedValue([])
        self._project_files_dictionary_cache = {}
        self._product_resolver: CachedValue = CachedValue(None)
        self._products_cache = CachedValue([])
        self._cached_machine_options = CachedValue({})
        self._cached_user_info = CachedValue(UserInfo(9999, 60))

    def clear_all_caches(self):
        self._log.info("Clearing cached API data")
        self._remote_projects_cache.reset_and_clear_cache()
        self._project_files_dictionary_cache.clear()
        self._product_resolver.reset_and_clear_cache()
        self._products_cache.reset_and_clear_cache()
        self._cached_machine_options.reset_and_clear_cache()
        self._cached_user_info.reset_and_clear_cache()

    def sign_in(self, user: 'User', skip_validation: bool = False) -> None:
        self._log.info("Signing in as " + user.get_auth_email())

        MetaAPIClient.sign_in(self, user, skip_validation=skip_validation)

        self._envoy_client = gridmarkets.EnvoyClient(email=user.get_auth_email(), access_key=user.get_auth_key())

        # refresh caches
        self.clear_all_caches()
        self.get_root_directories(ignore_cache=True)
        self.get_api_schema(ignore_cache=True)
        self.get_user_info(ignore_cache=True)
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

    def get_signed_in_user(self) -> typing.Optional['User']:
        return MetaAPIClient.get_signed_in_user(self)

    def get_cached_api_schema(self) -> typing.Optional['APISchema']:
        return self._api_schema_cache.get_value()

    def get_api_schema(self, factory_collection: 'FactoryCollection' = None, ignore_cache=False) -> 'APISchema':
        self._log.info("Getting api schema. ignore_cache=" + str(ignore_cache))

        if factory_collection is None:
            factory_collection = self._factory_collection

        if ignore_cache or not self._api_schema_cache.is_cached():
            self._log.info("Fetching api schema from XML source.")

            try:
                self._api_schema_cache.set_value(XMLAPISchemaParser.parse(factory_collection))
            except Exception as e:
                msg = "Could not fetch api schema: " + get_exception_with_traceback(e)
                self._log.error(msg, exc_info=True)
                raise APIClientError(msg)

        self._log.info("Returning api schema")
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
            except APIError as e:
                e_msg = str(e.user_message)

                # pretty error message for common errors
                if e_msg.startswith("Unexpected error communicating with Envoy.Please start Envoy"):
                    e_msg = "Unable to connect to Envoy."

                raise APIClientError(message=e_msg)

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
                       packed_project: 'PackedProject',
                       upload_root_dir: bool,
                       delete_local_files_after_upload: bool = False) -> 'RemoteProject':

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

        try:
            self._envoy_client.upload_project_files(gm_project)
        except APIError as e:
            raise APIClientError(e.user_message)

        self._log.info("Uploaded project")

        return convert_packed_project(packed_project, self.get_plugin())

    def _get_gm_job(self, job_preset: 'JobPreset', remote_project: 'RemoteProject') -> gridmarkets.Job:
        self._log.info("Calculating Job parameters...")
        job_settings = {}
        for job_preset_attribute in job_preset.get_job_preset_attributes():
            key = job_preset_attribute.get_key()
            value = job_preset_attribute.eval(self.get_plugin(), remote_project)
            job_settings[key] = value
            self._log.info("Job Parameter '" + key + "': " + str(value))

            # machine type attributes implicitly contain a gpu attribute
            if key == api_constants.API_KEYS.MACHINE_TYPE:
                attribute = job_preset_attribute.get_job_attribute().get_attribute()
                if attribute.get_type() != attribute_types.AttributeType.ENUM:
                    continue

                enum_attribute: attribute_types.EnumAttributeType = attribute
                if enum_attribute.get_subtype() != attribute_types.EnumSubtype.MACHINE_TYPE.value:
                    continue

                # we need to find the machine type with this id and work out if it is a gpu machine or not
                machine_id = value

                subtype_kwargs = attribute.get_subtype_kwargs()
                app = subtype_kwargs.get(api_constants.SUBTYPE_KEYS.ENUM.MACHINE_TYPE.PRODUCT)
                operation = subtype_kwargs.get(api_constants.SUBTYPE_KEYS.ENUM.MACHINE_TYPE.OPERATION)

                machines = self.get_machines(app, operation)

                for machine in machines:
                    if machine.get_id() == machine_id:
                        if machine.is_gpu_machine():
                            key = api_constants.API_KEYS.GPU
                            value = True
                            job_settings[key] = value
                            self._log.info("Job Parameter '" + key + "': " + str(value))

        job = gridmarkets.Job(**job_settings)

        # Check the app is supported
        if job.app not in self.get_product_app_types():
            msg = "App \"" + job.app + "\" is not supported for your account. Please contact " + api_constants.COMPANY_NAME + " support for details."
            self._log.error(msg)
            raise UnsupportedApplicationError(msg)

        # Check the version is supported
        if job.app_version not in self.get_product_versions(job.app):
            msg = "Version \"" + job.app_version + "\" for app_type \"" + job.app + \
                  "\" is not supported for your account. Please contact " + api_constants.COMPANY_NAME + \
                  " support for details."

            self._log.error(msg)
            raise UnsupportedApplicationError(msg)

        return job

    def submit_new_project(self,
                           packed_project: 'PackedProject',
                           job_preset: 'JobPreset',
                           delete_local_files_after_upload: bool = False) -> 'RemoteProject':
        plugin = self.get_plugin()

        if not self.is_user_signed_in():
            raise NotSignedInError("Must be signed-in to Submit a job.")

        self._log.info("Preparing to submit current scene as project \"" + packed_project.get_name() +
                       "\" with job \"" + job_preset.get_name() + "\".")

        client = self._envoy_client
        project_dir = str(packed_project.get_root_dir())
        project_name = packed_project.get_name()

        gm_project = gridmarkets.Project(project_dir, project_name)

        # add all files to packed project files list
        files = get_files_in_directory(packed_project.get_root_dir())
        packed_project.add_files(files)

        self._log.info("Marking directory \"" + project_dir + "\" for upload.")
        gm_project.add_folders(project_dir)

        remote_project = convert_packed_project(packed_project, self.get_plugin())

        job = self._get_gm_job(job_preset, remote_project)

        # add job to project
        gm_project.add_jobs(job)

        # submit the job to the remote project
        self._log.info(
            "Submitting current scene with job \"" + job_preset.get_name() + "\" to project \"" + project_name + "\".")

        try:
            client.submit_project(gm_project, skip_upload=False)
        except APIError as e:
            raise APIClientError(e.user_message)

        self._log.info("Job submitted - See Render Manager for details")

    def submit_to_remote_project(self, remote_project: 'RemoteProject', job_preset: 'JobPreset') -> None:
        plugin = self.get_plugin()

        if not self.is_user_signed_in():
            raise NotSignedInError("Must be signed-in to Submit a job.")

        # check the project exists
        if len(remote_project.get_files(force_update=True)) <= 0:
            msg = "Can not submit job to remote project \"" + remote_project.get_name() + \
                  "\", project does not exist."
            self._log.warning(msg)
            raise APIClientError(msg)

        # check the project has finished uploading
        if remote_project.get_remaining_bytes_to_upload(force_update=True) != 0:
            msg = "Can not submit job to remote project \"" + remote_project.get_name() + \
                  "\", project has not finished uploading."
            self._log.warning(msg)
            raise APIClientError(msg)

        self._log.info(
            "Preparing job " + job_preset.get_name() + " for submission to remote project " + remote_project.get_name())

        client = self._envoy_client
        project = gridmarkets.Project(str(remote_project.get_root_dir()), remote_project.get_name())

        job = self._get_gm_job(job_preset, remote_project)

        # add job to project
        project.add_jobs(job)

        # submit the job to the remote project
        self._log.info(
            "Submitting job " + job_preset.get_name() + " to existing remote project " + remote_project.get_name())
        client.submit_project(project, skip_upload=True)

        self._log.info("Job submitted - See Render Manager for details")

    def update_remote_project_status(self, remote_project: 'RemoteProject') -> None:

        self._log.info("Fetching project status for project \"" + remote_project.get_name() + "\"...")

        http_client = self._envoy_client.http_client
        url = self._envoy_client.url + "/project-status/" + remote_project.get_name()

        try:
            resp = http_client.request('get', url)
        except Exception as e:
            msg = "Could not fetch project status for project \"" + remote_project.get_name() + "\". " + \
                  get_exception_with_traceback(e)
            self._log.error(msg)
            raise APIClientError(msg)
        else:
            if resp.status_code == 200:
                self._log.info("Fetched project status for project \"" + remote_project.get_name() + "\".")

                json = resp.json()

                details = json.get('Details')

                total_bytes = 0
                total_bytes_done = 0
                files = set()

                if len(details.items()) > 0:
                    for detail_key, detail in details.items():
                        total_bytes_for_detail = detail.get('BytesTotal', 1)
                        bytes_done_for_detail = detail.get('BytesDone', 0)

                        total_bytes += total_bytes_for_detail
                        total_bytes_done += bytes_done_for_detail
                        files.add(pathlib.Path(detail_key))
                else:
                    # It is possible that the project has already been uploaded and Envoy is not bothering to show the
                    # project status for it any more.  Check to see if there are any files uploaded for this project.
                    uploaded_files = self.get_remote_project_files(remote_project.get_name(), ignore_cache=True)
                    if len(uploaded_files) >= 0:
                        for file in uploaded_files:
                            total_bytes += file.get_size()
                            total_bytes_done += file.get_size()
                            files.add(pathlib.Path(file.get_key()))

                remote_project.set_size(total_bytes)
                remote_project.set_total_bytes_done_uploading(total_bytes_done)
                remote_project.set_file_list(files)

            if resp.status_code == 404:
                msg = "404: {0} not found".format(url)
                self._log.error(msg)
                raise APIClientError(msg)

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
            url = self._envoy_client.url + '/projects'
            self._log.info("Fetching existing remote project directories from \"" + url + "\"")

            try:
                import requests
                r = requests.get(url)
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

        remote_projects = self._remote_projects_cache.get_value()
        self._log.info("Returning " + str(len(remote_projects)) + " Envoy Project(s).")
        return remote_projects

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

            try:
                r = requests.get(self._envoy_client.url + '/project/' + project_name + '/Files')
            except Exception as e:
                raise APIClientError(str(e))

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

    def get_products(self, ignore_cache=False) -> typing.List['Product']:
        self._log.info("Getting products list...")

        if not self.is_user_signed_in():
            msg = "Must be signed-in to get products list."
            self._log.error(msg)
            raise NotSignedInError(msg)

        if ignore_cache or not self._products_cache.is_cached():
            url = '{0}/products'.format(self._envoy_client.url)

            self._log.info("Fetching products list from " + url)

            try:
                resp = self._envoy_client.http_client.request('get', url)
            except Exception as e:
                msg = "Could not fetch products list: " + get_exception_with_traceback(e)
                self._log.error(msg)
                raise APIClientError(msg)
            else:
                if resp.status_code == 200:
                    content = resp.json()

                    def parse_product(json) -> 'Product':
                        return Product(json.get('id', -1),
                                       json.get('name', ''),
                                       json.get('app_type', ''),
                                       json.get('version', ''))

                    self._log.info("Caching fetched products...")
                    self._products_cache.set_value(list(map(lambda x: parse_product(x), content)))

                if resp.status_code == 404:
                    msg = "404: {0} not found".format(url)
                    self._log.error(msg)
                    raise APIClientError(msg)

        cached_products = self._products_cache.get_value()
        self._log.info("Returning " + str(len(cached_products)) + " cached products...")
        return cached_products

    def get_products_with_app_type(self, app_type: str, ignore_cache=False) -> typing.List['Product']:
        products = self.get_products(ignore_cache=ignore_cache)
        return list(filter(lambda x: x.get_app_type() == app_type, products))

    def get_product_app_types(self, ignore_cache=False) -> typing.List[str]:
        return sorted(list(set(map(lambda x: x.get_app_type(), self.get_products(ignore_cache=ignore_cache)))),
                      key=lambda s: s.casefold(), reverse=True)

    def get_user_info(self, ignore_cache=False) -> 'UserInfo':
        self._log.info("Getting User info. ignore_cache=" + str(ignore_cache))

        if ignore_cache or not self._cached_user_info.is_cached():
            url = '{0}/user-info'.format(self._envoy_client.url)
            self._log.info("Fetching user info from url \"" + url + "\"")

            try:
                resp = self._envoy_client.http_client.request('get', url)
            except Exception as e:
                msg = "Could not fetch user info: " + get_exception_with_traceback(e)
                self._log.error(msg)
                raise APIClientError(msg)
            else:
                if resp.status_code == 200:
                    content = resp.json().get('data')

                    user_info = UserInfo(content.get('max_throughput', 9999), content.get('job_throughput_limit', 60))

                    self._log.info("Caching user info...")
                    self._cached_user_info.set_value(user_info)

                if resp.status_code == 404:
                    msg = "404: {0} not found".format(url)
                    self._log.error(msg)
                    raise APIClientError(msg)

        self._log.info("Returning User info.")
        return self._cached_user_info.get_value()

    def get_machines(self, app: str,
                     operation: str,
                     ignore_cache: bool = False) -> typing.List['MachineOption']:

        cached_machine_options = self._cached_machine_options.get_value()

        if app in cached_machine_options:
            app_machine_options = cached_machine_options[app]
            if operation in app_machine_options:
                operation_machine_options = app_machine_options[operation]

                if not ignore_cache:
                    return operation_machine_options

        try:
            self._log.info("Fetching machine types for product \"" + app + "\" (operation=\"" + operation + "\")")
            cpu_machine_options = self._envoy_client.get_machines(app, operation, is_gpu=False)
            gpu_machine_options = self._envoy_client.get_machines(app, operation, is_gpu=True)
        except APIError as e:
            msg = str(e.user_message)
            self._log.error(msg)
            raise APIClientError(message=msg)

        def parse_machine_option(machine_option, is_gpu):
            return MachineOption(machine_option['id'], machine_option['name'], machine_option['is_default'], is_gpu)

        cpu_machine_options_list = list(map(lambda x: parse_machine_option(x, False), cpu_machine_options))
        gpu_machine_options_list = list(map(lambda x: parse_machine_option(x, True), gpu_machine_options))
        combined_machine_options = cpu_machine_options_list + gpu_machine_options_list

        # It is possible no machine options were returned, in that case we can still let users choose between their
        # default machine options (cpu vs gpu)
        if len(combined_machine_options) <= 0:
            combined_machine_options.append(("default_machine_cpu", "Defualt Machine_cpu",
                                             "Use your default cpu machine (As defined on your profile page in the portal)"))
            combined_machine_options.append(("default_machine_gpu", "Defualt Machine_cpu",
                                             "Use your default gpu machine (As defined on your profile page in the portal)"))

        app_machine_options = cached_machine_options.get(app, {})
        app_machine_options[operation] = combined_machine_options
        cached_machine_options[app] = app_machine_options

        self._cached_machine_options.set_value(cached_machine_options)

        return combined_machine_options

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

from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.gridmarkets.api_client import GridMarketsAPIClient
from gridmarkets_blender_addon.blender_plugin.decorators.attach_blender_plugin import attach_blender_plugin
from gridmarkets_blender_addon import utils_blender
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
import pathlib

@attach_blender_plugin
class APIClient(GridMarketsAPIClient):

    def __init__(self):
        GridMarketsAPIClient.__init__(self)

    def sign_in(self, user: User, skip_validation: bool = False) -> None:
        GridMarketsAPIClient.sign_in(self, user)
        utils_blender.force_redraw_addon()

    def sign_out(self) -> None:
        GridMarketsAPIClient.sign_out(self)
        utils_blender.force_redraw_addon()

    def connected(self) -> bool:
        raise NotImplementedError

    def submit_new_vray_project(self, packed_project: PackedProject, job_name: str, frame_ranges: str, output_height,
                                output_width,
                                output_prefix, output_format, output_path: pathlib.Path):
        import bpy
        import inspect
        from gridmarkets_blender_addon.utils_blender import get_wrapped_logger
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.invalid_input_error import InvalidInputError

        from gridmarkets.project import Project
        from gridmarkets.job import Job
        from gridmarkets.watch_file import WatchFile
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError

        # get method logger
        log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

        packed_dir = str(packed_project.get_root_dir())

        try:
            # create an instance of Envoy client

            client = self._envoy_client

            # create the project
            project = Project(packed_dir, packed_project.get_name())

            # add files to project
            # only files and folders within the project path can be added, use relative or full path
            # any other paths passed will be ignored
            log.info("Adding '" + packed_dir + "' to " + constants.COMPANY_NAME + " project...")
            project.add_folders(packed_dir)

            # get product resolver
            resolver = client.get_product_resolver()

            # get products for Houdini product type
            qry = 'vray'
            products = resolver.get_versions_by_type(qry)

            JOB_NAME = job_name
            PRODUCT_TYPE = "vray"
            PRODUCT_VERSION = products[-1]
            OPERATION = "render"
            PATH = '/' + packed_project.get_name() + '/' + str(packed_project.get_relative_main_file())
            FRAMES = frame_ranges
            OUTPUT_HEIGHT = output_height
            OUTPUT_WIDTH = output_width
            OUTPUT_PREFIX = output_prefix
            OUTPUT_FORMAT = output_format
            REMAP_FILE = str(packed_project.get_attribute("REMAP_FILE"))

            job = Job(
                JOB_NAME,  # job name
                PRODUCT_TYPE,  # product type
                PRODUCT_VERSION,  # product version
                OPERATION,  # operation
                PATH,
                # job file to be run, note that the path is relative to the project name which is also the remote folder name
                frames=FRAMES,  # rest are all job specific params
                output_height=OUTPUT_HEIGHT,
                output_width=OUTPUT_WIDTH,
                output_prefix=OUTPUT_PREFIX,
                output_format=OUTPUT_FORMAT,
                remap_file=REMAP_FILE,
            )

            # results regex pattern to download
            # `project.remote_output_folder` provides the remote root folder under which results are available
            # below is the regex to look for all folders and files under `project.remote_output_folder`
            output_pattern = '{0}/.+'.format(project.remote_output_folder)

            # create a watch file
            watch_file = WatchFile(output_pattern, str(output_path))

            # set the output directory
            project.add_watch_files(watch_file)

            log.info("Submitted V-Ray Job Settings: \n" +
                     "\tproject_name: %s\n" % project.name +
                     "\tjob.app: %s\n" % job.app +
                     "\tjob.name: %s\n" % job.name +
                     "\tjob.app_version: %s\n" % job.app_version +
                     "\tjob.operation: %s\n" % job.operation +
                     "\tjob.path: %s\n" % job.path +
                     "\tjob.frames: %s\n" % job.params['frames'] +
                     "\tjob.output_width: %s\n" % job.params['output_width'] +
                     "\tjob.output_height: %s\n" % job.params['output_height'] +
                     "\tjob.output_prefix: %s\n" % job.params['output_prefix'] +
                     "\tjob.output_format: %s\n" % job.params['output_format'] +
                     "\tjob.remap_file: %s\n" % job.params['remap_file'] +
                     "\tdownload_path: %s\n" % str(output_path)
                     )

            project.add_jobs(job)

            client.submit_project(project)

            log.info("Submitted V-Ray job")

            remote_project = RemoteProject(packed_project.get_name(),
                                           packed_project.get_root_dir(),
                                           packed_project.get_relative_main_file(),
                                           packed_project.get_relative_files(),
                                           packed_project.get_attributes())

            remote_project_container = self.get_plugin().get_remote_project_container()
            remote_project_container.append(remote_project)

        except InvalidInputError as e:
            log.warning("Invalid Input Error: " + e.user_message)
            raise e
        except AuthenticationError as e:
            log.error("Authentication Error: " + e.user_message)
            raise e
        except InsufficientCreditsError as e:
            log.error("Insufficient Credits Error: " + e.user_message)
            raise e
        except InvalidRequestError as e:
            log.error("Invalid Request Error: " + e.user_message)
            raise e
        except APIError as e:
            log.error("API Error: " + str(e.user_message))
            raise e

    def submit_existing_vray_project(self, remote_project: RemoteProject, job_name: str, frame_ranges: str, output_height,
                                     output_width, output_prefix, output_format, output_path: pathlib.Path):
        import bpy
        import inspect
        from gridmarkets_blender_addon.utils_blender import get_wrapped_logger
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.invalid_input_error import InvalidInputError

        from gridmarkets.project import Project
        from gridmarkets.job import Job
        from gridmarkets.watch_file import WatchFile
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError

        # get method logger
        log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

        try:
            # create an instance of Envoy client
            client = self._envoy_client

            # create the project
            project = Project(remote_project.get_root_dir(), remote_project.get_name())

            # get product resolver
            resolver = client.get_product_resolver()

            # get products for Houdini product type
            qry = 'vray'
            products = resolver.get_versions_by_type(qry)

            JOB_NAME = job_name
            PRODUCT_TYPE = "vray"
            PRODUCT_VERSION = products[-1]
            OPERATION = "render"
            PATH = '/' + remote_project.get_name() + '/' + str(remote_project.get_main_file())
            FRAMES = frame_ranges
            OUTPUT_HEIGHT = output_height
            OUTPUT_WIDTH = output_width
            OUTPUT_PREFIX = output_prefix
            OUTPUT_FORMAT = output_format
            REMAP_FILE = str(remote_project.get_attribute("REMAP_FILE"))

            job = Job(
                JOB_NAME,  # job name
                PRODUCT_TYPE,  # product type
                PRODUCT_VERSION,  # product version
                OPERATION,  # operation
                PATH,
                # job file to be run, note that the path is relative to the project name which is also the remote folder name
                frames=FRAMES,  # rest are all job specific params
                output_height=OUTPUT_HEIGHT,
                output_width=OUTPUT_WIDTH,
                output_prefix=OUTPUT_PREFIX,
                output_format=OUTPUT_FORMAT,
                remap_file=REMAP_FILE,
            )

            # results regex pattern to download
            # `project.remote_output_folder` provides the remote root folder under which results are available
            # below is the regex to look for all folders and files under `project.remote_output_folder`
            output_pattern = '{0}/.+'.format(project.remote_output_folder)

            # create a watch file
            watch_file = WatchFile(output_pattern, str(output_path))

            # set the output directory
            project.add_watch_files(watch_file)

            log.info("Submitted V-Ray Job Settings: \n" +
                     "\tproject_name: %s\n" % project.name +
                     "\tjob.app: %s\n" % job.app +
                     "\tjob.name: %s\n" % job.name +
                     "\tjob.app_version: %s\n" % job.app_version +
                     "\tjob.operation: %s\n" % job.operation +
                     "\tjob.path: %s\n" % job.path +
                     "\tjob.frames: %s\n" % job.params['frames'] +
                     "\tjob.output_width: %s\n" % job.params['output_width'] +
                     "\tjob.output_height: %s\n" % job.params['output_height'] +
                     "\tjob.output_prefix: %s\n" % job.params['output_prefix'] +
                     "\tjob.output_format: %s\n" % job.params['output_format'] +
                     "\tjob.remap_file: %s\n" % job.params['remap_file'] +
                     "\tdownload_path: %s\n" % str(output_path)
                     )

            project.add_jobs(job)

            client.submit_project(project, skip_upload=True)

            log.info("Submitted V-Ray job")

        except InvalidInputError as e:
            log.warning("Invalid Input Error: " + e.user_message)
            raise e
        except AuthenticationError as e:
            log.error("Authentication Error: " + e.user_message)
            raise e
        except InsufficientCreditsError as e:
            log.error("Insufficient Credits Error: " + e.user_message)
            raise e
        except InvalidRequestError as e:
            log.error("Invalid Request Error: " + e.user_message)
            raise e
        except APIError as e:
            log.error("API Error: " + str(e.user_message))
            raise e

    def submit_new_blender_project(self, packed_project: PackedProject):
        import bpy
        import inspect
        from gridmarkets_blender_addon.utils_blender import get_wrapped_logger
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.invalid_input_error import InvalidInputError

        from gridmarkets.project import Project
        from gridmarkets.job import Job
        from gridmarkets.watch_file import WatchFile
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError

        context = bpy.context
        scene = context.scene

        # get method logger
        log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

        # define a helper function for setting the progress
        def _set_progress(status=None):
            if status is not None:
                setattr(context.scene.props, "submitting_project_status", status)

        # set the submitting flag to true
        setattr(context.scene.props, "submitting_project", True)

        # set the progress to 0 and set a status message
        _set_progress(status="Starting job submission")

        # log the start of the operation
        log.info("Starting submit operation...")

        try:
            log.info("Uploading project for job submit...")
            _set_progress(status="Uploading project")

            if packed_project.get_name() is None:
                raise InvalidInputError("Project name can not be None type")

            project_name = packed_project.get_name()

            client = self._envoy_client

            project = Project(str(packed_project.get_root_dir()),packed_project.get_name())

            # add files to project
            # only files and folders within the project path can be added, use relative or full path
            # any other paths passed will be ignored
            project.add_folders(packed_project.get_root_dir())

            render_file = '/' + packed_project.get_name() + '/' + str(packed_project.get_relative_main_file())

            job = utils_blender.get_job(context, render_file)


            # add job to project
            project.add_jobs(job)

            # results regex pattern to download
            # `project.remote_output_folder` provides the remote root folder under which results are available
            # below is the regex to look for all folders and files under `project.remote_output_folder`
            output_pattern = '{0}/.+'.format(project.remote_output_folder)

            download_path = utils_blender.get_job_output_path_abs(context)

            # create a watch file
            watch_file = WatchFile(output_pattern, download_path)

            # set the output directory
            project.add_watch_files(watch_file)

            log.info("Submitted Job Settings: \n" +
                     "\tproject_name: %s\n" % project_name +
                     "\tjob.app: %s\n" % job.app +
                     "\tjob.name: %s\n" % job.name +
                     "\tjob.app_version: %s\n" % job.app_version +
                     "\tjob.operation: %s\n" % job.operation +
                     "\tjob.path: %s\n" % job.path +
                     "\tjob.frames: %s\n" % job.params['frames'] +
                     "\tjob.output_prefix: %s\n" % job.params['output_prefix'] +
                     "\tjob.output_format: %s\n" % job.params['output_format'] +
                     "\tjob.engine: %s\n" % job.params['engine'] +
                     "\tdownload_path: %s\n" % download_path
                     )

            # submit project
            log.info("Submitting job and uploading files...")
            _set_progress(status="Submitting project")
            client.submit_project(project)

            log.info("Job submitted")

            remote_project = RemoteProject(packed_project.get_name(),
                                           packed_project.get_root_dir(),
                                           packed_project.get_relative_main_file(),
                                           packed_project.get_relative_files(),
                                           packed_project.get_attributes())

            remote_project_container = self.get_plugin().get_remote_project_container()
            remote_project_container.append(remote_project)

        except InvalidInputError as e:
            log.warning("Invalid Input Error: " + e.user_message)
        except AuthenticationError as e:
            log.error("Authentication Error: " + e.user_message)
        except InsufficientCreditsError as e:
            log.error("Insufficient Credits Error: " + e.user_message)
        except InvalidRequestError as e:
            log.error("Invalid Request Error: " + e.user_message)
        except APIError as e:
            log.error("API Error: " + str(e.user_message))
        finally:
            log.info("Finished submit operation - Job Should appear in the Render Manager is submitted successfully")
            setattr(context.scene.props, "submitting_project", False)

    def submit_existing_blender_project(self, remote_project: RemoteProject):
        import bpy
        import inspect
        from gridmarkets_blender_addon.utils_blender import get_wrapped_logger
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.invalid_input_error import InvalidInputError

        from gridmarkets.project import Project
        from gridmarkets.job import Job
        from gridmarkets.watch_file import WatchFile
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError

        context = bpy.context
        scene = context.scene

        # get method logger
        log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

        # define a helper function for setting the progress
        def _set_progress(status=None):
            if status is not None:
                setattr(context.scene.props, "submitting_project_status", status)

        # set the submitting flag to true
        setattr(context.scene.props, "submitting_project", True)

        # set the progress to 0 and set a status message
        _set_progress(status="Starting job submission")

        # log the start of the operation
        log.info("Starting submit operation...")

        try:
            project_name = remote_project.get_name()

            client = self._envoy_client

            project = Project(str(remote_project.get_root_dir()), remote_project.get_name())

            render_file = '/' + remote_project.get_name() + '/' + str(remote_project.get_main_file())

            job = utils_blender.get_job(context, render_file)

            # add job to project
            project.add_jobs(job)

            # results regex pattern to download
            # `project.remote_output_folder` provides the remote root folder under which results are available
            # below is the regex to look for all folders and files under `project.remote_output_folder`
            output_pattern = '{0}/.+'.format(project.remote_output_folder)

            download_path = utils_blender.get_job_output_path_abs(context)

            # create a watch file
            watch_file = WatchFile(output_pattern, download_path)

            # set the output directory
            project.add_watch_files(watch_file)

            log.info("Submitted Job Settings: \n" +
                     "\tproject_name: %s\n" % project_name +
                     "\tjob.app: %s\n" % job.app +
                     "\tjob.name: %s\n" % job.name +
                     "\tjob.app_version: %s\n" % job.app_version +
                     "\tjob.operation: %s\n" % job.operation +
                     "\tjob.path: %s\n" % job.path +
                     "\tjob.frames: %s\n" % job.params['frames'] +
                     "\tjob.output_prefix: %s\n" % job.params['output_prefix'] +
                     "\tjob.output_format: %s\n" % job.params['output_format'] +
                     "\tjob.engine: %s\n" % job.params['engine'] +
                     "\tdownload_path: %s\n" % download_path
                     )

            # submit project
            log.info("Submitting job (skipping file uploads")
            _set_progress(status="Submitting project")
            client.submit_project(project, skip_upload=True)

            log.info("Job submitted")

        except InvalidInputError as e:
            log.warning("Invalid Input Error: " + e.user_message)
        except AuthenticationError as e:
            log.error("Authentication Error: " + e.user_message)
        except InsufficientCreditsError as e:
            log.error("Insufficient Credits Error: " + e.user_message)
        except InvalidRequestError as e:
            log.error("Invalid Request Error: " + e.user_message)
        except APIError as e:
            log.error("API Error: " + str(e.user_message))
        finally:
            log.info("Finished submit operation - Job Should appear in the Render Manager is submitted successfully")
            setattr(context.scene.props, "submitting_project", False)
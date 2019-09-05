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

import bpy
# noinspection PyUnresolvedReferences
import addon_utils
import inspect
import pathlib
import os
import collections
import json

from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon import utils
from gridmarkets_blender_addon.invalid_input_error import InvalidInputError
from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

from blender_asset_tracer import trace, pack

# global client to reuse
_envoy_client = None


def get_wrapped_logger(name):
    from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
    return get_wrapped_logger(name)


def trace_blend_file(blend_file_path, progress_cb=None):
    """ Finds all the dependencies for a given .blend file

    :param blend_file_path: the .blend file to inspect
    :type blend_file_path: str
    :param progress_cb: The progress reporting callback instance
    :type progress_cb: blender_asset_tracer.pack.progress.Callback
    :return: A dictionary of .blend files and their sets of dependencies
    :rtype: collections.defaultdict(set)
    """

    # the dependencies as a mapping from the blend file to its set of dependencies.
    dependencies = collections.defaultdict(set)

    # Find the dependencies
    for usage in trace.deps(pathlib.Path(blend_file_path), progress_cb):
        file_path = usage.block.bfile.filepath.absolute()
        for assetPath in usage.files():
            asset_path = assetPath.resolve()
            dependencies[str(file_path)].add(assetPath)

    return dependencies


def pack_blend_file(blend_file_path, target_dir_path, progress_cb=None):
    """ Packs a Blender .blend file to a target folder using blender_asset_tracer

    :param blend_file_path: The .blend file to pack
    :type blend_file_path: str
    :param target_dir_path: The path to the directory which will contain the packed files
    :type target_dir_path: str
    :param progress_cb: The progress reporting callback instance
    :type progress_cb: blender_asset_tracer.pack.progress.Callback
    """

    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Starting pack operation....")

    blend_file_path = pathlib.Path(blend_file_path)
    project_root_path = blend_file_path.parent
    target_dir_path = pathlib.Path(target_dir_path)

    log.info("blend_file_path: %s" % str(blend_file_path))
    log.info("project_root_path: %s" % str(project_root_path))
    log.info("target_dir_path: %s" % str(target_dir_path))

    # create packer
    with pack.Packer(blend_file_path,
                     project_root_path,
                     target_dir_path,
                     noop=False,            # no-op mode, only shows what will be done
                     compress=False,
                     relative_only=False
                     ) as packer:

        log.info("Created packer")

        if progress_cb:
            log.info("Setting packer progress callback...")
            packer._progress_cb = progress_cb

        # plan the packing operation (must be called before execute)
        log.info("Plan packing operation...")
        packer.strategise()

        # attempt to pack the project
        try:
            log.info("Plan packing operation...")
            packer.execute()
        except pack.transfer.FileTransferError as ex:
            log.warning(str(len(ex.files_remaining)) + " files couldn't be copied, starting with " +
                        str(ex.files_remaining[0]))
            raise SystemExit(1)
        finally:
            log.info("Exiting packing operation...")


def validate_credentials(email = None, access_key = None):
    """Blender specific authentication validator, uses the gridmarkets validate_auth() function internally but adds
        additional checks and blender specific error messages.

    :param email: The user's GridMarkets account email, if None or not given then it will be read from the preferences
    :type email: str
    :param access_key: The user's GridMarkets access key, if None or not given then it will be read from the preferences
    :type access_key: str
    :return: true if credentials are valid
    :rtype: bool

    :raises: InvalidInputError, AuthenticationError
    """

    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Validating credentials...")

    # only read from preferences if a parameter is None
    if email is None or access_key is None:

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        if email is None:
            email = addon_prefs.auth_email

        if access_key is None:
            access_key = addon_prefs.auth_accessKey

    # check an email address has been entered
    has_email = isinstance(email, str) and len(email) > 0

    # check a auth key has been entered
    has_key = isinstance(access_key, str) and len(access_key) > 0

    # validate
    if not has_email and not has_key:
        message = "No " + constants.COMPANY_NAME + " email address or access key provided." + \
                  constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)
    elif not has_email:
        message = "No " + constants.COMPANY_NAME + " email address provided." + constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)
    elif not has_key:
        message = "No " + constants.COMPANY_NAME + " access key provided." + constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)

    # if initial checks pass try the client api validate_auth function
    # create an instance of Envoy client
    client = EnvoyClient(email=email, access_key=access_key)
    client.validate_auth()

    return True


def get_new_envoy_client():
    """ Gets a new EnvoyClient instance using the authentication preferences for credentials

    :return: The envoy client
    :rtype: gridmarkets.envoy_client.EnvoyClient

    :raises: InvalidInputError, AuthenticationError
    """

    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Getting new Envoy client....")

    # get the add-on preferences
    addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

    # validate the authentication credentials
    validate_credentials(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)

    # return the new client
    return EnvoyClient(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)


def get_envoy_client():
    """ Gets the existing EnvoyClient instance unless the authentication credentials have changed

    :return: The existing envoy client or a new one if the credentials have changed
    :rtype: gridmarkets.envoy_client.EnvoyClient

    :raises: InvalidInputError, AuthenticationError
    """
    global _envoy_client

    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Getting Envoy client....")

    if _envoy_client:

        log.info("Found existing Envoy client, comparing credentials...")

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        # check neither the email or access key have changed
        if addon_prefs.auth_email == _envoy_client.email and addon_prefs.auth_accessKey == _envoy_client.access_key:
            log.info("Returning existing Envoy client...")
            return  _envoy_client

    # update the client
    _envoy_client = get_new_envoy_client()

    return _envoy_client


def _add_project_to_list(project_name, props):

    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Starting add_project_to_list operation...")

    # if props already contains a project with the given name
    existing_projects_with_name = list(filter(lambda x: x.name == project_name, props.projects))

    if existing_projects_with_name:
        # don't add it to the list and return the existing project
        log.info("A project with the name %s already exists, returning existing project..." % project_name)
        return existing_projects_with_name[0]

    # add a project to the list
    log.info("Adding project to list...")

    project = props.projects.add()

    project.id = utils.get_unique_id(props.projects)
    project.name = project_name

    # select the new project
    log.info("Selecting new project...")
    props.selected_project = len(props.projects) - 1

    # force region to redraw otherwise the list wont update until next event (mouse over, etc)
    force_redraw_addon()

    return project


def get_project_status(project):
    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    try:
        # create an instance of Envoy client
        client = get_envoy_client()

        log.info("Getting project status for %s..." % project.name)
        resp = client.get_project_status(project.name)

        # convert to string
        project.status = json.dumps(resp)

        log.info("Project status response: %s" % project.status)

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


def clean_up_temporary_files(project_item, progress_callback):
    """ Checks the status of the project until it has finished uploading and then deletes the temporary files """

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    if not constants.PROJECT_STATUS_POLLING_ENABLED:
        log.info("Uploading Project...")
        return

    # number of times to retry if receiving malformed responses
    bad_response_retires = 10

    log.info("Uploading Project...")
    progress_callback(0, "Uploading Project")

    while bad_response_retires > 0:
        import time

        # sleep for 10 seconds to give time for the project to upload
        log.info("Checking project upload status in " + str(10) + " seconds")
        time.sleep(10)

        try:
            # create an instance of Envoy client
            client = get_envoy_client()

            log.info("Checking project status for %s..." % project_item.name)
            resp = client.get_project_status(project_item.name)

            # convert to string
            project_item.status = json.dumps(resp)
            log.info("Project status response: %s" % project_item.status)

            # redraw the add-on to show the latest update
            force_redraw_addon()
        except AuthenticationError as e:
            log.error("Authentication Error: " + e.user_message)
            bad_response_retires -= 1
            continue
        except InsufficientCreditsError as e:
            log.error("Insufficient Credits Error: " + e.user_message)
            bad_response_retires -= 1
            continue
        except InvalidRequestError as e:
            log.error("Invalid Request Error: " + e.user_message)
            bad_response_retires -= 1
            continue
        except APIError as e:
            log.error("API Error: " + str(e.user_message))
            bad_response_retires -= 1
            raise e
            continue

        # parse the json status response
        project_status = json.loads(project_item.status)
        uploading_status = project_status['State']

        if uploading_status == 'Completed' or uploading_status == 'Submitted':
            progress_callback(100, "Uploaded Project")
            log.info("Uploaded Project")
            break
        elif uploading_status == 'Uploading':
            if "BytesDone" in project_status and "BytesTotal" in project_status:
                bytes_done = project_status["BytesDone"]
                bytes_total = project_status["BytesTotal"]

                try:
                    # try converting to floats
                    bytes_done_f = float(bytes_done)
                    bytes_total_f = float(bytes_total)

                    # avoid dividing by zero errors
                    if bytes_total_f > 0:
                        percent = (bytes_done_f / bytes_total_f) * 100
                        progress_callback(percent, "Uploading Project...")

                except ValueError:
                    log.warning("bytes_done or bytes_total was not a float")
            continue
        elif uploading_status == 'Error':

            if 'Message' not in project_status:
                log.warning("Upload Error: No Error message")
                bad_response_retires -= 1
                continue

            error_message = project_status['Message']

            # the api returns an error status even if the project has uploaded correctly but it was uploaded without a
            # job, we need to check to make sure that this 'Error' isn't just a uploaded project without a job
            if error_message == "Job validation failed.":

                # check that all the details have finished uploading
                if 'Details' not in project_status:
                    log.warning("Project status does not contain 'Details' attribute")
                else:
                    details = project_status['Details']

                    details_uploaded = True

                    for key, value in details.items():

                        # the Details attribute can contain it's own details attribute which we should ignore
                        if key == 'details':
                            continue

                        if 'BytesDone' not in value:
                            log.warning("project status detail does not contain 'BytesDone' attribute")
                            details_uploaded = False
                            break

                        if 'BytesTotal' not in value:
                            log.warning("project status detail does not contain 'Bytestotal' attribute")
                            details_uploaded = False
                            break

                        bytes_done = value['BytesDone']
                        bytes_total = value['BytesTotal']

                        # if the detail is not finished uploading then break
                        if bytes_done != bytes_total:
                            log.warning("project status detail %s does has not finished uploading" % key)
                            details_uploaded = False
                            break

                    if details_uploaded:
                        progress_callback(100, "Uploaded Project")
                        log.info("Uploaded Project")
                        break
                    else:
                        log.warning("Not all details have been uploaded")

            else:
                log.warning("Upload Error: %s" % error_message)
                bad_response_retires -= 1
                continue

        else:
            log.warning("Unrecognised status: %s" % uploading_status)
            bad_response_retires -= 1
            continue

    delete_temp_files_for_project(project_item.name)


def delete_temp_files_for_project(project_name):
    """ Attempts to delete the temporary project files for associated with a given project name

    :param project_name: The name of the project
    :type project_name: str
    :rtype: void
    """

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])
    log.info("Starting delete_temp_files_for_project operation")

    # get the temporary directory manager
    temporary_directory_manager = TempDirectoryManager.get_temp_directory_manager()

    # find the association for this project
    association = temporary_directory_manager.get_association_with_project_name(project_name)

    # if the association exists
    if association:
        log.info("Found association")

        # delete the temporary files for the project
        association.delete_temporary_directory()
    else:
        log.info("Project association does not exist")

def _scale_percentage(min_percentage, max_percentage, percentage):
    return min_percentage + ((max_percentage - min_percentage) / 100) * percentage


def upload_file_as_project(context, file_path, project_name, temp_dir_manager,
                   operator=None,
                   skip_upload=False,
                   min_progress=0,
                   max_progress=100,
                   progress_attribute_name = "uploading_project",
                   progress_percent_attribute_name = "uploading_project_progress",
                   progress_status_attribute_name = "uploading_project_status"
                   ):
    """Uploads the provided .blend file to Envoy as a new project, using the provided project name.

    :param context: The operator's context
    :type context: bpy.types.Context
    :param file_path: The path to the blend file that needs uploading
    :type file_path: str
    :param project_name: The name of the project as it will appear in Envoy
    :type project_name: str
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :param operator: The operator that called the function
    :type operator: bpy.types.Operator
    :param skip_upload: Pack files but don't upload project files
    :param operator: An optional instance of an operator so that invalid input can be reported correctly
    :type operator: bpy.types.Operator
    :param min_progress: The min value to set the progress too
    :type min_progress: float
    :param max_progress: The max value to set the progress too
    :type max_progress: float
    :param progress_attribute_name: The name of the property flag which indicated that the operation is running
    :type progress_attribute_name: str
    :param progress_percent_attribute_name: The name of the property which represents the operations progress
    :type progress_percent_attribute_name: str
    :param progress_status_attribute_name: The name of the property which represents the operations status
    :type progress_status_attribute_name: str
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    # helper function for setting the progress of the operation
    def _set_progress(progress=None, status=None):
        if progress is not None:
            # re-scale progress so that it is between the min and max values
            scaled_progress =_scale_percentage(min_progress, max_progress, progress)
            setattr(context.scene.props, progress_percent_attribute_name, scaled_progress)

        if status is not None:
            setattr(context.scene.props, progress_status_attribute_name, status)

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    setattr(context.scene.props, progress_attribute_name, True)
    _set_progress(progress=0, status="Starting project upload")

    try:
        # create an instance of Envoy client
        client = get_envoy_client()

        # create a new temp directory
        temp_dir_path = temp_dir_manager.get_temp_directory()

        # create directory to contain packed project
        packed_dir = temp_dir_path / project_name

        log.info("Creating packed directory '%s'..." % str(packed_dir))
        _set_progress(progress=40, status="Creating packed directory")
        os.mkdir(str(packed_dir))

        from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
        blender_scene_exporter = BlenderSceneExporter()
        blender_scene_exporter.export(packed_dir)

        """
        # create the progress callback
        progress_cb = BatProgressCallback(log)

        # pack the .blend file to the pack directory
        _set_progress(progress=60, status="Packing scene data")
        pack_blend_file(file_path, str(packed_dir), progress_cb=progress_cb)

        # delete pack-info.txt if it exists
        pack_info_file = pathlib.Path(packed_dir / 'pack-info.txt')
        if pack_info_file.is_file():
            log.info("Removing '%s'..." % str(pack_info_file))
            pack_info_file.unlink()
        """

        # create the project
        project = Project(str(packed_dir), project_name)

        # associate this project with the temp directory so the temp directory can be removed once the project is
        # complete
        temp_dir_manager.associate_with_temp_dir(str(temp_dir_path), project, pathlib.Path(file_path).name)
        # add files to project
        # only files and folders within the project path can be added, use relative or full path
        # any other paths passed will be ignored
        log.info("Adding '" + str(packed_dir) + "' to " + constants.COMPANY_NAME + " project...")
        project.add_folders(str(packed_dir))

        if skip_upload:
            log.info("Skipping project upload...")
        else:
            client.submit_project(project)  # returns project name

            # add the new project to the projects list
            project_item = _add_project_to_list(project_name, context.scene.props)

            # callback for keeping track of the upload progress
            def progress_callback(percent, status):
                scaled_percent = 80 + percent / (100 / (100 - 80))
                _set_progress(progress=scaled_percent, status=status)

            clean_up_temporary_files(project_item, progress_callback)

    except InvalidInputError as e:
        log.warning("Invalid Input Error: " + e.user_message)
        if operator:
            operator.report({'ERROR_INVALID_INPUT'}, e.user_message)
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
    finally:
        # hide the progress meter if unless skipping upload
        if not skip_upload:
            setattr(context.scene.props, progress_attribute_name, False)


def get_blend_file_name():
    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    # if the file has been saved
    if bpy.context.blend_data.is_saved:
        # use the name of the saved .blend file
        blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
        log.info(".blend file is saved, using '%s' as packed file name." % blend_file_name)
    else:
        # otherwise create a name for the packed .blend file
        blend_file_name = 'main_GM_blend_file_packed.blend'
        log.info(".blend file is not saved, using '%s' as packed file name." % blend_file_name)

    return blend_file_name


def upload_project(context, project_name, temp_dir_manager,
                   operator=None,
                   skip_upload=False,
                   min_progress=0,
                   max_progress=100,
                   progress_attribute_name = "uploading_project",
                   progress_percent_attribute_name = "uploading_project_progress",
                   progress_status_attribute_name = "uploading_project_status"
                   ):
    """Uploads the current scene with the provided project name to Envoy.

    :param context: The operator's context
    :type context: bpy.types.Context
    :param project_name: The name of the project as it will appear in Envoy
    :type project_name: str
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :param operator: The operator that called the function
    :type operator: bpy.types.Operator
    :param skip_upload: Pack files but don't upload project files
    :param operator: An optional instance of an operator so that invalid input can be reported correctly
    :type operator: bpy.types.Operator
    :param min_progress: The min value to set the progress too
    :type min_progress: float
    :param max_progress: The max value to set the progress too
    :type max_progress: float
    :param progress_attribute_name: The name of the property flag which indicated that the operation is running
    :type progress_attribute_name: str
    :param progress_percent_attribute_name: The name of the property which represents the operations progress
    :type progress_percent_attribute_name: str
    :param progress_status_attribute_name: The name of the property which represents the operations status
    :type progress_status_attribute_name: str
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    # helper function for setting the progress of the operation
    def _set_progress(progress=None, status=None):
        if progress is not None:
            # re-scale progress so that it is between the min and max values
            scaled_progress = _scale_percentage(min_progress, max_progress, progress)
            setattr(context.scene.props, progress_percent_attribute_name, scaled_progress)

        if status is not None:
            setattr(context.scene.props, progress_status_attribute_name, status)

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    setattr(context.scene.props, progress_attribute_name, True)
    _set_progress(progress=0, status="Starting project upload")

    blend_file_name = get_blend_file_name()

    # create a new temp directory
    temp_dir_path = temp_dir_manager.get_temp_directory()

    blend_file_path = temp_dir_path / blend_file_name

    # save a copy of the current scene to the temp directory. This is so that if the file has not been saved
    # or if it has been modified since it's last save then the submitted .blend file will represent the
    # current state of the scene
    _set_progress(progress=20, status="Saving scene data")
    bpy.ops.wm.save_as_mainfile(copy=True, filepath=str(blend_file_path), relative_remap=True,
                                compress=True)
    log.info("Saved copy of scene to '%s'" % str(blend_file_path))

    upload_file_as_project(context,str(blend_file_path), project_name, temp_dir_manager,
                           operator,
                           skip_upload,
                           _scale_percentage(min_progress, max_progress, 20),
                           max_progress,
                           progress_attribute_name,
                           progress_percent_attribute_name,
                           progress_status_attribute_name)


def get_blender_frame_range(context):
    scene = context.scene
    return str(scene.frame_start) + ' ' + str(scene.frame_end) + ' ' + str(scene.frame_step)


def get_default_blender_job(context, render_file):
    scene = context.scene

    return Job(
        "Default Blender Job",                                      # JOB_NAME
        constants.JOB_PRODUCT_TYPE,                                 # PRODUCT_TYPE
        constants.JOB_PRODUCT_VERSION,                              # PRODUCT_VERSION
        constants.JOB_OPERATION,                                    # OPERATION
        render_file,                                                # RENDER_FILE
        frames = get_blender_frame_range(context),                  # FRAMES
        output_prefix = None,                                       # OUTPUT_PREFIX
        output_format = scene.render.image_settings.file_format,    # OUTPUT_FORMAT
        engine = scene.render.engine,                               # RENDER_ENGINE
    )


def get_job_output_path(context, job=None):
    """ Gets the output path for either the provided job or the currently selested job if no job provided

    :param context: The context
    :type context: bpy.context
    :param job: The job to get the output path for (optional)
    :type job: properties.JobProps
    :return: The output path as it is entered in either the blender ui or custom output field
    :rtype: str
    """

    scene = context.scene
    props = scene.props

    if job is None:
        # if no job is selected return the blender frame range
        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            return context.scene.render.filepath

        # otherwise use the selected job
        job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]

    if job.use_custom_output_path:
        return job.output_path

    return context.scene.render.filepath


def get_job_output_path_abs(context, job=None):
    path = get_job_output_path(context, job)

    # check if the path is relative
    if path.startswith("//"):

        # remove the relative double slash
        path = path[2:]

        if bpy.context.blend_data.is_saved:
            return str(pathlib.Path(bpy.context.blend_data.filepath).parent / pathlib.Path(path))
        else:
            # if they are using a relative path with an unsaved project just output to tmp
            return constants.BLENDER_TEMP_DIRECTORY

    return path


def get_job_frame_ranges(context, job=None):
    scene = context.scene
    props = scene.props

    if job is None:
        # if no job is selected return the blender frame range
        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            return get_blender_frame_range(context)
        else:
            # otherwise use the selected job
            job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]

    # use scene frame settings unless the user has overridden them
    if job.use_custom_frame_ranges:

        # filter disabled frame ranges
        frame_ranges = filter(lambda frame_range: frame_range.enabled, job.frame_ranges)

        # join the frame_start, frame_end and frame_step properties
        frame_ranges = map(lambda r: ' '.join([str(r.frame_start), str(r.frame_end), str(r.frame_step)]),
                           frame_ranges)

        # join all frame ranges together
        return ','.join(frame_ranges)

    else:
        return get_blender_frame_range(context)


def do_frame_ranges_overlap(job):
    """ Detects if the job has overlapping frame ranges, returns false if use_custom_frame_ranges is false.

    :param job: The job to check
    :type job: property_groups.job_props.JobProps
    :return: True if frame ranges overlap, otherwise false
    :rtype: bool
    """

    if not job.use_custom_frame_ranges:
        return False

    # buffer to store frames already seen
    frames_buffer = []

    for frame_range in job.frame_ranges:
        start = frame_range.frame_start
        end = frame_range.frame_end
        step = frame_range.frame_step

        # add all frames in range to frames buffer
        i = start
        while i <= end:

            if i in frames_buffer:
                return True

            frames_buffer.append(i)
            i = i + step

    return False


def get_job_render_engine(context, job=None):
    scene = context.scene
    props = scene.props

    if job is None:
        # if no job is selected return the blender frame range
        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            return scene.render.engine
        else:
            # otherwise use the selected job
            job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]

    # use scene frame settings unless the user has overridden them
    if job.use_custom_render_engine:
        return job.render_engine

    else:
        return scene.render.engine


def get_supported_render_engines():
    return {"CYCLES", "VRAY_RENDER_RT"}


def get_user_friendly_name_for_engine(engine: str):
    if engine == "CYCLES":
        return "Cycles"
    elif engine == "BLENDER_EEVEE":
        return "Eevee"
    elif engine == "BLENDER_RENDER":
        return "Blender Internal"
    elif engine == "BLENDER_WORKBENCH":
        return "Blender Workbench"
    elif engine == "VRAY_RENDER_RT":
        return "V-Ray"
    else:
        # if not know just return the enum name for it
        return engine


def get_supported_products(scene, context):
    from gridmarkets_blender_addon.api_constants import PRODUCTS

    return [
        (PRODUCTS.BLENDER, "Blender", ""),
        (PRODUCTS.VRAY, "V-Ray", ""),
    ]


def get_supported_blender_versions(scene, context):
    from gridmarkets_blender_addon.api_constants import BLENDER_VERSIONS

    return [
        (BLENDER_VERSIONS.V_2_80, "2.80", ""),
        (BLENDER_VERSIONS.V_2_79, "2.79", ""),
    ]


def get_supported_blender_279_engines(scene, context):
    from gridmarkets_blender_addon.api_constants import BLENDER_ENGINES

    return [
        (BLENDER_ENGINES.CYCLES, "Cycles", ""),
        (BLENDER_ENGINES.INTERNAL, "Internal", ""),
    ]


def get_supported_blender_280_engines(scene, context):
    from gridmarkets_blender_addon.api_constants import BLENDER_ENGINES

    return [
        (BLENDER_ENGINES.CYCLES, "Cycles", ""),
        (BLENDER_ENGINES.EEVEE, "Eevee", ""),
    ]

def get_supported_vray_versions(scene, context):
    from gridmarkets_blender_addon.api_constants import VRAY_VERSIONS

    return [
        (VRAY_VERSIONS.V_3_60_03, "3.60.03", ""),
        (VRAY_VERSIONS.V_3_60_04, "3.60.04", ""),
        (VRAY_VERSIONS.V_3_60_05, "3.60.05", ""),
        (VRAY_VERSIONS.V_4_02_05, "4.02.05", ""),
        (VRAY_VERSIONS.V_4_10_01, "4.10.01", ""),
        (VRAY_VERSIONS.V_4_10_02, "4.10.02", ""),
    ]


def get_job_output_format(context, job=None):
    scene = context.scene
    props = scene.props

    if job is None:
        # if no job is selected return the blender frame range
        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            return scene.render.image_settings.file_format
        else:
            # otherwise use the selected job
            job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]

    # use scene frame settings unless the user has overridden them
    if job.use_custom_output_format:
        return job.output_format

    else:
        return scene.render.image_settings.file_format


def get_job_output_prefix(context, job=None):
    scene = context.scene
    props = scene.props

    if job is None:
        # if no job is selected return the blender frame range
        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            return None
        else:
            # otherwise use the selected job
            job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]

    # use scene frame settings unless the user has overridden them
    if job.use_custom_output_prefix:

        # check if the output prefix has been entered
        if not isinstance(job.output_prefix, str):
            return None

        return job.output_prefix

    return None


def get_job(context, render_file, enable_logging=True):
    scene = context.scene
    props = scene.props

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    if enable_logging:
        log.info("Getting job settings...")

    # if the job options are set to 'use blender render settings' then set the job options accordingly
    if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
        if enable_logging:
            log.info("Using default blender render settings")
        job = get_default_blender_job(context, render_file)

    # otherwise set the job options based on a user defined job
    elif props.job_options.isnumeric():
        if enable_logging:
            log.info("Using custom job")

        selected_job_option = int(props.job_options)
        selected_job = props.jobs[selected_job_option - constants.JOB_OPTIONS_STATIC_COUNT]

        job = Job(
            selected_job.name,
            constants.JOB_PRODUCT_TYPE,
            constants.JOB_PRODUCT_VERSION,
            constants.JOB_OPERATION,
            render_file,
            frames=get_job_frame_ranges(context, job=selected_job),
            output_prefix=get_job_output_prefix(context, job=selected_job),
            output_format=get_job_output_format(context, job=selected_job),
            engine=get_job_render_engine(context, job=selected_job),
            gpu=selected_job.render_device == constants.RENDER_DEVICE_GPU
        )
    else:
        raise InvalidInputError(message="Invalid job option")

    return job


def get_version_string():
    return 'GM Blender Add-on v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(
        constants.PLUGIN_VERSION['minor']) + '.' + str(constants.PLUGIN_VERSION['build'])


def submit_job(context, temp_dir_manager,
               new_project_name=None,
               operator=None,
               min_progress=0,
               max_progress=100,
               progress_attribute_name="submitting_project",
               progress_percent_attribute_name="submitting_project_progress",
               progress_status_attribute_name="submitting_project_status"
               ):
    """Submits a job to a existing or new project.

    :param context: Depends on the area of Blender which is currently being accessed
    :type context: bpy.context
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :param new_project_name: The name of the project to use if uploading a new project
    :type new_project_name: str
    :param operator: An optional instance of an operator so that invalid input can be reported correctly
    :type operator: bpy.types.Operator
    :param min_progress: The min value to set the progress too
    :type min_progress: float
    :param max_progress: The max value to set the progress too
    :type max_progress: float
    :param progress_attribute_name: The name of the property flag which indicated that the operation is running
    :type progress_attribute_name: str
    :param progress_percent_attribute_name: The name of the property which represents the operations progress
    :type progress_percent_attribute_name: str
    :param progress_status_attribute_name: The name of the property which represents the operations status
    :type progress_status_attribute_name: str
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    scene = context.scene
    props = scene.props

    # get method logger
    log = get_wrapped_logger(__name__ + '.' + inspect.stack()[0][3])

    # define a helper function for setting the progress
    def _set_progress(progress=None, status=None):
        if progress is not None:
            # re-scale progress so that it is between the min and max values
            scaled_progress = min_progress + ((max_progress - min_progress) / 100) * progress
            setattr(context.scene.props, progress_percent_attribute_name, scaled_progress)

        if status is not None:
            setattr(context.scene.props, progress_status_attribute_name, status)

    # set the submitting flag to true
    setattr(context.scene.props, progress_attribute_name, True)

    # set the progress to 0 and set a status message
    _set_progress(progress=0, status="Starting job submission")

    # log the start of the operation
    log.info("Starting submit operation...")

    try:
        # if the user has selected to upload the current scene as a new project then upload current scene as new project
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            log.info("Uploading project for job submit...")
            _set_progress(progress=10, status="Uploading project")

            if new_project_name is None:
                raise InvalidInputError("Project name can not be None type")

            project_name = new_project_name

            # upload the project
            upload_project(context, project_name, temp_dir_manager,
                           operator=operator,
                           min_progress=10,
                           max_progress=40,
                           progress_attribute_name=progress_attribute_name,
                           progress_percent_attribute_name=progress_percent_attribute_name,
                           progress_status_attribute_name=progress_status_attribute_name,
                           # skip upload here otherwise when we submit this job the project may not have finished
                           # uploading. Instead use upload project to pack the files and upload when the job is
                           # submitted
                           skip_upload=True)

            skip_upload = False

        elif props.project_options.isnumeric():
            log.info("Project already uploaded, submitting job...")
            # get the name of the selected project
            selected_project_option = int(props.project_options)
            selected_project = props.projects[selected_project_option - constants.PROJECT_OPTIONS_STATIC_COUNT]
            project_name = selected_project.name
            skip_upload = True
        else:
            raise InvalidInputError(message="Invalid project option")

        association = temp_dir_manager.get_association_with_project_name(project_name)
        project = association.get_project()
        render_file = association.get_relative_render_file()

        job = get_job(context, render_file)

        # create an instance of Envoy client
        client = get_envoy_client()

        # remove all previously run jobs
        project.jobs = list()

        # add job to project
        project.add_jobs(job)

        # results regex pattern to download
        # `project.remote_output_folder` provides the remote root folder under which results are available
        # below is the regex to look for all folders and files under `project.remote_output_folder`
        output_pattern = '{0}/.+'.format(project.remote_output_folder)

        download_path = get_job_output_path_abs(context)

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
        log.info("Submitting job (skip_upload=" + str(skip_upload) + ")...")
        _set_progress(progress=50, status="Submitting project")
        client.submit_project(project, skip_upload=skip_upload)

        # skip upload is only false if its a new project, in which case it needs adding to the list
        if not skip_upload:
            project_item = _add_project_to_list(project_name, props)

            # callback for keeping track of the upload progress
            def progress_callback(percent, status):
                scaled_percent = 50 + percent / 2
                _set_progress(progress=scaled_percent, status=status)

            clean_up_temporary_files(project_item, progress_callback)

        log.info("Job submitted")


    except InvalidInputError as e:
        log.warning("Invalid Input Error: " + e.user_message)
        if operator:
            operator.report({'ERROR_INVALID_INPUT'}, e.user_message)
    except AuthenticationError as e:
        log.error("Authentication Error: " + e.user_message)
    except InsufficientCreditsError as e:
        log.error("Insufficient Credits Error: " + e.user_message)
    except InvalidRequestError as e:
        log.error("Invalid Request Error: " + e.user_message)
    except APIError as e:
        log.error("API Error: " + str(e.user_message))
    finally:
        log.info("Finished submit operation")
        setattr(context.scene.props, progress_attribute_name, False)


def get_addon(module_name):
    """ Gets a blender add-on

    :param module_name: The name of the add-on
    :type module_name: str
    :return: The add-on or None if the add-on could not be found
    :rtype: (bpy.types.Addon, module_bl_info)
    """

    for module in addon_utils.modules(refresh=False):
        info = addon_utils.module_bl_info(module)

        if 'name' in info:
            name = info['name']

            if name == module_name:
                return module, info

    return None

def force_redraw_addon():
    #redraw_region(constants.WINDOW_SPACE_TYPE, constants.PANEL_REGION_TYPE)
    redraw_area(constants.WINDOW_SPACE_TYPE)

def redraw_area(area_type):
    # the screen may be None if method is called from a different thread
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            if area.type == area_type:
                area.tag_redraw()


def redraw_region(area_type, region_type):
    # the screen may be None if method is called from a different thread
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            if area.type == area_type:
                for region in area.regions:
                    if region.type == region_type:
                        region.tag_redraw()


def get_addon_window():
    for window in bpy.context.window_manager.windows:
        if window.screen.name == constants.INJECTED_SCREEN_NAME:
            return window
    return None


def addon_draw_condition(self, context):
    return context.screen.name == constants.INJECTED_SCREEN_NAME

def get_spinner(index: int):
    from gridmarkets_blender_addon.icon_loader import IconLoader
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]

    if index == 0:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_0_ID]
    elif index == 1:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_1_ID]
    elif index == 2:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_2_ID]
    elif index == 3:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_3_ID]
    elif index == 4:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_4_ID]
    elif index == 5:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_5_ID]
    elif index == 6:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_6_ID]
    else:
        return preview_collection[constants.CUSTOM_SPINNER_ICON_7_ID]

def get_logs(self, context):
    props = context.scene.props
    output = ''

    def _get_log_text(item):
        """ Converts a log item into a textual representation """
        text = ''

        if item.date:
            text = text + item.date + ' '

        if item.time:
            text = text + item.time + ' '

        if item.name:
            text = text + item.name + ' ' + item.level + ' '

        text = text + item.body

        return text

    for log_item in props.log_items:
        output = output + os.linesep + _get_log_text(log_item)

    return get_sys_info() + os.linesep + output


def is_addon_enabled(addon_name: str):
    is_enabled, is_loaded = addon_utils.check(addon_name)
    return is_enabled and is_loaded


def get_sys_info():
    import platform

    blender_version = bpy.app.version
    addon_version = constants.PLUGIN_VERSION

    sys_info = "Operating System: " + platform.platform() + os.linesep
    sys_info = sys_info + "Blender Version: " + str(blender_version[0]) + '.' + str(blender_version[1]) + '.' + \
               str(blender_version[2]) + os.linesep
    sys_info = sys_info + "Add-on Version: " + str(addon_version["major"]) + '.' + str(addon_version["minor"]) + \
               '.' + str(addon_version["build"]) + os.linesep

    return sys_info


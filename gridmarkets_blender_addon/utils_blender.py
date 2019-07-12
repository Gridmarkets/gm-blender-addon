import bpy
import inspect
import pathlib
import os
import collections
import json
import math

import constants
import utils

from invalid_input_error import InvalidInputError
from temp_directory_manager import TempDirectoryManager
from bat_progress_callback import BatProgressCallback

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

from blender_asset_tracer import trace, pack

# global client to reuse
_envoy_client = None


def get_wrapped_logger(name):
    from blender_logging_wrapper import get_wrapped_logger
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

    blend_file_path = pathlib.Path(blend_file_path)
    project_root_path = blend_file_path.parent
    target_dir_path = pathlib.Path(target_dir_path)

    # create packer
    with pack.Packer(blend_file_path,
                     project_root_path,
                     target_dir_path,
                     noop=False,            # no-op mode, only shows what will be done
                     compress=False,
                     relative_only=False
                     ) as packer:

        if progress_cb:
            packer._progress_cb = progress_cb

        # plan the packing operation (must be called before execute)
        packer.strategise()

        # attempt to pack the project
        try:
            packer.execute()
        except pack.transfer.FileTransferError as ex:
            print("%d files couldn't be copied, starting with %s",
                  len(ex.files_remaining), ex.files_remaining[0])
            raise SystemExit(1)


def validate_credentials(email = None, access_key = None):
    """Blender specific authentication validator, uses the gridmarkets validate_auth() function internally but adds
        additional checks and blender specific error messages.

    :param email: The user's Gridmarkets account email, if None or not given then it will be read from the preferences
    :type email: str
    :param access_key: The user's Gridmarkets access key, if None or not given then it will be read from the preferences
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
        message = "No Gridmarkets email address or access key provided." + constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)
    elif not has_email:
        message = "No Gridmarketes email address provided." + constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)
    elif not has_key:
        message = "No Gridmarketes access key provided." + constants.AUTHENTICATION_HELP_MESSAGE
        raise InvalidInputError(message=message)

    # if initial checks pass try the Gridmarkets validate_auth function
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

    if _envoy_client:

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        # check neither the email or access key have changed
        if addon_prefs.auth_email == _envoy_client.email and addon_prefs.auth_accessKey == _envoy_client.access_key:
            return  _envoy_client

    # update the client
    _envoy_client = get_new_envoy_client()

    return _envoy_client


def _add_project_to_list(project_name, props):

    # add a project to the list
    project = props.projects.add()

    project.id = utils.get_unique_id(props.projects)
    project.name = project_name

    # select the new project
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
            continue

        # parse the json status response
        project_status = json.loads(project_item.status)
        uploading_status = project_status['State']

        if uploading_status == 'Completed':
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
        else:
            log.warning("Uploading status was something other than 'Completed' or 'Uploading'")
            bad_response_retires -= 1
            continue

    delete_temp_files_for_project(project_item.name)


def delete_temp_files_for_project(project_name):
    """ Attempts to delete the temporary project files for associated with a given project name

    :param project_name: The name of the project
    :type project_name: str
    :rtype: void
    """

    # get the temporary directory manager
    temporary_directory_manager = TempDirectoryManager.get_temp_directory_manager()

    # find the association for this project
    association = temporary_directory_manager.get_association_with_project_name(project_name)

    # if the association exists
    if association:

        # delete the temporary files for the project
        association.delete_temporary_directory()


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
            scaled_progress = min_progress + ((max_progress - min_progress) / 100) * progress
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

        # if the file has been saved
        if bpy.context.blend_data.is_saved:
            # use the name of the saved .blend file
            blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
            log.info(".blend file is saved, using '%s' as packed file name." % blend_file_name)
        else:
            # otherwise create a name for the packed .blend file
            blend_file_name = 'main_GM_blend_file_packed.blend'
            log.info(".blend file is not saved, using '%s' as packed file name." % blend_file_name)

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

        # create directory to contain packed project
        packed_dir = temp_dir_path / project_name

        log.info("Creating packed directory '%s'..." % str(packed_dir))
        _set_progress(progress=40, status="Creating packed directory")
        os.mkdir(str(packed_dir))

        # create the progress callback
        progress_cb = BatProgressCallback(log)

        # pack the .blend file to the pack directory
        _set_progress(progress=60, status="Packing scene data")
        pack_blend_file(str(blend_file_path), str(packed_dir), progress_cb=progress_cb)

        # delete pack-info.txt if it exists
        pack_info_file = pathlib.Path(packed_dir / 'pack-info.txt')
        if pack_info_file.is_file():
            log.info("Removing '%s'..." % str(pack_info_file))
            pack_info_file.unlink()

        # create the project
        project = Project(str(packed_dir), project_name)

        # associate this project with the temp directory so the temp directory can be removed once the project is
        # complete
        temp_dir_manager.associate_with_temp_dir(str(temp_dir_path), project, blend_file_name)
        # add files to project
        # only files and folders within the project path can be added, use relative or full path
        # any other paths passed will be ignored
        log.info("Adding '%s' to Gridmarkets project..." % str(packed_dir))
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
        output_prefix = "0",                                        # OUTPUT_PREFIX
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


def get_job_output_prefix(job):
    # check if the output prefix has been entered
    if not isinstance(job.output_prefix, str) or len(job.output_prefix) <= 0:
        # the Blender job submission API requires an output prefix but an if it's an empty string envoy wont auto
        # download the results.
        return "0"

    return job.output_prefix


def get_job(context, render_file):
    scene = context.scene
    props = scene.props

    # if the job options are set to 'use blender render settings' then set the job options accordingly
    if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
        job = get_default_blender_job(context, render_file)

    # otherwise set the job options based on a user defined job
    elif props.job_options.isnumeric():
        selected_job_option = int(props.job_options)
        selected_job = props.jobs[selected_job_option - constants.JOB_OPTIONS_STATIC_COUNT]

        job = Job(
            selected_job.name,
            constants.JOB_PRODUCT_TYPE,
            constants.JOB_PRODUCT_VERSION,
            constants.JOB_OPERATION,
            render_file,
            frames=get_job_frame_ranges(context, job=selected_job),
            output_prefix=get_job_output_prefix(selected_job),
            output_format=get_job_output_format(context, job=selected_job),
            engine=get_job_render_engine(context, job=selected_job)
        )
    else:
        raise InvalidInputError(message="Invalid job option")

    return job


def get_version_string():
    return 'GM Blender Add-on Beta v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(
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
        log.info("Submitting job...")
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
        setattr(context.scene.props, progress_attribute_name, False)


def get_addon(module_name):
    """ Gets a blender add-on

    :param module_name: The name of the add-on
    :type module_name: str
    :return: The add-on or None if the add-on could not be found
    :rtype: (bpy.types.Addon, module_bl_info)
    """

    # noinspection PyUnresolvedReferences
    import addon_utils

    for module in addon_utils.modules(refresh=False):
        info = addon_utils.module_bl_info(module)

        if 'name' in info:
            name = info['name']

            if name == module_name:
                return module, info

    return None

def force_redraw_addon():
    redraw_region(constants.WINDOW_SPACE_TYPE, constants.PANEL_REGION_TYPE)


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

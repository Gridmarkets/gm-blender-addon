import bpy
import pathlib
import os


import constants
import utils

from invalid_input_error import InvalidInputError
from property_sanitizer import PropertySanitizer
from temp_directory_manager import TempDirectoryManager
from validation_response import ValidationResponse

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

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
        raise InvalidInputError(message="No Gridmarkets email address or access key provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)
    elif not has_email:
        raise InvalidInputError(message="No Gridmarketes email address provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)
    elif not has_key:
        raise InvalidInputError(message="No Gridmarketes access key provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)

    # if initial checks pass try the Gridmarkets validate_auth function
    # create an instance of Envoy client
    client = EnvoyClient(email=email, access_key=access_key)
    client.validate_auth()

    return True


def get_new_envoy_client():
    """ Gets a new EnvoyClient instance using the authentication preferences for credentials

    :return: The envoy client
    :rtype: EnvoyClient

    :raises: InvalidInputError, AuthenticationError
    """

    # get the add-on preferences
    addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

    # validate the authentication credentials
    validate_credentials(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)

    # return the new client
    return EnvoyClient(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)


def upload_project(project_name, temp_dir_manager):
    """ Uploads the current scene with the provided project name to Envoy.

    :param project_name: The name of the project as it will appear in Envoy
    :type project_name: str
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    # create an instance of Envoy client
    client = get_new_envoy_client()

    blend_file_name = None

    # if the file has been saved
    if bpy.context.blend_data.is_saved:
        # use the name of the saved .blend file
        blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
    else:
        # otherwise create a name for the packed .blend file
        blend_file_name = 'main_GM_blend_file_packed.blend'

    # create a new temp directory
    temp_dir_path = temp_dir_manager.get_temp_directory()

    blend_file_path = temp_dir_path / blend_file_name

    # save a copy of the current scene to the temp directory. This is so that if the file has not been saved
    # or if it has been modified since it's last save then the submitted .blend file will represent the
    # current state of the scene
    bpy.ops.wm.save_as_mainfile(copy=True, filepath=str(blend_file_path), relative_remap=True,
                                compress=True)

    # create directory to contain packed project
    packed_dir = temp_dir_path / project_name
    os.mkdir(str(packed_dir))

    # pack the .blend file to the pack directory
    utils.pack_blend_file(str(blend_file_path), str(packed_dir))

    # delete pack-info.txt if it exists
    pack_info_file = pathlib.Path(packed_dir / 'pack-info.txt')
    if pack_info_file.is_file():
        pack_info_file.unlink()

    # create the project
    project = Project(str(packed_dir), project_name)

    # associate this project with the temp directory so the temp directory can be removed once the project is
    # complete
    temp_dir_manager.associate_with_temp_dir(str(temp_dir_path), project, blend_file_name)

    # add files to project
    # only files and folders within the project path can be added, use relative or full path
    # any other paths passed will be ignored
    project.add_folders(str(packed_dir))

    # submit project
    resp = client.submit_project(project)  # returns project name


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


def get_job_frame_ranges(context, job):
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


def get_job_output_prefix(job):
    # check if the output prefix has been entered
    if not isinstance(job.output_prefix, str) or len(job.output_prefix) <= 0:
        # the Blender job submission API requires an output prefix but an if it's an empty string envoy wont auto
        # download the results.
        return "0"

    return job.outputPrefix


def submit_job(context, temp_dir_manager):
    """ Submits a job to a existing or new project.

    :param context: Depends on the area of Blender which is currently being accessed
    :type context: bpy.context
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    scene = context.scene
    props = scene.props

    # if the user has selected to upload the current scene as a new project then upload current scene as new project
    if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
        # create a name for the project
        project_name = utils.create_unique_object_name(props.projects, name_prefix='unnamed_project_')

        # upload the project
        upload_project(project_name, temp_dir_manager)

        # update the ui options list
        add_project_to_options_list(context, project_name)

    elif props.project_options.isnumeric():
        # get the name of the selected project
        selected_project_option = int(props.project_options)
        selected_project = props.projects[selected_project_option - constants.PROJECT_OPTIONS_STATIC_COUNT]
        project_name = selected_project.name
    else:
        raise InvalidInputError(message="Invalid project option")

    association = temp_dir_manager.get_association_with_project_name(project_name)
    project = association.get_project()
    render_file = association.get_relative_render_file()

    if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
        job = get_default_blender_job(context, render_file)

    elif props.job_options.isnumeric():
        selected_job_option = int(props.job_options)
        selected_job = props.jobs[selected_job_option - constants.JOB_OPTIONS_STATIC_COUNT]

        job = Job(
            selected_job.name,
            constants.JOB_PRODUCT_TYPE,
            constants.JOB_PRODUCT_VERSION,
            constants.JOB_OPERATION,
            render_file,
            frames=get_job_frame_ranges(context, selected_job),
            output_prefix=get_job_output_prefix(selected_job),
            output_format=scene.render.image_settings.file_format,
            engine=scene.render.engine
        )
    else:
        raise InvalidInputError(message="Invalid job option")

    # create an instance of Envoy client
    client = get_new_envoy_client()

    # add job to project
    project.add_jobs(job)


    print('project_name:', project_name)
    print('job.name:', job.name)
    print('job.app:', job.app)
    print('job.app_version:', job.app_version)
    print('job.operation:', job.operation)
    print('job.path:', job.path)
    print('job.frames:', get_blender_frame_range(context))

    # submit project
    client.submit_project(project, skip_upload=True)


def add_project_to_options_list(context, project_name):
    props = context.scene.props

    # add a project to the list
    project = props.projects.add()

    project.id = utils.get_unique_id(props.projects)
    project.name = project_name

    # select the new project
    props.selected_project = len(props.projects) - 1

    # force region to redraw otherwise the list wont update until next event (mouse over, etc)
    for area in bpy.context.screen.areas:
        if area.type == constants.PANEL_SPACE_TYPE:
            for region in area.regions:
                if region.type == constants.PANEL_REGION_TYPE:
                    region.tag_redraw()
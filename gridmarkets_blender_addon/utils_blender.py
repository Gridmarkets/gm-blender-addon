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
import collections
import json

from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.invalid_input_error import InvalidInputError

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.job import Job
from gridmarkets.errors import *

from blender_asset_tracer import trace

# global client to reuse
_envoy_client = None


def get_wrapped_logger(name):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    return PluginFetcher.get_plugin().get_logging_coordinator().get_logger(name)


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
        addon_prefs = bpy.context.user_preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

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
    addon_prefs = bpy.context.user_preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

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
        addon_prefs = bpy.context.user_preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        # check neither the email or access key have changed
        if addon_prefs.auth_email == _envoy_client.email and addon_prefs.auth_accessKey == _envoy_client.access_key:
            log.info("Returning existing Envoy client...")
            return  _envoy_client

    # update the client
    _envoy_client = get_new_envoy_client()

    return _envoy_client


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
    if (not hasattr(job, "use_custom_frame_ranges")) or job.use_custom_frame_ranges:

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

    if hasattr(job, "use_custom_frame_ranges") and not job.use_custom_frame_ranges:
        return False

    # buffer to store frames already seen
    frames_buffer = []

    for frame_range in job.frame_ranges:

        if not frame_range.enabled:
            continue

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
    return {"CYCLES", "VRAY_RENDER_RT", "BLENDER_RENDER"}


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


def is_addon_enabled(addon_name: str):
    is_enabled, is_loaded = addon_utils.check(addon_name)
    return is_enabled and is_loaded


def get_selected_project_options(scene, context, id):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.icon_loader import IconLoader
    from gridmarkets_blender_addon import api_constants
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]

    project_options = [
        # it is always an option to upload as a new project
        (constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE,
         constants.PROJECT_OPTIONS_NEW_PROJECT_LABEL,
         constants.PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION,
         'FILE_NEW', 0)
    ]

    plugin = PluginFetcher.get_plugin_if_initialised()

    if plugin:
        remote_project_container = plugin.get_remote_project_container()
        remote_projects = remote_project_container.get_all()

        a = 0

        # iterate through uploaded projects and add them as options
        for i, project in enumerate(remote_projects):
            project_product = project.get_attribute("PRODUCT")

            # get the correct icon
            if project_product == "vray":
                icon = preview_collection[constants.VRAY_LOGO_ID].icon_id
            elif project_product == "blender":
                icon = constants.ICON_BLENDER
            else:
                icon = constants.ICON_PROJECT

            # if render engine set to V-Ray only return VRay projects
            if context.scene.render.engine == constants.VRAY_RENDER_RT and project_product == api_constants.PRODUCTS.VRAY:
                append = True
            elif context.scene.render.engine != constants.VRAY_RENDER_RT and project_product != api_constants.PRODUCTS.VRAY:
                # otherwise only return blender projects
                append = True
            else:
                append = False

            if append:
                a += 1

                if a == int(id):
                    return project

                project_options.append(
                    (str(i + 1), project.get_name(), '', icon, remote_project_container.get_project_id(project)))

    return project_options
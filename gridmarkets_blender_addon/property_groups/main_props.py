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

import typing

from bpy.app.handlers import persistent
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps
from gridmarkets_blender_addon.property_groups.job_props import JobProps
from gridmarkets_blender_addon.property_groups.project_props import ProjectProps
from gridmarkets_blender_addon.blender_plugin.user_interface.property_groups.user_interface_props import UserInterfaceProps
from gridmarkets_blender_addon.blender_plugin.remote_project.property_groups.remote_project_props import RemoteProjectProps
from gridmarkets_blender_addon.blender_plugin.log_item.property_groups.log_item_props import LogItemProps
from gridmarkets_blender_addon.blender_plugin.log_history_container.property_groups.log_history_container_props import LogHistoryContainerProps
from gridmarkets_blender_addon.blender_plugin.job_preset.property_groups.job_preset_props import JobPresetProps
from gridmarkets_blender_addon.blender_plugin.job_preset_container.property_groups.job_preset_container_props import JobPresetContainerprops
from gridmarkets_blender_addon.blender_plugin.remote_project_container.property_groups.remote_project_container_props import RemoteProjectContainerProps
from gridmarkets_blender_addon.property_groups.custom_settings_views import CustomSettingsViews
from gridmarkets_blender_addon.property_groups.vray_props import VRayProps

_BLEND_FILE = "*" + constants.BLEND_FILE_EXTENSION


def _get_project_options(scene, context):
    """ Returns a list of items representing project options """

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.icon_loader import IconLoader
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

        # iterate through uploaded projects and add them as options
        for i, project in enumerate(remote_projects):
            project_product = project.get_attribute(api_constants.API_KEYS.APP)

            # get the correct icon
            if project_product == api_constants.PRODUCTS.VRAY:
                icon = preview_collection[constants.VRAY_LOGO_ID].icon_id
            elif project_product == api_constants.PRODUCTS.BLENDER:
                icon = constants.ICON_BLENDER
            else:
                icon = constants.ICON_PROJECT

            project_options.append(
                (str(i + 1), project.get_name(), '', icon, remote_project_container.get_project_id(project)))

    return project_options




def get_job_options(scene, context):
    """ Returns a list of items representing project options """

    from gridmarkets_blender_addon import utils_blender
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    job_preset_container = plugin.get_preferences_container().get_job_preset_container()
    job_presets = job_preset_container.get_all()

    compatible_job_definitions = utils_blender.get_matching_job_definitions()
    compatible_job_definitions_ids = list(map(lambda x: x.get_definition_id(), compatible_job_definitions))

    _job_options = []

    # iterate through uploaded job presets and add them as options
    for i, job_preset in enumerate(job_presets):

        # only return job presets deriving from a compatible job definition
        if job_preset.get_job_definition().get_definition_id() not in compatible_job_definitions_ids:
            continue

        value = job_preset.get_id()
        job_preset_option_tuple = (value, job_preset.get_name(), '', constants.ICON_JOB, job_preset.get_id_number())
        _job_options.append(job_preset_option_tuple)

    return _job_options


def get_selected_job_option(context: bpy.types.Context) -> typing.Optional['JobPreset']:
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    job_preset_container = plugin.get_preferences_container().get_job_preset_container()

    job_preset_options = get_job_options(context.scene, context)
    if job_preset_options:
        job_preset_option = job_preset_container.get_with_id(context.scene.props.job_options)
    else:
        job_preset_option = None

    return job_preset_option


def _job_options_getter(self):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin_if_initialised()

    # if the plugin is not initialised then return 0
    if plugin is None:
        return 0

    # if there are no valid job preset options return 0
    job_preset_options = get_job_options(None, None)
    if len(job_preset_options) == 0:
        return 0

    default_option = job_preset_options[0][4]

    # if the value has not yet been set, return default_option
    try:
        index = self['job_option']
    except KeyError:
        return default_option

    # check that index refers to a job preset option
    for job_preset_option in job_preset_options:
        if job_preset_option[4] == index:
            break
    else:
        return default_option

    return index


def _job_options_setter(self, value):
    self['job_option'] = value


def _get_tab_items(scene, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin_if_initialised()

    if plugin:
        if not plugin.get_api_client().is_user_signed_in():
            return [
                (constants.TAB_CREDENTIALS, constants.TAB_CREDENTIALS, ''),
            ]

    if bpy.context.scene.render.engine == constants.VRAY_RENDER_RT:
        return [
            (constants.TAB_SUBMISSION_SETTINGS, constants.TAB_SUBMISSION_SETTINGS, ''),
            (constants.TAB_PROJECTS, constants.TAB_PROJECTS, ''),
            (constants.TAB_CREDENTIALS, constants.TAB_CREDENTIALS, ''),
            (constants.TAB_LOGGING, constants.TAB_LOGGING, ''),
        ]

    return [
        (constants.TAB_SUBMISSION_SETTINGS, constants.TAB_SUBMISSION_SETTINGS, ''),
        (constants.TAB_PROJECTS, constants.TAB_PROJECTS, ''),
        (constants.TAB_JOB_PRESETS, constants.TAB_JOB_PRESETS, ''),
        (constants.TAB_CREDENTIALS, constants.TAB_CREDENTIALS, ''),
        (constants.TAB_LOGGING, constants.TAB_LOGGING, ''),
    ]


def _get_tab_option(self):
    try:
        value = self["tab_option"]

        # if the selected tab option no longer exists we need to set it to something else
        options = _get_tab_items(bpy.context.scene, bpy.context)
        if value >= len(options):
            value = len(options) - 1

    except KeyError:
        value = 0
    return value


def _set_tab_option(self, value):
    self["tab_option"] = value


class GRIDMARKETS_PROPS_Addon_Properties(bpy.types.PropertyGroup):
    """ Class to represent the main state of the plugin. Holds all the properties that are accessible via the interface.
    """

    user_interface: bpy.props.PointerProperty(
        type=UserInterfaceProps
    )

    remote_project_container: bpy.props.PointerProperty(
        type=RemoteProjectContainerProps,
    )

    log_history_container: bpy.props.PointerProperty(
        type=LogHistoryContainerProps,
    )

    job_preset_container: bpy.props.PointerProperty(
        type=JobPresetContainerprops,
    )

    vray: bpy.props.PointerProperty(
        type=VRayProps
    )

    # project collection
    projects: bpy.props.CollectionProperty(
        type=ProjectProps,
    )

    selected_project: bpy.props.IntProperty(
        options=set()
    )

    # projects enum
    project_options: bpy.props.EnumProperty(
        name="Project",
        description="The list of possible projects to use on submit",
        items=_get_project_options
    )

    # job collection
    jobs: bpy.props.CollectionProperty(
        type=JobProps
    )

    selected_job: bpy.props.IntProperty(
        options=set()
    )

    # jobs enum
    job_options: bpy.props.EnumProperty(
        name="Job",
        description="The list of possible jobs to use on submit",
        items=get_job_options,
        get=_job_options_getter,
        set=_job_options_setter
    )

    tab_options: bpy.props.EnumProperty(
        name="Tabs",
        description="The tabs that show at the top of the add-on main window",
        items = _get_tab_items,
        get=_get_tab_option,
        set=_set_tab_option
    )

    submission_summary_open: bpy.props.BoolProperty(
        name="Submission Summary Open",
        description="Whether or not the submission summary view is open",
        default=False
    )

    is_logging_console_open: bpy.props.BoolProperty(
        name="Is Logging Console Open",
        description="Whether or not the logging console is open",
        default=True
    )

    custom_settings_views: bpy.props.PointerProperty(type=CustomSettingsViews)

    # path to the .blend file that you want to pack
    blend_file_path: bpy.props.StringProperty(
        name="Blend file",
        description="The path to your .blend file that you want to pack",
        default=_BLEND_FILE,
        subtype='FILE_PATH'
    )

    # used for uploading packed projects
    root_directory: bpy.props.StringProperty(
        name="Root Directory",
        description="The path to the root of your project.",
        subtype='DIR_PATH'
    )

    upload_all_files_in_root: bpy.props.BoolProperty(
        name="Upload Everything",
        description="Select to upload all files in the root directory. Otherwise only known files will be uploaded",
        default=False
    )

    # path to a directory that you want to pack the .blend file to
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="A path to a directory that you want to pack your .blend file to",
        subtype='DIR_PATH'
    )

    # a constant that is actually a prop to keep the formatting the same as other props
    project_defined: bpy.props.StringProperty(
        default="<Value inferred from project>",
        options={'HIDDEN', 'SKIP_SAVE'}
    )


classes = (
    CustomSettingsViews,
    FrameRangeProps,
    VRayProps,
    JobProps,
    ProjectProps,
    UserInterfaceProps,
    RemoteProjectProps,
    RemoteProjectContainerProps,
    LogItemProps,
    LogHistoryContainerProps,
    JobPresetProps,
    JobPresetContainerprops,
    GRIDMARKETS_PROPS_Addon_Properties,
)


@persistent
def reset_to_defaults(pos):
    from gridmarkets_blender_addon import utils
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    PluginFetcher.delete_cached_plugin()

    # options={'SKIP_SAVE'} doesnt work for global properties so we must reset manually
    bpy.context.scene.props.vray.frame_ranges.clear()
    bpy.context.scene.props.vray.selected_frame_range = 0

    bpy.context.scene.props.log_history_container.log_history_items.clear()
    bpy.context.scene.props.log_history_container.focused_log_item = 0

    bpy.context.scene.props.remote_project_container.remote_projects.clear()
    bpy.context.scene.props.remote_project_container.focused_remote_project = 0

    frame_range = bpy.context.scene.props.vray.frame_ranges.add()
    frame_range.name = "Default frame range"
    frame_range.enabled = True
    frame_range.frame_start = 1
    frame_range.frame_end = 256
    frame_range.frame_step = 1


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    # register add-on properties
    bpy.types.Scene.props = bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_Addon_Properties)

    # add event handler
    bpy.app.handlers.load_post.append(reset_to_defaults)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

    # delete add-on properties
    del bpy.types.Scene.props

    # remove event handler
    bpy.app.handlers.load_post.remove(reset_to_defaults)

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
from bpy.app.handlers import persistent
from gridmarkets_blender_addon import constants, api_constants

from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps
from gridmarkets_blender_addon.property_groups.job_props import JobProps
from gridmarkets_blender_addon.property_groups.project_props import ProjectProps
from gridmarkets_blender_addon.blender_plugin.user_interface.property_groups.user_interface_props import UserInterfaceProps
from gridmarkets_blender_addon.blender_plugin.remote_project.property_groups.remote_project_props import RemoteProjectProps
from gridmarkets_blender_addon.blender_plugin.log_item.property_groups.log_item_props import LogItemProps
from gridmarkets_blender_addon.blender_plugin.log_history_container.property_groups.log_history_container_props import LogHistoryContainerProps
from gridmarkets_blender_addon.blender_plugin.remote_project_container.property_groups.remote_project_container_props import RemoteProjectContainerProps
from gridmarkets_blender_addon.property_groups.custom_settings_views import CustomSettingsViews
from gridmarkets_blender_addon.property_groups.vray_props import VRayProps


def _get_project_options(scene, context):
    """ Returns a list of items representing project options """

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.icon_loader import IconLoader
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]

    props = context.scene.props

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
                project_options.append(
                    (str(i + 1), project.get_name(), '', icon, remote_project_container.get_project_id(project)))

    return project_options


def _get_job_options(scene, context):
    """ Returns a list of items representing project options """

    props = context.scene.props

    job_options = [
        (constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE,
         constants.JOB_OPTIONS_BLENDERS_SETTINGS_LABEL,
         constants.JOB_OPTIONS_BLENDERS_SETTINGS_DESCRIPTION,
         'BLENDER', 0)
    ]

    # iterate through uploaded projects and add them as options
    for i, job in enumerate(props.jobs):
        job_options.append((str(i + 1), job.name, '', constants.ICON_JOB, job.id))

    return job_options


def _get_tab_items(scene, context):

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

    vray : bpy.props.PointerProperty(
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
        items=_get_job_options
    )

    # upload project progress props
    uploading_project: bpy.props.BoolProperty(
        name="Uploading Project",
        description="Indicates that a project is being uploaded",
        default=False,
        options={'SKIP_SAVE'}
    )

    uploading_project_progress: bpy.props.IntProperty(
        name="Uploading Project Progress",
        description="What percent of the project has been uploaded",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE',
        options={'SKIP_SAVE'}
    )

    uploading_project_status: bpy.props.StringProperty(
        name="Uploading Project Status",
        description="A brief description of the current status of the uploading operation",
        default="",
    )

    # submit operation progress props
    submitting_project: bpy.props.BoolProperty(
        name="Submitting Project",
        description="Indicates that a project is being submitted",
        default=False,
        options={'SKIP_SAVE'}
    )

    submitting_project_progress: bpy.props.IntProperty(
        name="Submitting Project Progress",
        description="The progress made towards submitting this job",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE',
        options={'SKIP_SAVE'}
    )

    submitting_project_status: bpy.props.StringProperty(
        name="Submitting Project Status",
        description="A brief description of the current status of the submit operation",
        default="",
        options={'SKIP_SAVE'}
    )

    tab_options: bpy.props.EnumProperty(
        name="Tabs",
        description="The tabs that show at the top of the add-on main window",
        items = _get_tab_items
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
    GRIDMARKETS_PROPS_Addon_Properties,
)


@persistent
def reset_to_defaults(pos):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    PluginFetcher.delete_cached_plugin()

    # options={'SKIP_SAVE'} doesnt work for global properties so we must reset manually
    bpy.context.scene.props.uploading_project = False
    bpy.context.scene.props.uploading_project_progress = 0
    bpy.context.scene.props.submitting_project = False
    bpy.context.scene.props.submitting_project_progress = 0
    bpy.context.scene.props.submitting_project_status = ""

    while len(bpy.context.scene.props.vray.frame_ranges) > 0:
        bpy.context.scene.props.vray.frame_ranges.pop()

    bpy.context.scene.props.vray.selected_frame_range = 0

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


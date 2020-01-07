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

from gridmarkets_blender_addon import constants, utils_blender


def draw_submission_summary(layout, context):
    scene = context.scene
    props = scene.props
    open = props.submission_summary_open

    box = layout.box()

    col = box.column()
    row = col.row(align=True)
    row.alignment = 'LEFT'

    row.operator(
        constants.OPERATOR_TOGGLE_SUBMISSION_SUMMARY_ID_NAME,
        text="Submission Summary",
        icon=constants.ICON_DISCLOSURE_TRI_DOWN if open else constants.ICON_DISCLOSURE_TRI_RIGHT,
        emboss=False,
    )

    if open:
        split = col.split(factor=0.2)
        labels = split.column()
        labels.label(text="Project: ")
        labels.separator()
        labels.label(text="Job: ")
        labels.label(text="App: ")
        labels.label(text="App Version: ")
        labels.label(text="GM Operation: ")
        labels.label(text="Path: ")
        labels.label(text="Frame range(s): ")
        labels.label(text="Output prefix: ")
        labels.label(text="Output format: ")
        labels.label(text="Output path: ")
        labels.label(text="Render Engine: ")
        labels.label(text="Resolution X: ")
        labels.label(text="Resolution Y: ")
        labels.label(text="Resolution %: ")
        labels.label(text="Frame Rate: ")

        values = split.column()
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            values.label(text=constants.PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION)
        else:
            project = utils_blender.get_selected_project_options(scene, context,
                                                                 props.project_options)  # props.projects[int(props.project_options) - constants.PROJECT_OPTIONS_STATIC_COUNT]
            values.label(text=project.get_name())
        values.separator()

        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            values.label(text=constants.JOB_OPTIONS_BLENDERS_SETTINGS_LABEL)
        else:
            selected_job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]
            values.label(text=selected_job.name)

        # get a gridmarkets job. The render file doesnt matter for now
        job = utils_blender.get_job(context, "RENDER FILE", enable_logging=False)
        values.label(text=job.app)
        values.label(text=job.app_version)
        values.label(text=job.operation)
        values.label(text=job.path)
        values.label(text=job.params['frames'])
        values.label(text=job.params['output_prefix'])
        values.label(text=job.params['output_format'])
        values.label(text=utils_blender.get_job_output_path_abs(context))
        values.label(text=job.params['engine'])
        values.label(text=str(scene.render.resolution_x))
        values.label(text=str(scene.render.resolution_y))
        values.label(text=str(scene.render.resolution_percentage) + ' %')
        values.label(text=str(scene.render.fps))


def draw_submission_settings(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.set_focused_job_preset import \
        GRIDMARKETS_OT_set_focused_job_preset
    from gridmarkets_blender_addon.property_groups.main_props import get_job_options
    from gridmarkets_blender_addon.operators.set_ui_layout import GRIDMARKETS_OT_set_layout
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    job_preset_container = plugin.get_preferences_container().get_job_preset_container()

    # get the selected job preset option
    if get_job_options(context.scene, context):
        job_preset_option = job_preset_container.get_at(int(context.scene.props.job_options))
    else:
        job_preset_option = None

    layout.use_property_split = True
    layout.use_property_decorate = False  # No animating of properties

    props = context.scene.props

    # submit box
    box = layout.box()
    box.use_property_split = False
    split = box.split()

    # project options
    col = split.column(align=True)
    col.label(text="Project")
    sub = col.row()
    sub.enabled = False
    sub.label(text="The project to run the selected job against.")
    col.separator(factor=1.0)
    col.box().prop(props, "project_options", text="")

    # job options
    col = split.column(align=True)
    col.label(text="Job")
    sub = col.row()
    sub.enabled = False
    sub.label(text="The render settings and output settings to use.")
    col.separator(factor=1.0)
    job_preset_box = col.box().row(align=True)

    if job_preset_option:
        job_preset_index = job_preset_container.get_index(job_preset_option)

        row2 = job_preset_box.row()
        row2.prop(props, "job_options", text="")
        row3 = row2.row()
        row3.alignment = 'RIGHT'
        row3.operator(GRIDMARKETS_OT_set_focused_job_preset.bl_idname, text="",
                      icon=constants.ICON_HIDE_OFF).job_preset_index = job_preset_index
    else:
        row2 = job_preset_box.row(align=True)
        row2.label(text="You have not created any Job Presets to choose from.", icon=constants.ICON_ERROR)
        row3 = row2.row()
        row3.alignment = 'RIGHT'
        row3.operator(GRIDMARKETS_OT_set_layout.bl_idname,
                      text="New Job Preset").layout = constants.JOB_PRESETS_LAYOUT_VALUE

    submit_text = "Submit"
    submit_icon = "NONE"

    # submit button / progress indicator
    row = box.row(align=True)
    row.scale_y = 2.5

    # disable submit button when already running an operation
    if plugin.get_user_interface().is_running_operation():
        row.enabled = False

    # disable if there are no job presets to choose from
    if not job_preset_option:
        row.enabled = False

    # if the engine is not in the supported engines list disable and show a help message
    render_engine = "CYCLES"  # utils_blender.get_job_render_engine(context)
    if render_engine not in utils_blender.get_supported_render_engines():
        row.enabled = False
        submit_text = "Render engine '%s' is not currently supported" % utils_blender.get_user_friendly_name_for_engine(
            render_engine)
        submit_icon = constants.ICON_ERROR

    row.operator(constants.OPERATOR_SUBMIT_ID_NAME, text=submit_text, icon=submit_icon)

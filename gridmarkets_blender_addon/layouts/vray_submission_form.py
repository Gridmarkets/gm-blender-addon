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

def _draw_frame_ranges_view(self, context):
    from gridmarkets_blender_addon import constants, utils_blender

    layout = self.layout
    props = context.scene.props


    frame_ranges = props.vray.frame_ranges
    frame_range_count = len(frame_ranges)

    row = layout.row()
    row.template_list("GRIDMARKETS_UL_frame_range", "", props.vray, "frame_ranges", props.vray,
                      "selected_frame_range", rows=5)

    col = row.column()
    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_MODIFIER, text="").action = 'EDIT'

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_ADD, text="").action = 'ADD'

    remove = sub.row()
    # prevent the user removing the last frame range for a job
    if frame_range_count < 2:
        remove.enabled = False
    remove.operator(constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_REMOVE, text="").action = 'REMOVE'

    sub = col.column(align=True)

    # disable up / down buttons if only one frame range
    if frame_range_count < 2:
        sub.enabled = False

    sub.operator(constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_UP, text="").action = 'UP'
    sub.operator(constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_DOWN, text="").action = 'DOWN'

    # display warning if overlapping frame ranges
    if utils_blender.do_frame_ranges_overlap(props.vray):
        sub = layout.row()
        sub.enabled=False
        sub.label(text="Warning: frame ranges overlap. You will still be charged for overlapping frames but will "
                       "receive only one output frame for each conflict.", icon=constants.ICON_ERROR)


def draw_v_ray_submission_form(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon import utils_blender, constants
    from types import SimpleNamespace

    plugin = PluginFetcher.get_plugin()

    props = context.scene.props
    new_project = props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE

    if not new_project:
        project = utils_blender.get_selected_project_options(context.scene, context, props.project_options)

    # submit box
    box = self.layout.box()
    col = box.column(align=True)
    col.label(text="V-Ray Job Options")
    col.separator()
    # project options

    sub = col.row()
    sub.prop(props, "project_options", text="Project Options:")

    sub = col.row()
    sub.enabled = False
    sub.label(text="The project to run the selected job against.")
    col.separator()


    if new_project:
        col.prop(props.vray, "project_name")

    else:
        sub = col.row()
        sub.label(text="Progect Name:")
        sub.box().label(text=project.get_name())

    sub = col.row()
    sub.label(text="The name of the GridMarkets project the files will be / are stored on.")
    sub.enabled = False

    col.separator()
    col.prop(props.vray, "job_name")
    sub = col.row()
    sub.label(text="The name of the job as it will show in the render manager")
    sub.enabled = False

    col.separator()
    col.label(text="Frame Ranges:")
    sub = col.row()
    sub.label(text="Defines the frame range in format start [end] [step],[start [end] [step]],...")
    _draw_frame_ranges_view(SimpleNamespace(layout=col), context)

    sub.enabled = False

    col.separator()
    sub = col.row()
    sub.label(text="Output Width:")
    sub.prop(props.vray, "output_width", text="")
    sub = col.row()
    sub.label(text="Defines the render output width")
    sub.enabled = False

    col.separator()
    sub = col.row()
    sub.label(text="Output Height:")
    sub.prop(props.vray, "output_height", text="")
    sub = col.row()
    sub.label(text="Defines the render output height.")
    sub.enabled = False

    col.separator()
    col.prop(props.vray, "output_prefix")
    sub = col.row()
    sub.label(text="Defines the render output file prefix.")
    sub.enabled = False

    col.separator()
    col.prop(props.vray, "output_format")
    sub = col.row()
    sub.label(text="Defines the render output format.")
    sub.enabled = False

    col.separator()
    col.prop(props.vray, "output_path")
    sub = col.row()
    sub.label(text="Defines the path to download the results to.")
    sub.enabled = False

    submit_text = "Submit V-Ray Project"
    submit_icon = "NONE"

    # submit button / progress indicator
    row = box.row(align=True)
    row.scale_y = 2.5

    # disable submit button when already running an operation
    if plugin.get_user_interface().is_running_operation():
        row.enabled = False

    if not utils_blender.is_addon_enabled("vb30"):
        row.enabled = False

    vray = props.vray

    op = row.operator('gridmarkets.submit_new_vray_project', text=submit_text, icon=submit_icon)

    if new_project:
        op.project_name = vray.project_name
    else:
        op.project_name = project.get_name()

    op.job_name = vray.job_name
    op.frame_ranges = utils_blender.get_job_frame_ranges(context, job=vray)
    op.output_width = vray.output_width
    op.output_height = vray.output_height
    op.output_prefix = vray.output_prefix
    op.output_format = vray.output_format
    op.output_path = vray.output_path

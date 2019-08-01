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
from types import SimpleNamespace
from gridmarkets_blender_addon import constants, utils_blender


def _draw_frame_ranges_view(self, context):
    layout = self.layout
    props = bpy.context.scene.props
    selected_job = props.jobs[props.selected_job]
    frame_range_count = len(selected_job.frame_ranges)

    enabled = selected_job.use_custom_frame_ranges

    row = layout.row()
    row.active = enabled
    row.template_list("GRIDMARKETS_UL_frame_range", "", selected_job, "frame_ranges", selected_job,
                      "selected_frame_range", rows=5)

    col = row.column()
    col.active = enabled

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_MODIFIER, text="").action = 'EDIT'

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_ADD, text="").action = 'ADD'

    remove = sub.row()
    # prevent the user removing the last frame range for a job
    if frame_range_count < 2:
        remove.enabled = False
    remove.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_REMOVE, text="").action = 'REMOVE'

    sub = col.column(align=True)

    # disable up / down buttons if only one frame range
    if frame_range_count < 2:
        sub.enabled = False

    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_UP, text="").action = 'UP'
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_DOWN, text="").action = 'DOWN'

    # display warning if overlapping frame ranges
    if utils_blender.do_frame_ranges_overlap(selected_job):
        sub = layout.row()
        sub.enabled=False
        sub.label(text="Warning: frame ranges overlap. You will still be charged for overlapping frames but will "
                       "receive only one output frame for each conflict.", icon=constants.ICON_ERROR)


def _draw_output_format_view(self, context):
    layout = self.layout
    job = context.scene.props.jobs[context.scene.props.selected_job]
    layout.prop(job, "output_format")


def _draw_output_path_view(self, context):
    layout = self.layout
    job = context.scene.props.jobs[context.scene.props.selected_job]

    layout.prop(job, "output_path")
    sub = layout.row()
    sub.enabled=False
    sub.label(text="Note: Relative paths will not work if the scene has not been saved")


def _draw_output_prefix_view(self, context):
    layout = self.layout
    job = context.scene.props.jobs[context.scene.props.selected_job]

    layout.prop(job, "output_prefix")
    sub = layout.row()
    sub.enabled=False


def _draw_render_engine_view(self, context):
    layout = self.layout
    job = context.scene.props.jobs[context.scene.props.selected_job]
    layout.prop(job, "render_engine")


def _draw_view(self, context, operator_id, view_name, draw_handler):
    views = context.scene.props.custom_settings_views
    job = context.scene.props.jobs[context.scene.props.selected_job]

    box = self.layout.box()
    col = box.column(align = True)
    row = col.row(align=True)
    row.alignment = 'LEFT'

    view = getattr(views, view_name + '_view')

    row.operator(
        operator_id,
        text="",
        icon= constants.ICON_DISCLOSURE_TRI_DOWN if view else constants.ICON_DISCLOSURE_TRI_RIGHT,
        emboss=False,
    )

    row.prop(job, "use_custom_" + view_name)

    if view:
        draw_handler(SimpleNamespace(layout=col), context)


def draw_jobs(self, context):
    layout = self.layout
    props = context.scene.props
    job_count = len(props.jobs)

    layout.label(text='Preset Jobs')

    row = layout.row()
    row.template_list("GRIDMARKETS_UL_job", "", props, "jobs", props, "selected_job", rows=3)

    col = row.column()

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_JOB_LIST_ACTIONS_ID_NAME, icon=constants.ICON_ADD, text="").action = 'ADD'
    sub2 = sub.row()

    # disable remove button if there are no projects to remove
    if job_count <= 0:
        sub2.enabled = False

    sub2.operator(constants.OPERATOR_JOB_LIST_ACTIONS_ID_NAME, icon=constants.ICON_REMOVE, text="").action = 'REMOVE'

    sub = col.column(align=True)

    # disable up and down buttons if there are less than 2 projects
    if job_count < 2:
        sub.enabled = False

    sub.operator(constants.OPERATOR_JOB_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_UP, text="").action = 'UP'
    sub.operator(constants.OPERATOR_JOB_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_DOWN, text="").action = 'DOWN'

    if len(context.scene.props.jobs) > 0:
        _draw_job_settings(self, context)


def _draw_job_settings(self, context):
    layout = self.layout
    scene = context.scene
    props = scene.props
    job = context.scene.props.jobs[context.scene.props.selected_job]

    custom_settings_box = SimpleNamespace(layout=self.layout.box())
    custom_settings_box.layout.label(text="Overridable Settings")

    _draw_view(custom_settings_box, context, constants.OPERATOR_TOGGLE_FRAME_RANGES_VIEW_ID_NAME, "frame_ranges", _draw_frame_ranges_view)

    # output format
    _draw_view(custom_settings_box, context, constants.OPERATOR_TOGGLE_OUTPUT_FORMAT_VIEW_ID_NAME, "output_format",
               _draw_output_format_view)

    # output path
    _draw_view(custom_settings_box, context, constants.OPERATOR_TOGGLE_OUTPUT_PATH_VIEW_ID_NAME, "output_path", _draw_output_path_view)

    # output prefix
    _draw_view(custom_settings_box, context, constants.OPERATOR_TOGGLE_OUTPUT_PREFIX_VIEW_ID_NAME, "output_prefix",
               _draw_output_prefix_view)

    # render engine
    _draw_view(custom_settings_box, context, constants.OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_ID_NAME, "render_engine",
               _draw_render_engine_view)

    gm_settings = layout.box()
    gm_settings.label(text="GridMarkets Job Settings")

    # render device
    gm_settings.prop(job, "render_device")

    # resolution x
    # Todo (needs agent update)

    # resolution y
    # Todo (needs agent update)

    # resolution percentage
    # Todo (needs agent update)

    # frame rate
    # Todo (needs agent update)
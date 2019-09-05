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

from types import SimpleNamespace
from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.layouts.submission_settings import draw_submission_settings, draw_submission_summary
from gridmarkets_blender_addon.layouts.preferences import draw_preferences
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts import draw_remote_project_container
from gridmarkets_blender_addon.layouts.jobs import draw_jobs
from gridmarkets_blender_addon.layouts.console import draw_console, draw_compact_console
from gridmarkets_blender_addon.layouts.sidebar import draw_sidebar

from gridmarkets_blender_addon.layouts.sidebar import draw_sidebar
from gridmarkets_blender_addon.layouts.vray_submission_form import draw_v_ray_submission_form


def draw_body(self, context):
    layout = self.layout
    props = context.scene.props

    # split to show the side bar
    split = layout.split(percentage=0.2)
    col = SimpleNamespace(layout=split.column())

    # draw the sidebar
    draw_sidebar(col, context)

    # draw the main body
    col = split.column()
    box = col.box()
    row = box.row()
    row.prop(props, "tab_options", expand=True)
    col = SimpleNamespace(layout=col)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        if context.scene.render.engine == "VRAY_RENDER_RT":
            draw_v_ray_submission_form(col, context)
            draw_compact_console(col, context)
        else:
            draw_submission_settings(col, context)
            draw_submission_summary(col, context)
            draw_compact_console(col, context)

    elif props.tab_options == constants.TAB_PROJECTS:
        draw_remote_project_container(col, context)
        draw_compact_console(col, context)
    elif props.tab_options == constants.TAB_JOB_PRESETS:
        draw_jobs(col, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(col, context)
    elif props.tab_options == constants.TAB_LOGGING:
        draw_console(col, context)

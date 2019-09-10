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

from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.layouts.submission_settings import draw_submission_settings, draw_submission_summary
from gridmarkets_blender_addon.layouts.preferences import draw_preferences
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts import draw_remote_project_container
from gridmarkets_blender_addon.layouts.jobs import draw_jobs

from gridmarkets_blender_addon.blender_plugin.log_history_container.layouts.draw_logging_console import draw_logging_console

from gridmarkets_blender_addon.layouts.sidebar import draw_sidebar
from gridmarkets_blender_addon.layouts.vray_submission_form import draw_v_ray_submission_form

_CONSOLE_SEPARATOR_SPACING = 2

def draw_body(self, context):
    layout = self.layout
    props = context.scene.props

    box = layout.box()
    row = box.row()
    row.prop_tabs_enum(props, "tab_options", icon_only=True)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        if context.scene.render.engine == "VRAY_RENDER_RT":

            from gridmarkets_blender_addon import utils_blender

            # submit box
            box = self.layout.box()
            row = box.column(align=True)

            # project options
            row.label(text="Project")
            sub = row.row()
            sub.enabled = False
            sub.label(text="The project to run the selected job against.")
            row.separator()
            row.prop(props, "project_options", text="")

            submit_text = "Submit V-Ray Project"
            submit_icon = "NONE"

            # submit button / progress indicator
            row = box.row(align=True)
            row.scale_y = 2.5
            if props.submitting_project:
                row.prop(props, "submitting_project_progress", text=props.submitting_project_status)
            else:
                # disable submit button when uploading project
                if props.uploading_project:
                    row.enabled = False

                if not utils_blender.is_addon_enabled("vb30"):
                    row.enabled = False

                row.operator(constants.OPERATOR_SUBMIT_ID_NAME, text=submit_text, icon=submit_icon)
        else:
            draw_submission_settings(self, context)
            draw_submission_summary(self, context)
            self.layout.separator(factor=_CONSOLE_SEPARATOR_SPACING)
            draw_logging_console(self, context)

    elif props.tab_options == constants.TAB_PROJECTS:
        draw_remote_project_container(self, context)
        self.layout.separator(factor=_CONSOLE_SEPARATOR_SPACING)
        draw_logging_console(self, context)
    elif props.tab_options == constants.TAB_JOB_PRESETS:
        draw_jobs(self, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(self, context)
    elif props.tab_options == constants.TAB_LOGGING:
        draw_logging_console(self, context)

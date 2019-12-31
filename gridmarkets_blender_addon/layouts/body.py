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
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts.draw_remote_project_container import \
    draw_remote_project_container
from gridmarkets_blender_addon.blender_plugin.job_preset_container.layouts.draw_job_preset_container import draw_job_preset_container

from gridmarkets_blender_addon.blender_plugin.log_history_container.layouts.draw_logging_console import \
    draw_logging_console

from gridmarkets_blender_addon.layouts.sidebar import draw_sidebar
from gridmarkets_blender_addon.layouts.vray_submission_form import draw_v_ray_submission_form

_CONSOLE_SEPARATOR_SPACING = 2


# new imports
from gridmarkets_blender_addon.menus import *


def draw_body(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    api_client = plugin.get_api_client()

    layout = self.layout
    props = context.scene.props

    # only show the login screen if not logged in
    if not api_client.is_user_signed_in():
        layout.separator()
        draw_preferences(self, context)
        return

    """
    box = layout.box()
    row = box.row()
    row.prop_tabs_enum(props, "tab_options", icon_only=True)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        if context.scene.render.engine == "VRAY_RENDER_RT":
            draw_v_ray_submission_form(self, context)
            draw_logging_console(self, context)
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
        draw_job_preset_container(self, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(self, context)
    elif props.tab_options == constants.TAB_LOGGING:
        draw_logging_console(self, context)
    """

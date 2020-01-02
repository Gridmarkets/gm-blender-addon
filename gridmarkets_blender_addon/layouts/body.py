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

import typing

from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.layouts.submission_settings import draw_submission_settings, draw_submission_summary
from gridmarkets_blender_addon.layouts.preferences import draw_preferences
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts.draw_remote_project_container import \
    draw_remote_project_container
from gridmarkets_blender_addon.blender_plugin.job_preset_container.layouts.draw_job_preset_container import \
    draw_job_preset_container

from gridmarkets_blender_addon.blender_plugin.log_history_container.layouts.draw_logging_console import \
    draw_logging_console

from gridmarkets_blender_addon.layouts.sidebar import draw_sidebar
from gridmarkets_blender_addon.layouts.vray_submission_form import draw_v_ray_submission_form

_CONSOLE_SEPARATOR_SPACING = 2

# new imports
from gridmarkets_blender_addon.layouts.draw_pack_and_upload_current_scene import draw_pack_and_upload_current_scene
from gridmarkets_blender_addon.layouts.draw_upload_packed_project import draw_upload_packed_project
from gridmarkets_blender_addon.layouts.draw_pack_current_scene import draw_pack_current_scene
from gridmarkets_blender_addon.layouts.draw_pack_external_project import draw_pack_external_project
from gridmarkets_blender_addon.layouts.draw_manually_add_remote_project import draw_manually_add_remote_project


def _get_ui_layout_draw_method(ui_layout: (str, str, str, str, int)) -> typing.Callable:
    """ Matches a ui_layout tuple with it's draw method """

    map = {
        constants.JOB_PRESETS_LAYOUT_TUPLE[0]: draw_job_preset_container,
        constants.REMOTE_PROJECTS_LAYOUT_TUPLE[0]: draw_remote_project_container,
        constants.UPLOAD_CURRENT_SCENE_TUPLE[0]: draw_pack_and_upload_current_scene,
        constants.UPLOAD_PACKED_PROJECT_TUPLE[0]: draw_upload_packed_project,
        constants.PACK_CURRENT_SCENE_TUPLE[0]: draw_pack_current_scene,
        constants.PACK_BLEND_FILE_TUPLE[0]: draw_pack_external_project,
        constants.UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_TUPLE[0]: draw_manually_add_remote_project,
    }

    return map[ui_layout[0]]


def draw_body(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    api_client = plugin.get_api_client()
    user_interface = plugin.get_user_interface()

    layout = self.layout

    # only show the login screen if not logged in
    if not api_client.is_user_signed_in():
        layout.separator()
        draw_preferences(self, context)
        return

    def get_ui_layout_tuple() -> (str, str, str, str, int):
        ui_layout = user_interface.get_layout()
        for tuple in constants.LAYOUTS:
            if tuple[0] == ui_layout:
                return tuple
        raise RuntimeError("Could not find project action tuple")

    ui_layout = get_ui_layout_tuple()

    draw_method = _get_ui_layout_draw_method(ui_layout)
    if draw_method is not None:
        box = layout.box()
        #title = box.row()
        #title.alignment = 'CENTER'
        #title.label(text=ui_layout[1])
        #box.separator()

        draw_method(box, context)

    layout.separator()

    draw_logging_console(self, context)

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

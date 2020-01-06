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
from gridmarkets_blender_addon.menus import *
from gridmarkets_blender_addon.operators.set_ui_layout import GRIDMARKETS_OT_set_layout


def _draw_header_button(layout: bpy.types.UILayout, t):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    user_interface = plugin.get_user_interface()
    ui_layout = user_interface.get_layout()

    row = layout.row()
    row.operator(GRIDMARKETS_OT_set_layout.bl_idname, text=t[1]).layout = t[0]
    if ui_layout == t[0]:
        row.enabled = False


def draw_header(self, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    layout: bpy.types.UILayout = self.layout
    user_interface = plugin.get_user_interface()
    signed_in_user = plugin.get_api_client().get_signed_in_user()

    row = layout.row()

    draw_header_menus(row, context)

    # signed in indicator
    sub = row.row(align=True)

    if user_interface.is_running_operation():
        sub.label(text=user_interface.get_running_operation_message(),
                  icon_value=utils_blender.get_spinner(user_interface.get_running_operation_spinner()).icon_id)

    # right aligned content
    layout.separator_spacer()

    _draw_header_button(layout, constants.REMOTE_PROJECTS_LAYOUT_TUPLE)
    _draw_header_button(layout, constants.JOB_PRESETS_LAYOUT_TUPLE)

    row = layout.row(align=True)
    row.alignment = 'RIGHT'
    if signed_in_user:
        row.label(text=signed_in_user.get_auth_email())
        row.menu(GRIDMARKETS_MT_auth_menu.bl_idname, text="", icon_value=GRIDMARKETS_MT_auth_menu.get_icon())
    else:
        row.label(text="Not signed in", icon=constants.ICON_ERROR)

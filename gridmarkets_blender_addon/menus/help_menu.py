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

__all__ = ['GRIDMARKETS_MT_help_menu']

import bpy
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.operators.copy_support_email import GRIDMARKETS_OT_copy_support_email
from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.save_logs_to_file import \
    GRIDMARKETS_OT_save_logs_to_file


class GRIDMARKETS_MT_help_menu(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_help_menu"
    bl_label = "Help"
    icon = constants.ICON_HELP

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.url_open", text="FAQ", icon='URL', ).url = constants.FAQ_URL
        layout.operator("wm.url_open", text="Blender", icon='URL', ).url = constants.HELP_URL
        layout.operator("wm.url_open", text="Security", icon='URL', ).url = constants.SECURITY_URL

        layout.separator()
        layout.operator("wm.url_open", text="Envoy Logs", icon='URL', ).url = constants.ENVOY_LOGS_URL
        layout.operator(GRIDMARKETS_OT_save_logs_to_file.bl_idname,
                        text="Save Add-on Logs",
                        icon=constants.ICON_SAVE_TO_FILE)

        layout.separator()
        layout.operator(GRIDMARKETS_OT_copy_support_email.bl_idname)
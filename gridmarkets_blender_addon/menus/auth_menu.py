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

__all__ = ['GRIDMARKETS_MT_auth_menu']

import bpy
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.blender_plugin.user_container.operators.sign_out import GRIDMARKETS_OT_sign_out
from gridmarkets_blender_addon.blender_plugin.user_container.operators.show_user_credits import GRIDMARKETS_OT_show_user_credits
from .switch_user_menu import GRIDMARKETS_MT_switch_user_menu


class GRIDMARKETS_MT_auth_menu(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_auth_menu"
    bl_label = "Auth"

    @staticmethod
    def get_icon() -> int:
        from gridmarkets_blender_addon.icon_loader import IconLoader
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        return preview_collection[constants.USER_ICON_ID].icon_id

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        api_client = plugin.get_api_client()

        if api_client.is_user_signed_in():
            signed_in_user = api_client.get_signed_in_user()

            layout = self.layout

            row = layout.row()
            row.label(text=signed_in_user.get_auth_email(), icon_value=self.get_icon())
            row.scale_y = 1.5

            layout.separator()

            # credits
            layout.operator(GRIDMARKETS_OT_show_user_credits.bl_idname)

            layout.separator()

            users = plugin.get_preferences_container().get_user_container().get_all()
            if len(users) > 1:
                layout.menu(GRIDMARKETS_MT_switch_user_menu.bl_idname)

            layout.separator()
            layout.operator(GRIDMARKETS_OT_sign_out.bl_idname)

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

__all__ = ['GRIDMARKETS_MT_switch_user_menu']

import bpy
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.blender_plugin.user_container.operators.switch_user import GRIDMARKETS_OT_switch_user


class GRIDMARKETS_MT_switch_user_menu(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_switch_user_menu"
    bl_label = "Switch User"

    @staticmethod
    def get_icon() -> int:
        from gridmarkets_blender_addon.icon_loader import IconLoader
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        return preview_collection[constants.USER_ICON_ID].icon_id

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        layout = self.layout

        layout.label(text="Switch to user:")
        layout.separator()

        signed_in_user = api_client.get_signed_in_user()
        users = plugin.get_preferences_container().get_user_container().get_all()
        if len(users) > 1:
            for user in users:
                row = layout.row()
                op = row.operator(GRIDMARKETS_OT_switch_user.bl_idname, text=user.get_auth_email())
                op.auth_email = user.get_auth_email()
                op.auth_accessKey = user.get_auth_key()

                # prevent switching to the current user
                if user.get_auth_email() == signed_in_user.get_auth_email():
                    row.enabled = False
        else:
            layout.label("You have no other saved profiles to switch to.", icon=constants.ICON_ERROR)

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


class GRIDMARKETS_OT_show_user_credits(bpy.types.Operator):
    bl_idname = "gridmarkets.show_user_credits"
    bl_label = "Check Available Credits"
    bl_description = "Shows a popup displaying the users available credits"
    bl_options = {"REGISTER"}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        available_credits = api_client.get_available_credits()

        def draw_available_credits_popup(self, context):
            layout = self.layout
            layout.label(text="Credits: " + str(round(available_credits, 2)))

        bpy.context.window_manager.popup_menu(draw_available_credits_popup)

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_show_user_credits,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

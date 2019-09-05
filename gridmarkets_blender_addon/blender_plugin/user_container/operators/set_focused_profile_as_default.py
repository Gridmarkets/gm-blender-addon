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


class GRIDMARKETS_OT_set_focused_profile_as_default(bpy.types.Operator):
    bl_idname = "gridmarkets.set_focused_profile_as_default"
    bl_label = "Set as default"
    bl_description = "Indicates whether or not the add-on will automatically sign-in using this profile"
    bl_options = {"REGISTER"}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        user_container = plugin.get_preferences_container().get_user_container()

        default_user = user_container.get_default_user()
        focused_user = user_container.get_focused_item()

        if focused_user == default_user:
            user_container.set_default_user(None)
        else:
            user_container.set_focused_as_default_user()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_set_focused_profile_as_default,
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

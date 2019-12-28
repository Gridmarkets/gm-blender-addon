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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_set_project_upload_method(bpy.types.Operator):
    bl_idname = "gridmarkets.set_project_upload_method"
    bl_label = "Set upload method"
    bl_options = {'INTERNAL'}

    method: bpy.props.EnumProperty(
        name="Upload Method",
        items=constants.PROJECT_ACTION_OPERATORS,
    )

    def execute(self, context):
        from gridmarkets_blender_addon import utils_blender
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        user_interface = plugin.get_user_interface()
        user_interface.set_project_upload_method(self.method)

        utils_blender.force_redraw_addon()
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_set_project_upload_method,
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

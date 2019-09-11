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
from bpy_extras.io_utils import ExportHelper
from gridmarkets_blender_addon import constants, utils_blender


class GRIDMARKETS_OT_save_logs_to_file(bpy.types.Operator, ExportHelper):
    bl_idname = "gridmarkets.save_logs_to_file"
    bl_label = "Save logs to file"
    bl_description = "Copy all the logs (Including system information logs) to a user specified file"
    bl_options = {"REGISTER"}

    filename_ext = ".txt"

    DEFAULT_FILTER = "*.txt"
    DEFAULT_NAME = "GM_blender_logs"

    filter_glob: bpy.props.StringProperty(
        default= DEFAULT_FILTER,
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filepath: bpy.props.StringProperty(
        default= DEFAULT_NAME,
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        plugin.get_logging_coordinator().save_logs_to_file(self.filepath)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_save_logs_to_file,
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

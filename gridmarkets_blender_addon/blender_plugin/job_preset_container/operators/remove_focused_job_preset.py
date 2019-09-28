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


class GRIDMARKETS_OT_remove_focused_job_preset(bpy.types.Operator):
    bl_idname = "gridmarkets.remove_focused_job_preset"
    bl_label = "Remove Focused Job Preset"
    bl_description = "Removes the focuesed Job Preset from the Job Presets list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset
        from gridmarkets_blender_addon import utils, constants

        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()
        job_definitions = api_schema.get_job_definitions()

        job_preset_container = plugin.get_preferences_container().get_job_preset_container()
        focused_job_preset = job_preset_container.get_focused_item()

        if focused_job_preset:
            job_preset_container.remove(focused_job_preset)
            focused_job_preset.unregister_props()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_remove_focused_job_preset,
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

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


class GRIDMARKETS_OT_toggle_job_preset_locked_state(bpy.types.Operator):
    bl_idname = "gridmarkets.toggle_job_preset_locked_state"
    bl_label = "Toggle job Preset locked state"
    bl_description = "Toggles the lock on a job preset"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon import utils_blender

        plugin = PluginFetcher.get_plugin()
        job_preset_container = plugin.get_preferences_container().get_job_preset_container()
        job_preset = job_preset_container.get_focused_item()

        if job_preset is not None:
            job_preset.toggle_locked_state()
            utils_blender.force_redraw_addon()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_toggle_job_preset_locked_state,
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

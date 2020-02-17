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

from gridmarkets_blender_addon.property_groups.main_props import get_job_options, get_selected_job_option


class GRIDMARKETS_OT_remove_focused_job_preset(bpy.types.Operator):
    bl_idname = "gridmarkets.remove_focused_job_preset"
    bl_label = "Remove Focused Job Preset"
    bl_description = "Removes the focused Job Preset from the Job Presets list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher

        plugin = PluginFetcher.get_plugin()
        job_preset_container = plugin.get_preferences_container().get_job_preset_container()
        focused_job_preset = job_preset_container.get_focused_item()

        if focused_job_preset:
            index = job_preset_container.get_index(focused_job_preset)

            if index == 0:
                new_index = index + 1
            else:
                new_index = index - 1

            item = job_preset_container.get_at(new_index)
            if item:
                job_preset_container.focus_item(item)

            job_preset_container.remove(focused_job_preset)
            focused_job_preset.unregister_props()

            # get selected job preset option
            selected_job_preset_option = get_selected_job_option(context)

            if selected_job_preset_option:
                # If we just deleted the selected job preset option
                if selected_job_preset_option.get_id_number() == focused_job_preset.get_id_number():
                    # then reset the selected job preset option to another value
                    job_preset_options = get_job_options(context.scene, context)
                    if job_preset_options:
                        context.scene.props.job_options = job_preset_options[0][0]

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

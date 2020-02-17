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


class GRIDMARKETS_OT_set_focused_job_preset(bpy.types.Operator):
    bl_idname = "gridmarkets.set_focused_job_preset"
    bl_label = "Edit Job Preset"
    bl_description = "Focuses the provided job preset and optionally switches to the Job preset layout"
    bl_options = {"REGISTER", "UNDO"}

    job_preset_index : bpy.props.IntProperty()
    set_layout: bpy.props.BoolProperty(
        default=True
    )

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon import utils_blender

        plugin = PluginFetcher.get_plugin()
        job_preset_container = plugin.get_preferences_container().get_job_preset_container()

        job_preset = job_preset_container.get_at(self.job_preset_index)
        if job_preset is not None:
            job_preset_container.focus_item(job_preset)

            if self.set_layout:
                bpy.ops.gridmarkets.set_layout(layout='job_presets')

            utils_blender.force_redraw_addon()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_set_focused_job_preset,
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

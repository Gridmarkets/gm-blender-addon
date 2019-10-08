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


class GRIDMARKETS_MT_new_job_preset(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_new_job_preset"
    bl_label = "Create a new Job Preset"

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.create_new_job_preset import \
            GRIDMARKETS_OT_create_new_job_preset
        from gridmarkets_blender_addon.blender_plugin.api_schema.api_schema import get_icon_for_job_definition

        layout = self.layout
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()
        job_definitions = api_schema.get_job_definitions()

        for job_definition in job_definitions:
            icon = get_icon_for_job_definition(job_definition)

            op = layout.operator(GRIDMARKETS_OT_create_new_job_preset.bl_idname, text=job_definition.get_display_name(),
                                 icon=icon[0], icon_value=icon[1])
            op.job_definition_id = job_definition.get_definition_id()

        layout.separator()
        layout.label(text="Job Definitions")


classes = (
    GRIDMARKETS_MT_new_job_preset,
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

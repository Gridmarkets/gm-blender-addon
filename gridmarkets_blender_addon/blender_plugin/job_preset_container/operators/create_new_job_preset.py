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
from gridmarkets_blender_addon.meta_plugin import utils
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_create_new_job_preset(bpy.types.Operator):
    bl_idname = "gridmarkets.create_new_job_preset"
    bl_label = "Create new job Preset"
    bl_description = "Creates a new Job Preset and adds it to the Job Presets list"
    bl_options = {"REGISTER", "UNDO"}

    job_definition_id: bpy.props.StringProperty(
        name="Job Definition Id",
        description="The unique identifier for the job definition that is being used to create a job preset from"
    )

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset

        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_cached_api_schema()
        job_definitions = api_schema.get_job_definitions()

        if self.job_definition_id is None:
            self.report({'ERROR_INVALID_INPUT'}, "Job Definition ID must not be 'None'.")
            return {'FINISHED'}

        for job_definition in job_definitions:
            if job_definition.get_definition_id() == self.job_definition_id:
                job_preset_container = plugin.get_preferences_container().get_job_preset_container()
                job_preset_items = bpy.context.scene.props.job_preset_container.items

                name_prefix = (job_definition.get_display_name() + "_Job_Preset_").replace(' ', '_')
                name = utils.create_unique_object_name(job_preset_items, name_prefix=name_prefix)
                job_preset = JobPreset(name, job_definition)

                job_preset_container.append(job_preset)
                return {'FINISHED'}
        else:
            self.report({'ERROR_INVALID_INPUT'},
                        "Job Definition ID must match a know Job Definition. It was '" + str(
                            self.job_definition_id) + "'.")
            return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_create_new_job_preset,
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

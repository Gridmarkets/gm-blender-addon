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


class GRIDMARKETS_OT_set_inference_source(bpy.types.Operator):
    bl_idname = "gridmarkets.set_inference_source"
    bl_label = "Set Inference Source"
    bl_description = "Sets the source from which to infer the job attributes value"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    inference_source: bpy.props.StringProperty()
    job_preset_prop_id: bpy.props.StringProperty()
    job_attribute_key: bpy.props.StringProperty()

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher

        if self.inference_source:
            plugin = PluginFetcher.get_plugin()
            job_preset_container = plugin.get_preferences_container().get_job_preset_container()
            for job_preset in job_preset_container.get_all():
                if job_preset.get_id() == self.job_preset_prop_id:
                    job_attribute = job_preset.get_job_definition().get_attribute_with_key(self.job_attribute_key)
                    job_preset.set_attribute_active_inference_source(job_attribute, self.inference_source)
                    break
            else:
                raise ValueError("Could not find job preset")

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_set_inference_source,
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

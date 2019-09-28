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

from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset as MetaJobPreset
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition


class JobPreset(MetaJobPreset):
    def __init__(self, name: str, id: str, job_definition: JobDefinition):
        MetaJobPreset.__init__(self, name, id, job_definition)
        self._register_props()

    def _reset_properties_to_default(self):
        import bpy
        from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType
        from gridmarkets_blender_addon.blender_plugin.job_attribute.job_attribute import get_default_value

        scene = bpy.context.scene
        job_preset_props = getattr(scene, self.get_prop_id())

        job_definition = self.get_job_definition()
        for job_attribute in job_definition.get_attributes():
            if job_attribute.get_type() != AttributeType.NULL:
                setattr(job_preset_props, job_attribute.get_key(), get_default_value(job_attribute))

    def _register_props(self):
        import bpy
        from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType, EnumAttributeType

        job_definition = self.get_job_definition()

        properties = {}

        for job_attribute in job_definition.get_attributes():

            key = job_attribute.get_key()
            display_name = job_attribute.get_display_name()
            description = job_attribute.get_description()
            attribute_type = job_attribute.get_type()
            default_value = job_attribute.get_default_value()

            if attribute_type == AttributeType.STRING:
                properties[key] = bpy.props.StringProperty(
                    name=display_name,
                    description=description,
                    default=default_value,
                    options={'SKIP_SAVE'}
                )

            elif attribute_type == AttributeType.ENUM:

                enum_attribute: EnumAttributeType = job_attribute

                items = []
                enum_items = enum_attribute.get_items()

                for enum_item in enum_items:
                    items.append((enum_item.get_key(), enum_item.get_display_name(), enum_item.get_description()))

                properties[key] = bpy.props.EnumProperty(
                    name=display_name,
                    description=description,
                    items=items,
                    default=default_value.get_key(),
                    options={'SKIP_SAVE'}
                )

            elif attribute_type == AttributeType.BOOLEAN:
                properties[key] = bpy.props.BoolProperty(
                    name=display_name,
                    description=description,
                    default=default_value,
                    options={'SKIP_SAVE'}
                )

            elif attribute_type == AttributeType.INTEGER:
                properties[key] = bpy.props.IntProperty(
                    name=display_name,
                    description=description,
                    default=default_value,
                    options={'SKIP_SAVE'}
                )

        # register property group
        self._property_group_class = type("GRIDMARKETS_PROPS_job_preset_attributes",
                                          (bpy.types.PropertyGroup,),
                                          {"__annotations__": properties})

        bpy.utils.register_class(self._property_group_class)

        setattr(bpy.types.Scene,
                self.get_prop_id(),
                bpy.props.PointerProperty(type=self._property_group_class))

    def unregister_props(self):
        import bpy

        # reset values to their defaults otherwise new JobPresets with the same id will use these old values
        self._reset_properties_to_default()
        bpy.utils.unregister_class(self._property_group_class)
        delattr(bpy.types.Scene, self.get_prop_id())

    def get_prop_id(self):
        return "job_preset_" + self.get_id()

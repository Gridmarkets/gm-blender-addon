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

import typing

from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset as MetaJobPreset
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute
from gridmarkets_blender_addon import utils, utils_blender


class JobPreset(MetaJobPreset):
    INFERENCE_SOURCE_KEY = "Attribute Inference Source"
    JOB_PRESET_ID_PREFIX = "job_preset_"

    FRAME_RANGE_COLLECTION = "_collection"
    FRAME_RANGE_FOCUSED = "_focused"

    def __init__(self, name: str, job_definition: JobDefinition, is_locked=False):
        self._name = name

        job_preset_items = bpy.context.scene.props.job_preset_container.items
        self._id_number = utils.get_unique_id(job_preset_items)
        self._id = JobPreset.JOB_PRESET_ID_PREFIX + str(self._id_number)
        self._job_definition = job_definition

        self._job_preset_attributes = list(map(lambda job_attribute: JobPresetAttribute(self, job_attribute),
                                               job_definition.get_attributes()))

        self._is_locked = is_locked

        self._property_group_class = None
        self.register_props()
        self._reset_properties_to_default()

    def _reset_properties_to_default(self):
        import bpy
        from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
        from gridmarkets_blender_addon.meta_plugin.attribute_types import StringSubtype, StringAttributeType

        scene = bpy.context.scene
        job_preset_props = getattr(scene, self.get_id())

        job_definition = self.get_job_definition()
        for job_attribute in job_definition.get_attributes():
            attribute = job_attribute.get_attribute()
            attribute_type = attribute.get_type()
            if attribute_type != AttributeType.NULL:

                # subtypes must be handled differently
                if attribute_type == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FRAME_RANGES.value:
                    setattr(job_preset_props, attribute.get_key() + self.FRAME_RANGE_FOCUSED, 0)

                    collection = getattr(job_preset_props, attribute.get_key() + self.FRAME_RANGE_COLLECTION)
                    collection.clear()

                    frame_range = collection.add()
                    frame_range.name = "Default frame range"
                    frame_range.enabled = True
                    frame_range.frame_start = 1
                    frame_range.frame_end = 256
                    frame_range.frame_step = 1
                else:
                    default_value = attribute.get_default_value()

                    if default_value is not None:
                        setattr(job_preset_props, attribute.get_key(), default_value)

                # reset inference source to default
                inference_sources = job_attribute.get_inference_sources()
                setattr(job_preset_props, self.INFERENCE_SOURCE_KEY + attribute.get_key(), inference_sources[0].get_id())

    def _register_job_attribute(self,
                                job_attribute: JobAttribute,
                                properties: typing.Dict[str, bpy.types.Property]):

        prop_id = job_attribute.get_attribute().get_key()

        # get blender properties for the base attribute
        utils_blender.get_blender_props_for_attribute(job_attribute.get_attribute(), properties, prop_id)

        # get blender properties for the inference source drop down
        inference_source_items = []
        for inference_source in job_attribute.get_inference_sources():
            inference_source_items.append((inference_source.get_id(),
                                           inference_source.get_display_name(),
                                           inference_source.get_description()))

        properties[self.INFERENCE_SOURCE_KEY + prop_id] = bpy.props.EnumProperty(
            name=self.INFERENCE_SOURCE_KEY,
            description="The source to read the attribute value from.",
            items=inference_source_items,
            default=str(job_attribute.get_default_inference_source().get_id()),
            options={'SKIP_SAVE'}
        )

    def register_props(self):
        import bpy
        job_definition = self.get_job_definition()
        properties = {}

        for job_attribute in job_definition.get_attributes():
            self._register_job_attribute(job_attribute, properties)

        # register property group
        self._property_group_class = type("GRIDMARKETS_PROPS_job_preset_attributes",
                                          (bpy.types.PropertyGroup,),
                                          {"__annotations__": properties})

        bpy.utils.register_class(self._property_group_class)

        setattr(bpy.types.Scene,
                self.get_id(),
                bpy.props.PointerProperty(type=self._property_group_class))

    def unregister_props(self):
        import bpy

        if self._property_group_class is not None:
            bpy.utils.unregister_class(self._property_group_class)

        delattr(bpy.types.Scene, self.get_id())

    def get_property_group(self):
        import bpy
        return getattr(bpy.context.scene, self.get_id())

    def get_id_number(self) -> int:
        return self._id_number


from gridmarkets_blender_addon.blender_plugin.job_preset_attribute.job_preset_attribute import JobPresetAttribute

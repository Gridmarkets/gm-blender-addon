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

import typing

from gridmarkets_blender_addon.meta_plugin.job_preset_attribute import JobPresetAttribute as MetaJobPresetAttribute
from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute
from gridmarkets_blender_addon.blender_plugin.attribute.attribute import get_value

class JobPresetAttribute(MetaJobPresetAttribute):

    def __init__(self, parent_preset: 'JobPreset', job_attribute: JobAttribute,
                 inference_source: InferenceSource = None,
                 value: any = None):

        MetaJobPresetAttribute.__init__(self, parent_preset, job_attribute, inference_source=inference_source,
                                        value=value)

    def get_parent_preset(self) -> 'JobPreset':
        return MetaJobPresetAttribute.get_parent_preset(self)

    def get_value(self):
        job_preset = self.get_parent_preset()
        property_group = job_preset.get_property_group()
        attribute = self.get_job_attribute().get_attribute()
        prop_id = self.get_key()
        return get_value(property_group, attribute, prop_id)

    def set_value(self, value: any) -> None:
        raise NotImplementedError
        #MetaJobPresetAttribute.set_value(self, value)

    def get_inference_source(self) -> InferenceSource:
        job_preset = self.get_parent_preset()
        inference_source_id = getattr(job_preset.get_property_group(), JobPreset.INFERENCE_SOURCE_KEY + self.get_key())
        return InferenceSource.get_inference_source(inference_source_id)

    def set_inference_source(self, inference_source) -> None:
        job_preset = self.get_parent_preset()
        setattr(job_preset.get_property_group(), JobPreset.INFERENCE_SOURCE_KEY + self.get_key(),
                inference_source.get_id())


# avoid circular imports by importing at end
from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset

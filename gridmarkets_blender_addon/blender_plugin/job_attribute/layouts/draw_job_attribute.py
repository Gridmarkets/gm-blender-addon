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

from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute
from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset


def draw_job_attribute(self, context, job_preset: JobPreset, job_attribute: JobAttribute, col1, col2, col3):
    from types import SimpleNamespace
    from gridmarkets_blender_addon.blender_plugin.job_attribute.operators.set_inference_source import \
        GRIDMARKETS_OT_set_inference_source
    from gridmarkets_blender_addon.blender_plugin.attribute.layouts.draw_attribute_input import draw_attribute_input
    from gridmarkets_blender_addon.meta_plugin.attribute_inference_source import AttributeInferenceSource
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
    from gridmarkets_blender_addon.meta_plugin.errors.invalid_attribute_error import InvalidAttributeError

    scene = context.scene
    props = scene.props

    job_preset_props = getattr(scene, job_preset.get_prop_id())

    attribute = job_attribute.get_attribute()
    attribute_type = attribute.get_type()

    if attribute_type == AttributeType.NULL:
        return

    inference_sources = job_attribute.get_inference_sources()
    inference_source = getattr(job_preset_props, JobPreset.INFERENCE_SOURCE_KEY + attribute.get_key())

    display_name_row = col1.row()
    display_name_row.label(text=attribute.get_display_name() + ":")

    input_row = col2.column()

    if inference_source == AttributeInferenceSource.CONSTANT.value:
        input_row.prop(job_preset_props, attribute.get_key(), text="")
        input_row.enabled = False

    elif inference_source == AttributeInferenceSource.APPLICATION.value:
        input_row.label(text=str(job_preset.get_attribute_value(job_attribute)))

    elif inference_source == AttributeInferenceSource.USER_DEFINED.value:
        draw_attribute_input(SimpleNamespace(layout=input_row),
                             context,
                             job_preset_props,
                             attribute)

    elif inference_source == AttributeInferenceSource.PROJECT.value:
        input_row.prop(props, "project_defined", text="")
        input_row.enabled = False

    col3.alignment="EXPAND"
    col3.prop(job_preset_props, JobPreset.INFERENCE_SOURCE_KEY + job_attribute.get_attribute().get_key(),
                           text="")
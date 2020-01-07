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

from gridmarkets_blender_addon.meta_plugin.job_preset_attribute import JobPresetAttribute


def draw_job_preset_attribute(layout, context, job_preset_attribute: JobPresetAttribute, col1, key_column, col2, col3):
    from types import SimpleNamespace
    from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.attribute.layouts.draw_attribute_input import draw_attribute_input
    from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType

    plugin = PluginFetcher.get_plugin()
    scene = context.scene
    props = scene.props

    job_preset = job_preset_attribute.get_parent_preset()
    is_locked = job_preset.is_locked()
    job_attribute = job_preset_attribute.get_job_attribute()

    job_preset_props = getattr(scene, job_preset.get_id())

    attribute = job_attribute.get_attribute()
    attribute_type = attribute.get_type()

    if attribute_type == AttributeType.NULL:
        return

    inference_source = job_preset_attribute.get_inference_source()

    display_name_row = col1.row()
    display_name_row.label(text=attribute.get_display_name() + ":")

    if plugin.get_user_interface().get_show_hidden_job_preset_attributes():
        key_row = key_column.row()
        key_row.enabled = False
        key_row.label(text=attribute.get_key())

    input_row = col2.column()

    if inference_source == InferenceSource.get_constant_inference_source():
        input_row.prop(job_preset_props, attribute.get_key(), text="")
        input_row.enabled = False

    elif inference_source == InferenceSource.get_application_inference_source():
        input_row.label(text=str(job_preset_attribute.eval(plugin=plugin)))

    elif inference_source == InferenceSource.get_user_defined_inference_source():
        draw_attribute_input(SimpleNamespace(layout=input_row),
                             context,
                             job_preset_props,
                             attribute)

    elif inference_source == InferenceSource.get_project_inference_source():
        input_row.prop(props, "project_defined", text="")
        input_row.enabled = False

    col3.alignment="EXPAND"
    col3.prop(job_preset_props, JobPreset.INFERENCE_SOURCE_KEY + job_preset_attribute.get_key(), text="")
    col3.enabled = len(job_attribute.get_inference_sources()) > 1

    # disable input and inference source drop down if job preset is locked
    if is_locked:
        input_row.enabled = False
        col3.enabled = False

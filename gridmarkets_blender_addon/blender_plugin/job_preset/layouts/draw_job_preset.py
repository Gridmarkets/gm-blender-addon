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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_open_inference_source_help(bpy.types.Operator):
    bl_idname = "gridmarkets.open_inference_source_help"
    bl_label = "Open Inference Source Help"

    def invoke(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource

        def draw_help(self, layout):
            layout = self.layout
            layout.scale_y = 0.8

            layout.alignment = "EXPAND"
            layout.label(text="Inference Source Help", icon=constants.ICON_INFO)
            layout.label(text="Some Job Preset attributes let you choose between different inference sources. The possible source types are:")
            layout.separator()

            inference_sources = InferenceSource.get_all_inference_source_types()
            for inference_source in inference_sources:
                layout.label(text=inference_source.get_display_name() + ':')
                description_row = layout.row()
                description_row.enabled = False
                description_row.label(text=inference_source.get_description())
                layout.separator()

        context.window_manager.popover(draw_help, ui_units_x=30)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_open_inference_source_help,
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


def draw_job_preset(self, context):
    from gridmarkets_blender_addon import constants
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.api_schema.api_schema import get_icon_for_job_definition
    from gridmarkets_blender_addon.blender_plugin.job_attribute.layouts.draw_job_attribute import draw_job_attribute
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType

    layout = self.layout
    scene = context.scene

    plugin = PluginFetcher.get_plugin()
    job_preset_container = plugin.get_preferences_container().get_job_preset_container()
    job_preset = job_preset_container.get_focused_item()

    if job_preset:
        job_definition = job_preset.get_job_definition()
        icon = get_icon_for_job_definition(job_definition)

        layout.label(text=job_preset.get_name(), icon=icon[0], icon_value=icon[1])

        attributes = job_definition.get_attributes()

        box = layout.box()
        col = box.column()
        split1_factor = 0.2

        def _get_columns(parent_layout):
            job_attribute_row = parent_layout.row()

            # attribute display name column
            split = job_attribute_row.split(factor=split1_factor)
            col1 = split.column(align=True)
            temp_col = split.column()
            row = temp_col.row(align=True)

            split = row.split(factor=0.8)
            # attribute input column
            col2 = split.column()

            # attribute inference source column
            col3 = split.column()

            return col1, col2, col3

        columns = _get_columns(col)
        columns[0].label(text="Attribute Name")
        columns[0].enabled = False

        columns[1].label(text="Input Field")
        columns[1].enabled = False

        source_header_row = columns[2].row(align=True)
        source_header_row_label = source_header_row.row()
        source_header_row_label.enabled = False
        source_header_row_label.label(text="Source")

        source_header_row_operator = source_header_row.row()
        source_header_row_operator.operator(GRIDMARKETS_OT_open_inference_source_help.bl_idname, text="", icon=constants.ICON_INFO, emboss=False)

        col.separator()

        for job_attribute in attributes:
            if job_attribute.get_attribute().get_type() == AttributeType.NULL:
                continue

            if not plugin.get_user_interface().get_show_hidden_job_preset_attributes():
                if len(job_attribute.get_inference_sources()) == 1:
                    from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource

                    if job_attribute.get_inference_sources()[0] == InferenceSource.get_constant_inference_source():
                        continue

                    if job_attribute.get_inference_sources()[0] == InferenceSource.get_project_inference_source():
                        continue

            columns = _get_columns(col)
            draw_job_attribute(self, context, job_preset, job_attribute, columns[0], columns[1], columns[2])

        col.separator()

        row = col.row(align=True)
        row.alignment = "RIGHT"
        row.label(text="Show Hidden Job Preset Attributes")
        row.prop(scene.props.user_interface, "show_hidden_job_preset_attributes", text="")

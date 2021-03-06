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
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource
from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.toggle_job_preset_locked_state import \
    GRIDMARKETS_OT_toggle_job_preset_locked_state

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset
    from gridmarkets_blender_addon.meta_plugin.gridmarkets.remote_project import RemoteProject


class GRIDMARKETS_OT_open_inference_source_help(bpy.types.Operator):
    bl_idname = "gridmarkets.open_inference_source_help"
    bl_label = "Open Inference Source Help"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource

        def draw_help(self, context):
            layout = self.layout
            layout.scale_y = 0.8

            layout.alignment = "EXPAND"
            layout.label(text="Inference Source Help", icon=constants.ICON_INFO)
            layout.label(
                text="Some Job Preset attributes let you choose between different inference sources. The possible source types are:")
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


def _get_columns(layout: bpy.types.UILayout):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    split_factor = 0.3 if plugin.get_user_interface().get_show_hidden_job_preset_attributes() else 0.2

    job_attribute_row = layout.row()

    split = job_attribute_row.split(factor=split_factor)

    temp_col = split.column(align=True)
    row = temp_col.row(align=True)

    # attribute display name column
    col1 = row.column(align=True)

    # attribute key column
    key_column = row.column() if plugin.get_user_interface().get_show_hidden_job_preset_attributes() else None

    temp_col = split.column()
    row = temp_col.row(align=True)
    split = row.split(factor=0.8)

    # attribute input column
    col2 = split.column()

    # attribute inference source column
    col3 = split.column()

    return col1, col2, col3, key_column


def _draw_job_preset_headers(layout: bpy.types.UILayout):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    columns = _get_columns(layout)
    columns[0].label(text="Attribute Name")
    columns[0].enabled = False

    columns[1].label(text="Input Field")
    columns[1].enabled = False

    source_header_row = columns[2].row(align=True)
    source_header_row_label = source_header_row.row()
    source_header_row_label.enabled = False
    source_header_row_label.label(text="Source")

    source_header_row_operator = source_header_row.row()
    source_header_row_operator.operator(GRIDMARKETS_OT_open_inference_source_help.bl_idname, text="",
                                        icon=constants.ICON_INFO, emboss=False)

    if plugin.get_user_interface().get_show_hidden_job_preset_attributes():
        columns[3].label(text="Attribute Key")
        columns[3].enabled = False


def draw_job_preset(layout: bpy.types.UILayout,
                    context: bpy.types.Context,
                    job_preset: typing.Optional['JobPreset'] = None,
                    remote_project: typing.Optional['RemoteProject'] = None):

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.job_definition import get_blender_icon_tuple_for_job_definition
    from gridmarkets_blender_addon.blender_plugin.job_preset_attribute.layouts.draw_job_preset_attribute import \
        draw_job_preset_attribute
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType

    scene = context.scene

    plugin = PluginFetcher.get_plugin()

    if job_preset is None:
        job_preset_container = plugin.get_preferences_container().get_job_preset_container()
        job_preset = job_preset_container.get_focused_item()

    if job_preset:
        job_definition = job_preset.get_job_definition()
        icon = get_blender_icon_tuple_for_job_definition(job_definition)

        box = layout.box()

        row = box.row(align=True)

        row2 = row.row()
        row2.alignment = 'LEFT'
        row2.label(text=job_preset.get_name(), icon=icon[0], icon_value=icon[1])

        row2 = row.row()
        row2.alignment = 'RIGHT'
        row3 = row2.row()
        row3.alignment = 'RIGHT'
        row3.enabled = False
        row3.label(text="Based on job definition \"" + job_preset.get_job_definition().get_display_name() + "\"")

        locked_icon = constants.ICON_LOCKED if job_preset.is_locked() else constants.ICON_UNLOCKED

        row2.emboss = "PULLDOWN_MENU"
        toggle_locked_state_btn = row2.operator(GRIDMARKETS_OT_toggle_job_preset_locked_state.bl_idname,
                                                icon=locked_icon,
                                                text="Toggle Lock")
        toggle_locked_state_btn.job_preset_id = job_preset.get_id()

        col = box.column()

        _draw_job_preset_headers(col)

        col.separator()

        for job_preset_attribute in job_preset.get_job_preset_attributes():

            job_attribute = job_preset_attribute.get_job_attribute()
            if job_attribute.get_attribute().get_type() == AttributeType.NULL:
                continue

            # If hidden job preset attributes are not visible
            if not plugin.get_user_interface().get_show_hidden_job_preset_attributes():

                # Then hide attributes which only have one inference source and it is either constant or project defined
                # We hide these since they are not modifiable by the user so they can be hidden.
                if len(job_attribute.get_inference_sources()) == 1:
                    if job_preset_attribute.get_inference_source() == InferenceSource.get_constant_inference_source():
                        continue

                    if job_preset_attribute.get_inference_source() == InferenceSource.get_project_inference_source():
                        continue

            columns = _get_columns(col)

            if remote_project is not None and \
                    job_preset_attribute.get_inference_source() == InferenceSource.get_project_inference_source():
                project_inferred_value = job_preset_attribute.eval(plugin, remote_project)
            else:
                project_inferred_value = None

            draw_job_preset_attribute(layout, context, job_preset_attribute, columns[0], columns[3], columns[1],
                                      columns[2], project_inferred_value=project_inferred_value)

        col.separator()

        row = col.row(align=True)

        row2 = row.row()
        row2.alignment = "RIGHT"
        row2.label(text="Show Hidden Job Preset Attributes")
        row2.prop(scene.props.user_interface, "show_hidden_job_preset_attributes", text="")

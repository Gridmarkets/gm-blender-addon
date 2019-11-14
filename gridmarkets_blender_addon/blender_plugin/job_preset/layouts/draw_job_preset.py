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
        columns[1].label(text="Input Field")
        columns[2].label(text="Source")
        for column in columns:
            column.enabled = False

        for job_attribute in attributes:
            columns = _get_columns(col)
            if job_attribute.get_attribute().get_type() != AttributeType.NULL:
                draw_job_attribute(self, context, job_preset, job_attribute, columns[0], columns[1], columns[2])

        col.separator()
        col.label(text="Some Job Preset attributes let you choose between different sources. These Sources Include:",
                  icon=constants.ICON_INFO)

        indent = " " * 8

        def _draw_source_hint(source_name: str, source_description: str):
            row = col.row(align=True)

            sub = row.row(align=True)
            sub.ui_units_x = 10

            sub.alignment="LEFT"
            sub.label(text=indent + "- " + source_name + ":")

            sub = row.row(align=True)
            sub.alignment="EXPAND"
            sub.enabled = False
            sub.label(text=source_description)

        _draw_source_hint("Application (A)", "The value is inferred from the application.")
        _draw_source_hint("User Input Field (U)", "The value is read from the provided input field.")
        _draw_source_hint("Project Inferred Value (P)", "The value will be read from the project's attributes when you submit.")
        _draw_source_hint("Constant (C)","Uses a pre-defined constant value.")

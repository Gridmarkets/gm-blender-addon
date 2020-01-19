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

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.pack_blend_file import GRIDMARKETS_OT_pack_blend_file


def draw_pack_external_project(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    scene = context.scene
    props = scene.props

    box = layout.box()

    # blend file
    split = box.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Blend File:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(props, "blend_file_path", text="")

    row = col2.row()
    row.label(text="The path to your .blend file that you want to pack.")
    row.enabled = False

    # export path
    split = box.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Export Path:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(props, "export_path", text="")

    row = col2.row()
    row.label(text="The path to save your packed scene to.")
    row.enabled = False

    box.separator()

    row = box.row()
    row.operator(GRIDMARKETS_OT_pack_blend_file.bl_idname)
    row.enabled = not plugin.get_user_interface().is_running_operation()
    row.scale_y = 2.5

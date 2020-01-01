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

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.pack_current_scene import GRIDMARKETS_OT_pack_current_scene


def draw_pack_current_scene(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    props = scene.props

    # export path
    split = layout.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Export Path:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(props, "export_path", text="")

    row = col2.row()
    row.label(text="The path to save your packed scene to.")
    row.enabled = False

    layout.separator()

    row = layout.row()
    row.operator(GRIDMARKETS_OT_pack_current_scene.bl_idname)
    row.scale_y = 2.5

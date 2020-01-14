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
from gridmarkets_blender_addon.blender_plugin.project_attribute.layouts import draw_project_attribute
from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import RejectedTransitionInputError
from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_packed_project import GRIDMARKETS_OT_upload_packed_project


def draw_upload_packed_project(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    props = scene.props

    # export path
    split = layout.split(factor=constants.PROJECT_ATTRIBUTE_SPLIT_FACTOR)
    col1 = split.column()
    col1.label(text="Root Directory:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(props, "root_directory", text="")

    row = col2.row()
    row.label(text="The to the root of your packed project. All external assets must be inside this directory.")
    row.enabled = False

    # upload_all_files_in_root
    split = layout.split(factor=constants.PROJECT_ATTRIBUTE_SPLIT_FACTOR)
    col1 = split.column()
    col1.label(text="Upload Everything:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(props, "upload_all_files_in_root", text="")

    row = col2.row()
    row.label(text="Select to upload all files in the root directory. Otherwise only known files will be uploaded.")
    row.enabled = False

    #####################
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    root = plugin.get_api_client().get_api_schema().get_root_project_attribute()

    try:
        draw_project_attribute(layout, context, root)
        enabled = True

    except RejectedTransitionInputError as e:
        layout.separator()
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        row.label(text="Warning: Project settings are invalid. " + e.user_message)
        enabled = False

    layout.separator()

    row = layout.row()
    row.operator(GRIDMARKETS_OT_upload_packed_project.bl_idname)
    row.scale_y = 2.5
    row.enabled = enabled

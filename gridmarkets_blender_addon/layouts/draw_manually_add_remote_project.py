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

from gridmarkets_blender_addon.blender_plugin.project_attribute.layouts import *
from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.add_remote_project import \
    GRIDMARKETS_OT_add_remote_project
from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.refresh_project_list import \
    GRIDMARKETS_OT_refresh_project_list
from gridmarkets_blender_addon import constants


def _draw_remote_project_prop(layout: bpy.types.UILayout, context: bpy.types.Context):
    split = layout.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Project name:")

    col2 = split.column()
    row = col2.row(align=True)
    row.prop(context.scene.props.remote_project_container, "project_name", text="")
    sub = row.row(align=True)
    sub.alignment="RIGHT"
    sub.operator(GRIDMARKETS_OT_refresh_project_list.bl_idname, text="refresh")

    row = col2.row()
    row.label(text="The name of the existing remote project.")
    row.enabled = False


def draw_manually_add_remote_project(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    api_client = plugin.get_api_client()
    api_schema = api_client.get_cached_api_schema()
    root = api_schema.get_root_project_attribute()

    projects = api_client.get_cached_root_directories()

    box = layout.box()

    # If the user has no projects display a warning message
    if len(projects) == 0:
        col = box.column()
        col.alignment = 'CENTER'

        # warn user that no projects have been found
        row = col.row()
        row.alignment = 'CENTER'
        row.label(text="To use this option you must have already uploaded a project to Envoy. Check for existing " +
                       "projects using the button below.")
        col.separator()

        # draw refresh projects list button
        row = col.row()
        row.alignment = 'CENTER'
        row.operator(GRIDMARKETS_OT_refresh_project_list.bl_idname, text="Check for Existing Projects",
                     icon=constants.ICON_RELOAD)
        return

    enabled = not draw_project_attribute(box, context, root, remote_source=True)

    box.separator()

    row = box.row()
    row.operator(GRIDMARKETS_OT_add_remote_project.bl_idname, text="Add Project Details")
    row.scale_y = 2.5
    row.enabled = enabled

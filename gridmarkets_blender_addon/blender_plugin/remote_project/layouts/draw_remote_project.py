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


def draw_remote_project(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon import constants
    plugin = PluginFetcher.get_plugin()

    remote_project = plugin.get_remote_project_container().get_focused_item()

    if remote_project:
        box = layout.box()

        box.label(text="Project details:")

        split = box.split(factor=0.2)

        col1 = split.column()
        col2 = split.column()

        col1.label(text="Project name:")
        col2.label(text=remote_project.get_name())

        col1.label(text="Root directory:")
        col2.label(text=str(remote_project.get_root_dir()))

        col1.label(text="File Count:")
        col2.label(text=str(len(remote_project.get_files())))

        #col1.label(text="Project Size (bytes):")
        #col2.label(text=str(remote_project.get_size()))

        row = box.row()
        split = row.split(factor=0.2)
        col1 = split.column()
        col2 = split.column()

        col1.label(text="Attributes:")
        col1.scale_y = 1.5

        split2 = col2.box().split(factor=0.2)
        keys = split2.column()
        values = split2.column()

        sub=keys.row()
        sub.label(text="Key name:")
        sub.enabled=False

        sub = values.row()
        sub.label(text="Value:")
        sub.enabled = False

        for key, attribute in remote_project.get_attributes().items():
            keys.label(text=key)
            values.label(text=str(attribute))

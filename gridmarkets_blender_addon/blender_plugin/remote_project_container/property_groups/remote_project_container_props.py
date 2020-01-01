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
from gridmarkets_blender_addon.blender_plugin.remote_project.property_groups.remote_project_props import RemoteProjectProps


def _get_remote_root_directories(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    api_client = plugin.get_api_client()
    projects = api_client.get_cached_root_directories()

    return list(map(lambda project: (project, project, ''), projects))


class RemoteProjectContainerProps(bpy.types.PropertyGroup):

    def _get_focused_remote_project(self):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin is None:
            return -1

        remote_project_container = plugin.get_remote_project_container()
        focused_item = remote_project_container.get_focused_item()

        if focused_item is None:
            return -1

        return remote_project_container.get_index(focused_item)

    def _set_focused_remote_project(self, value):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin:
            remote_project_container = plugin.get_remote_project_container()
            item = remote_project_container.get_at(value)
            remote_project_container.focus_item(item, update_props=False)

    focused_remote_project: bpy.props.IntProperty(
        get=_get_focused_remote_project,
        set=_set_focused_remote_project,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    remote_projects: bpy.props.CollectionProperty(
        type=RemoteProjectProps
    )

    project_name: bpy.props.EnumProperty(
        name="Project Name",
        items=_get_remote_root_directories
    )

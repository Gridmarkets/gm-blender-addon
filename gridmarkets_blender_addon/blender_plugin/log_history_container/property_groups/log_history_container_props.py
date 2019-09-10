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
from gridmarkets_blender_addon.blender_plugin.log_item.property_groups.log_item_props import LogItemProps


class LogHistoryContainerProps(bpy.types.PropertyGroup):

    def _get_focused_logging_item(self):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin is None:
            return -1

        log_history_container = plugin.get_logging_coordinator().get_log_history_container()
        focused_item = log_history_container.get_focused_item()

        if focused_item is None:
            return -1

        return log_history_container.get_index(focused_item)

    def _set_focused_logging_item(self, value):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin:
            log_history_container = plugin.get_logging_coordinator().get_log_history_container()
            item = log_history_container.get_at(value)
            log_history_container.focus_item(item, update_props=False)

    focused_log_item: bpy.props.IntProperty(
        options={'SKIP_SAVE', 'HIDDEN'},
        get=_get_focused_logging_item,
        set=_set_focused_logging_item
    )

    log_history_items: bpy.props.CollectionProperty(
        type=LogItemProps
    )

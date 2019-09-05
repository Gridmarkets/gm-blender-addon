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
from gridmarkets_blender_addon.blender_plugin.user.property_groups.user_props import UserProps


class UserContainerProps(bpy.types.PropertyGroup):

    def _update_focused_user(self, context):
        pass

    def _get_focused_user(self):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin is None:
            return -1

        user_container = plugin.get_preferences_container().get_user_container()
        focused_item = user_container.get_focused_item()

        if focused_item is None:
            return -1

        return user_container.get_index(focused_item)

    def _set_focused_user(self, value):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin:
            user_container = plugin.get_preferences_container().get_user_container()
            item = user_container.get_at(value)
            user_container.focus_item(item, update_prop=False)


    def _update_default_user(self, context):
        pass

    def _get_default_user(self):
        try:
            value = self["default_user"]
        except KeyError:
            value = -1

        return value

    def _set_default_user(self, value):
        self["default_user"] = value

    focused_user: bpy.props.IntProperty(
        options=set(),
        update=_update_focused_user,
        get=_get_focused_user,
        set=_set_focused_user
    )

    default_user: bpy.props.IntProperty(
        options=set(),
        update=_update_default_user,
        get=_get_default_user,
        set=_set_default_user
    )

    user_profiles: bpy.props.CollectionProperty(
        type=UserProps
    )

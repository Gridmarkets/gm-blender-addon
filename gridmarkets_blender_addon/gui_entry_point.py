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
from gridmarkets_blender_addon.layouts.top_bar import draw_top_bar


def register():
    bpy.types.TOPBAR_MT_editor_menus.append(draw_top_bar)

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    PluginFetcher.get_plugin().register_dynamic_props()


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_top_bar)

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin_if_initialised()
    if plugin:
        plugin.unregister_dynamic_props()

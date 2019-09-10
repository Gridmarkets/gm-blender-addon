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

from gridmarkets_blender_addon.meta_plugin.plugin_utils import PluginUtils as MetaPluginUtils


class PluginUtils(MetaPluginUtils):

    def get_application_version(self) -> str:
        ver = bpy.app.version
        return str(ver[0]) + '.' + str(ver[1]) + '.' + str(ver[2])

    def get_sys_info(self) -> str:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        import platform
        import os

        plugin = PluginFetcher.get_plugin()
        plugin_version = plugin.get_version()

        sys_info = "Operating System: " + platform.platform() + os.linesep
        sys_info += "Blender Version: " + self.get_application_version() + os.linesep
        sys_info += "Add-on Version: " + plugin_version.to_string()

        return sys_info

    def copy_to_clipboard(self, value: str) -> None:
        bpy.context.window_manager.clipboard = value

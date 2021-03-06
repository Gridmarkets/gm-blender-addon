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
from gridmarkets_blender_addon.blender_plugin.remote_project import get_blender_icon_tuple_for_remote_project


class GRIDMARKETS_UL_remote_project(bpy.types.UIList):
    bl_idname = "GRIDMARKETS_UL_remote_project"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        remote_project = plugin.get_remote_project_container().get_at(index)
        icons = get_blender_icon_tuple_for_remote_project(remote_project)

        layout.alignment = "LEFT"
        layout.label(text=remote_project.get_name(), icon=icons[0], icon_value=icons[1])


classes = (
    GRIDMARKETS_UL_remote_project,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

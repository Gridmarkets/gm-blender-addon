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
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants


class GRIDMARKETS_UL_remote_project(bpy.types.UIList):
    bl_idname = "GRIDMARKETS_UL_remote_project"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.icon_loader import IconLoader
        plugin = PluginFetcher.get_plugin()

        layout.alignment = "LEFT"

        remote_project = plugin.get_remote_project_container().get_at(index)

        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        product = remote_project.get_attribute(api_constants.API_KEYS.APP)
        if product == api_constants.PRODUCTS.VRAY:
            icon = preview_collection[constants.VRAY_LOGO_ID].icon_id
            layout.label(text=remote_project.get_name(), icon_value=icon)
        elif product == api_constants.PRODUCTS.BLENDER:
            layout.label(text=remote_project.get_name(), icon=constants.ICON_BLENDER)
        else:
            layout.label(text=remote_project.get_name())



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

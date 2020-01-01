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

__all__ = ['GRIDMARKETS_MT_gm_menu']

import bpy
from gridmarkets_blender_addon import constants
from .about_menu import GRIDMARKETS_MT_about_menu


class GRIDMARKETS_MT_gm_menu(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_gm_menu"
    bl_label = ""

    @staticmethod
    def get_icon() -> int:
        from gridmarkets_blender_addon.icon_loader import IconLoader
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        return preview_collection[constants.GRIDMARKETS_LOGO_ID].icon_id

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.url_open", text=constants.COMPANY_NAME, icon='URL',).url = constants.GRIDMARKETS_WEBSITE_URL
        layout.separator()
        layout.menu(GRIDMARKETS_MT_about_menu.bl_idname)
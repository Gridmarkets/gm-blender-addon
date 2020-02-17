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

__all__ = ['GRIDMARKETS_MT_about_menu']

import bpy
from gridmarkets_blender_addon import constants


class GRIDMARKETS_MT_about_menu(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_about_menu"
    bl_label = "About"
    icon = constants.ICON_COLLAPSEMENU

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.url_open", text="Release Notes", icon='URL',).url = constants.RELEASE_NOTES_URL
        layout.separator()
        layout.operator("wm.url_open", text="GitHub", icon='URL',).url = constants.GITHUB_REPO
        layout.separator()
        layout.operator("wm.url_open", text="Licence", icon='URL',).url = constants.LICENCE_URL

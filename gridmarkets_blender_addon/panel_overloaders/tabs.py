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
from gridmarkets_blender_addon.utils_blender import addon_draw_condition
from gridmarkets_blender_addon.layouts.empty import draw_empty
from gridmarkets_blender_addon.panel_overloaders.panel_overloader import PanelOverloader

_instance = None


class TabsOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_tabs,
                         draw_empty,
                         overload_condition=addon_draw_condition)


def register():
    global _instance

    if _instance is None:
        _instance = TabsOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

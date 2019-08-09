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

from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.icon_loader import IconLoader

_old_header_draw = None


def draw_GM_operator(layout, context):
    # get the GridMarkets icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    if utils_blender.get_addon_window():
        text = 'Close ' + constants.COMPANY_NAME + ' add-on'
    else:
        text = 'Open ' + constants.COMPANY_NAME + ' add-on'

    layout.operator(constants.OPERATOR_OPEN_ADDON_ID_NAME, icon_value=iconGM.icon_id, text=text)


def draw_top_bar_menu_options(layout, context):
    """ Draws the top bar button that opens the add-on window

    :param self: The menu instance that's drawing this button
    :type self: bpy.types.Menu
    :param context: The blender context
    :type context: bpy.context
    :rtype: void
    """

    # call the old draw menu method to draw the normal menu elements
    _old_header_draw(layout, context)

    layout.separator()

    # then draw a button to open the GM blender add-on main window
    draw_GM_operator(layout, context)


def register():
    global _old_header_draw
    _old_header_draw = bpy.types.INFO_MT_editor_menus.draw_menus

    bpy.types.INFO_MT_editor_menus.draw_menus = draw_top_bar_menu_options


def unregister():
    bpy.types.INFO_MT_editor_menus.draw_menus = _old_header_draw


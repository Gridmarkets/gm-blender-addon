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

__all__ = ['GRIDMARKETS_MT_about_menu',
           'GRIDMARKETS_MT_auth_menu',
           'GRIDMARKETS_MT_gm_menu',
           'GRIDMARKETS_MT_help_menu',
           'GRIDMARKETS_MT_misc_options',
           'GRIDMARKETS_MT_project_packing_options',
           'GRIDMARKETS_MT_switch_user_menu',
           'GRIDMARKETS_MT_project_upload_options',
           'GRIDMARKETS_MT_submit_options',
           'draw_header_menus']

import bpy
from gridmarkets_blender_addon import constants

from .about_menu import GRIDMARKETS_MT_about_menu
from .auth_menu import GRIDMARKETS_MT_auth_menu
from .gm_menu import GRIDMARKETS_MT_gm_menu
from .help_menu import GRIDMARKETS_MT_help_menu
from .misc_options import GRIDMARKETS_MT_misc_options
from .packing_options import GRIDMARKETS_MT_project_packing_options
from .switch_user_menu import GRIDMARKETS_MT_switch_user_menu
from .upload_options import GRIDMARKETS_MT_project_upload_options
from .submission_options import GRIDMARKETS_MT_submit_options


def draw_header_menus(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.operators.set_ui_layout import GRIDMARKETS_OT_set_layout

    menu_row = layout.row(align=True)
    menu_row.alignment = 'LEFT'

    row = menu_row.row(align=True)
    row.menu(GRIDMARKETS_MT_gm_menu.bl_idname, text="", icon_value=GRIDMARKETS_MT_gm_menu.get_icon())

    row = menu_row.row(align=True)
    row.emboss = 'PULLDOWN_MENU'
    row.scale_x = 0.9
    row.operator(GRIDMARKETS_OT_set_layout.bl_idname, text=GRIDMARKETS_MT_submit_options.bl_label).layout = constants.SUBMISSION_SETTINGS_VALUE

    row = menu_row.row(align=True)
    row.menu(GRIDMARKETS_MT_project_upload_options.bl_idname)

    column = menu_row.column()
    column.menu(GRIDMARKETS_MT_project_packing_options.bl_idname)

    row = menu_row.row(align=True)
    row.menu(GRIDMARKETS_MT_misc_options.bl_idname)

    row = menu_row.row(align=True)
    row.menu(GRIDMARKETS_MT_help_menu.bl_idname)


classes = (
    GRIDMARKETS_MT_about_menu,
    GRIDMARKETS_MT_auth_menu,
    GRIDMARKETS_MT_gm_menu,
    GRIDMARKETS_MT_help_menu,
    GRIDMARKETS_MT_misc_options,
    GRIDMARKETS_MT_project_packing_options,
    GRIDMARKETS_MT_switch_user_menu,
    GRIDMARKETS_MT_project_upload_options,
    GRIDMARKETS_MT_submit_options,
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

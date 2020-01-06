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
           'GRIDMARKETS_MT_submit_options']

from .about_menu import GRIDMARKETS_MT_about_menu
from .auth_menu import GRIDMARKETS_MT_auth_menu
from .gm_menu import GRIDMARKETS_MT_gm_menu
from .help_menu import GRIDMARKETS_MT_help_menu
from .misc_options import GRIDMARKETS_MT_misc_options
from .packing_options import GRIDMARKETS_MT_project_packing_options
from .switch_user_menu import GRIDMARKETS_MT_switch_user_menu
from .upload_options import GRIDMARKETS_MT_project_upload_options
from .submission_options import GRIDMARKETS_MT_submit_options


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

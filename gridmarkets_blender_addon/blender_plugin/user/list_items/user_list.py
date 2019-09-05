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
from gridmarkets_blender_addon.blender_plugin.user.property_groups.user_props import UserProps


class GRIDMARKETS_UL_user(bpy.types.UIList):
    bl_idname = "GRIDMARKETS_UL_user"

    def draw_item(self, context, layout, data, item: UserProps, icon, active_data, active_property, index=0, flt_flag=0):
        saved_profiles = bpy.context.user_preferences.addons[constants.ADDON_PACKAGE_NAME].preferences.saved_profiles
        is_default_user = saved_profiles.default_user == index

        row = layout.row()
        row.alignment="LEFT"
        row.label(icon=constants.ICON_DEFAULT_USER if is_default_user else constants.ICON_NON_DEFAULT_USER)
        row.label(text=item.auth_email)


classes = (
    GRIDMARKETS_UL_user,
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

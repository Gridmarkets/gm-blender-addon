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
from gridmarkets_blender_addon.blender_plugin.user_container.property_groups.user_container_props import UserContainerProps


class AddonPreferences(bpy.types.AddonPreferences):
    """ 
    This class holds the user's preferences for the add-on. They are set in the
    user preferences window in the Add-ons tab.
    """

    # the bl_idname must match the add-on's package name
    bl_idname = constants.ADDON_PACKAGE_NAME

    saved_profiles = bpy.props.PointerProperty(
        type=UserContainerProps
    )

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.user_container.layouts import draw_user_container
        draw_user_container(self, context)


classes = (
    UserProps,
    UserContainerProps,
    AddonPreferences,
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

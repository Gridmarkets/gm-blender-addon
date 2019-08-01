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


class AddonPreferences(bpy.types.AddonPreferences):
    """ 
    This class holds the user's preferences for the addon. They are set in the 
    user preferences window in the Add-ons tab.
    """

    # the bl_idname must match the addon's package name
    bl_idname = constants.ADDON_PACKAGE_NAME

    # user's email
    auth_email = bpy.props.StringProperty(
        name="Email",
        description="Your Gridmarkets account email",
        default="",
        maxlen=1024,
        )
    
    # user's gridmarkets access key
    auth_accessKey = bpy.props.StringProperty(
        name="Access Key",
        description="Your Gridmarkets access key. This is different from your "
            "password and can be found by opening the Gridmarkets mangager "
            "portal and viewing your profile details",
        default="",
        maxlen=1024,
        subtype='PASSWORD'
        )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "auth_email")
        layout.prop(self, "auth_accessKey")


def register():
    # register add-on preferences
    bpy.utils.register_class(AddonPreferences)

def unregister():
    # unregister add-on preferences
    bpy.utils.unregister_class(AddonPreferences)
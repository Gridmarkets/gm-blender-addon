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

from gridmarkets_blender_addon.blender_plugin.user.property_groups.user_props import UserProps
from gridmarkets_blender_addon.meta_plugin.utils import get_deep_attribute
from .sign_in import GRIDMARKETS_OT_sign_in_new_user


class GRIDMARKETS_OT_switch_user(bpy.types.Operator):
    bl_idname = "gridmarkets.switch_user"
    bl_label = "Switch User"
    bl_description = "Switch to a different account"
    bl_options = {"REGISTER"}

    auth_email: bpy.props.StringProperty(
        name="Email",
        description=UserProps.AUTH_EMAIL_DESCRIPTION,
        default="",
        maxlen=1024,
    )

    # user's access key
    auth_accessKey: bpy.props.StringProperty(
        name="Access Key",
        description=UserProps.AUTH_KEY_DESCRIPTION,
        default="",
        maxlen=1024,
        subtype='PASSWORD'
    )

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        user_interface = plugin.get_user_interface()
        user_interface.set_auth_email(self.auth_email)
        user_interface.set_auth_access_key(self.auth_accessKey)

        get_deep_attribute(bpy.ops, GRIDMARKETS_OT_sign_in_new_user.bl_idname)()
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_switch_user,
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

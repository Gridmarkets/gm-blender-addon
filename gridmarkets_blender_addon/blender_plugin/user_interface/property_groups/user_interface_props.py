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


class UserInterfaceProps(bpy.types.PropertyGroup):

    # email
    def _update_auth_email_input(self, context):
        self["is_auth_email_valid"] = True
        self["is_user_valid"] = True

    def _get_auth_email_input(self):
        try:
            value = self["auth_email_input"]
        except KeyError:
            value = ""
        return value

    def _set_auth_email_input(self, value):
        self["auth_email_input"] = value

    auth_email_input: bpy.props.StringProperty(
        name="Email",
        description=UserProps.AUTH_EMAIL_DESCRIPTION,
        default="",
        maxlen=1024,
        update=_update_auth_email_input,
        get=_get_auth_email_input,
        set=_set_auth_email_input,
        options={'SKIP_SAVE'}
    )

    is_auth_email_valid: bpy.props.BoolProperty(
        default=True,
        options={'SKIP_SAVE', 'HIDDEN'},
    )

    auth_email_validity_message: bpy.props.StringProperty(
        default="",
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    # access key
    def _update_auth_access_key_input(self, context):
        self["is_auth_access_key_valid"] = True
        self["is_user_valid"] = True

    def _get_auth_access_key_input(self):
        try:
            value = self["auth_access_key_input"]
        except KeyError:
            value = ""
        return value

    def _set_auth_access_key_input(self, value):
        self["auth_access_key_input"] = value

    auth_access_key_input: bpy.props.StringProperty(
        name="Access Key",
        description=UserProps.AUTH_KEY_DESCRIPTION,
        default="",
        maxlen=1024,
        subtype='PASSWORD',
        update=_update_auth_access_key_input,
        get=_get_auth_access_key_input,
        set=_set_auth_access_key_input,
        options={'SKIP_SAVE'}
    )

    is_auth_access_key_valid: bpy.props.BoolProperty(
        default=True,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    auth_access_key_validity_message: bpy.props.StringProperty(
        default="",
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    #user
    is_user_valid: bpy.props.BoolProperty(
        default=True,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    user_validity_message: bpy.props.StringProperty(
        default="",
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    # spinner
    running_operation_spinner: bpy.props.IntProperty(
        default=1,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    # logger
    show_log_dates: bpy.props.BoolProperty(
        name="Show Logged Dates",
        description="Toggles the displaying of dates for log items",
        default=False
    )

    show_log_times: bpy.props.BoolProperty(
        name="Show Logged Times",
        description="Toggles the displaying of times for log items",
        default=True
    )

    show_logger_names: bpy.props.BoolProperty(
        name="Show Logger Names",
        description="Toggles the displaying of logger names for log items",
        default=False
    )

    is_running_operation: bpy.props.BoolProperty(
        default=False,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    running_operation_message: bpy.props.StringProperty(
        default="",
        options={'SKIP_SAVE', 'HIDDEN'}
    )

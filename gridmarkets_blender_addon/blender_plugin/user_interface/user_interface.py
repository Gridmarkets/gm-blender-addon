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

from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.user_interface import UserInterface as MetaUserInterface
import bpy


class UserInterface(MetaUserInterface):

    # email
    def get_auth_email(self) -> str:
        return bpy.context.scene.props.user_interface.auth_email_input

    def get_auth_email_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_auth_email_valid

    def set_auth_email_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_auth_email_valid = is_valid

    def get_auth_email_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.auth_email_validity_message

    def set_auth_email_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.auth_email_validity_message = message

    # access key
    def get_auth_access_key(self) -> str:
        return bpy.context.scene.props.user_interface.auth_access_key_input

    def get_auth_access_key_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_auth_access_key_valid

    def set_auth_access_key_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_auth_access_key_valid = is_valid

    def get_auth_access_key_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.auth_access_key_validity_message

    def set_auth_access_key_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.auth_access_key_validity_message = message

    # user
    def get_user_validity_flag(self) -> bool:
        return bpy.context.scene.props.user_interface.is_user_valid

    def set_user_validity_flag(self, is_valid: bool) -> None:
        bpy.context.scene.props.user_interface.is_user_valid = is_valid

    def get_user_validity_message(self) -> str:
        return bpy.context.scene.props.user_interface.user_validity_message

    def set_user_validity_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.user_validity_message = message

    # operation
    def is_running_operation(self) -> bool:
        return bpy.context.scene.props.user_interface.is_running_operation

    def set_is_running_operation_flag(self, value: bool) -> None:
        bpy.context.scene.props.user_interface.is_running_operation = value

    def get_running_operation_message(self) -> str:
        return bpy.context.scene.props.user_interface.running_operation_message

    def set_running_operation_message(self, message: str) -> None:
        bpy.context.scene.props.user_interface.running_operation_message = message

    # load profile
    def load_profile(self, user_profile: User):
        bpy.context.scene.props.user_interface.auth_email_input = user_profile.get_auth_email()
        bpy.context.scene.props.user_interface.auth_access_key_input = user_profile.get_auth_key()

    # spinner
    def get_running_operation_spinner(self) -> int:
        return bpy.context.scene.props.user_interface.running_operation_spinner

    def increment_running_operation_spinner(self) -> None:
        bpy.context.scene.props.user_interface.running_operation_spinner += 1

        if bpy.context.scene.props.user_interface.running_operation_spinner > 7:
            bpy.context.scene.props.user_interface.running_operation_spinner = 0

    # logger
    def show_log_dates(self) -> bool:
        return bpy.context.scene.props.user_interface.show_log_dates

    def set_show_log_dates(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_log_dates = enabled

    def show_log_times(self) -> bool:
        return bpy.context.scene.props.user_interface.show_log_times

    def set_show_log_times(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_log_times = enabled

    def show_logger_names(self) -> bool:
        return bpy.context.scene.props.user_interface.show_logger_names

    def set_show_logger_names(self, enabled: bool) -> None:
        bpy.context.scene.props.user_interface.show_logger_names = enabled

    # console
    def is_logging_console_open(self) -> bool:
        return bpy.context.scene.props.is_logging_console_open

    def toggle_logging_console(self) -> None:
        bpy.context.scene.props.is_logging_console_open = not bpy.context.scene.props.is_logging_console_open

    # job preset
    def get_show_hidden_job_preset_attributes(self) -> bool:
        return bpy.context.scene.props.user_interface.show_hidden_job_preset_attributes

    def set_show_hidden_job_preset_attributes(self, value: bool) -> None:
        bpy.context.scene.props.user_interface.show_hidden_job_preset_attributes = value

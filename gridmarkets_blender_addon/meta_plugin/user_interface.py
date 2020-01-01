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

from abc import ABC, abstractmethod

from gridmarkets_blender_addon.meta_plugin.plugin_accessor import PluginAccessor
from gridmarkets_blender_addon.meta_plugin.user import User


class UserInterface(ABC, PluginAccessor):

    # email
    def get_auth_email(self) -> str:
        raise NotImplementedError

    def set_auth_email(self, email: str) -> None:
        raise NotImplementedError

    def get_auth_email_validity_flag(self) -> bool:
        raise NotImplementedError

    def set_auth_email_validity_flag(self, is_valid: bool) -> None:
        raise NotImplementedError

    def get_auth_email_validity_message(self) -> str:
        raise NotImplementedError

    def set_auth_email_validity_message(self, message: str) -> None:
        raise NotImplementedError

    # access key
    def get_auth_access_key(self) -> str:
        raise NotImplementedError

    def set_auth_access_key(self, auth_access_key) -> None:
        raise NotImplementedError

    def get_auth_access_key_validity_flag(self) -> bool:
        raise NotImplementedError

    def set_auth_access_key_validity_flag(self, is_valid: bool) -> None:
        raise NotImplementedError

    def get_auth_access_key_validity_message(self) -> str:
        raise NotImplementedError

    def set_auth_access_key_validity_message(self, message: str) -> None:
        raise NotImplementedError

    # user
    def get_user_validity_flag(self) -> bool:
        raise NotImplementedError

    def set_user_validity_flag(self, is_valid: bool) -> None:
        raise NotImplementedError

    def get_user_validity_message(self) -> str:
        raise NotImplementedError

    def set_user_validity_message(self, message: str) -> None:
        raise NotImplementedError

    # operation
    def is_running_operation(self) -> bool:
        raise NotImplementedError

    def set_is_running_operation_flag(self, value: bool) -> None:
        raise NotImplementedError

    def get_running_operation_message(self) -> str:
        raise NotImplementedError

    def set_running_operation_message(self, message: str) -> None:
        raise NotImplementedError

    # load profile
    def load_profile(self, user_profile: User):
        raise NotImplementedError

    # logging
    def show_log_dates(self) -> bool:
        raise NotImplementedError

    def set_show_log_dates(self, enabled: bool) -> None:
        raise NotImplementedError

    def show_log_times(self) -> bool:
        raise NotImplementedError

    def set_show_log_times(self, enabled: bool) -> None:
        raise NotImplementedError

    def show_logger_names(self) -> bool:
        raise NotImplementedError

    def set_show_logger_names(self, enabled: bool) -> None:
        raise NotImplementedError

    # job preset
    def get_show_hidden_job_preset_attributes(self) -> bool:
        raise NotImplementedError

    def set_show_hidden_job_preset_attributes(self, value: bool) -> None:
        raise NotImplementedError

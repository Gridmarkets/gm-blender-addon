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

    # signing in
    def get_signing_in_flag(self) -> bool:
        raise NotImplementedError

    def set_signing_in_flag(self, signing_in: bool) -> None:
        raise NotImplementedError

    # load profile
    def load_profile(self, user_profile: User):
        raise NotImplementedError
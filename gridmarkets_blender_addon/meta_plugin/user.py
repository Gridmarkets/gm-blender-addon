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

__all__ = 'User'


class User:

    def __init__(self, auth_email: str, auth_access_key: str):
        self._auth_email = auth_email
        self._auth_access_key = auth_access_key

    def get_auth_email(self) -> str:
        return self._auth_email

    def set_auth_email(self, email: str) -> None:
        self._auth_email = email

    def get_auth_key(self) -> str:
        return self._auth_access_key

    def set_auth_key(self, key: str) -> None:
        self._auth_access_key = key

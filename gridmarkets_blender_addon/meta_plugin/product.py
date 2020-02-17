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

__all__ = 'Product'


class Product:

    def __init__(self, unique_id: int, display_name: str, app_type: str, version: str):
        """
        :param unique_id: A unique integer that specifies this product
        :type unique_id: int
        :param display_name: The name of the product to use when displaying to the user
        :type display_name: str
        :param app_type: The application this product represents
        :type app_type: str
        :param version: The version of the application
        :type version: str
        """

        self._unique_id = unique_id
        self._display_name = display_name
        self._app_type = app_type
        self._version = version

    def get_unique_id(self) -> int:
        return self._unique_id

    def get_app_type(self) -> str:
        return self._app_type

    def get_display_name(self) -> str:
        return self._display_name

    def get_version(self) -> str:
        return self._version

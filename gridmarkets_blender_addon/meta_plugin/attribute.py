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

import enum


class AttributeType(enum.Enum):
    STRING = "STRING"
    ENUM = "ENUM"
    NULL = "NULL"


class Attribute:

    def __init__(self, key:str, display_name: str, description: str, attribute_type: AttributeType):
        self._key = key
        self._display_name = display_name
        self._description = description
        self._attribute_type = attribute_type

    def get_key(self) -> str:
        return self._key

    def get_display_name(self) -> str:
        return self._display_name

    def get_description(self) -> str:
        return self._description

    def get_type(self) -> AttributeType:
        return self._attribute_type

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
import typing
from abc import ABC, abstractmethod


class AttributeType(enum.Enum):
    STRING = "STRING"
    ENUM = "ENUM"
    NULL = "NULL"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"


class Attribute(ABC):

    def __init__(self,
                 key:str,
                 display_name: str,
                 description: str,
                 attribute_type: AttributeType,
                 subtype_kwargs: typing.Dict):

        self._key = key
        self._display_name = display_name
        self._description = description
        self._attribute_type = attribute_type
        self._subtype_kwargs = subtype_kwargs

    def get_key(self) -> str:
        return self._key

    def get_display_name(self) -> str:
        return self._display_name

    def get_description(self) -> str:
        return self._description

    def get_type(self) -> AttributeType:
        return self._attribute_type

    def get_subtype_kwargs(self) -> typing.Dict:
        return self._subtype_kwargs

    @abstractmethod
    def get_default_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def validate_value(self, value: any) -> None:
        raise NotImplementedError

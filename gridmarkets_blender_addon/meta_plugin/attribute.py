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
from gridmarkets_blender_addon.meta_plugin.attribute_type import AttributeType

import typing


class Attribute(ABC):

    def __init__(self, key:str, display_name: str, description: str):
        self._key = key
        self._display_name = display_name
        self._description = description

    def get_key(self) -> str:
        return self._key

    def get_display_name(self) -> str:
        return self._display_name

    def get_description(self) -> str:
        return self._description

    def get_type(self) -> AttributeType:
        raise NotImplementedError


class StringAttribute:
    def get_type(self) -> AttributeType:
        return AttributeType.STRING


class EnumItem:

    def __init__(self, key: str, display_name: str, description: str):
        self._key = key
        self._display_name = display_name
        self._description = description

    def get_key(self) -> str:
        return self._key

    def get_display_name(self) -> str:
        return self._display_name

    def get_description(self) -> str:
        return self._description


class EnumAttribute:

    def __init__(self, items: typing.List[EnumItem]):
        self._items = items

    def get_type(self) -> AttributeType:
        return AttributeType.ENUM.value

    def get_items(self) -> typing.List[EnumItem]:
        return self._items

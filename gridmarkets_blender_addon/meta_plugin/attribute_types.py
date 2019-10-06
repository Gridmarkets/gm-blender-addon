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

__all__ = ['StringAttributeType', 'EnumAttributeType', 'EnumItem', 'NullAttributeType', 'BooleanAttributeType',
           'IntegerAttributeType']

import typing
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute, AttributeType


class StringAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str, default_value: typing.Optional[str] = ""):
        Attribute.__init__(self, key, display_name, description, AttributeType.STRING)

        if default_value is None:
            default_value = ""

        self._default_value = default_value

    def get_default_value(self) -> str:
        return self._default_value


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


class EnumAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str, items: typing.List[EnumItem],
                 default_value: typing.Optional[str] = None):
        Attribute.__init__(self, key, display_name, description, AttributeType.ENUM)

        if len(items) <= 0:
            raise ValueError("Enum must have at least one possible value")

        self._items = items

        if default_value is None:
            # by default use the first enum item as a default value if no default value was provided
            self._default_value = items[0]
        else:
            # check the default enum value is a valid enum item
            for item in self._items:
                if item.get_key() == default_value:
                    self._default_value = item
                    break
            else:
                raise ValueError("Default enum value must be a valid enum option, not '" + str(default_value) + "'")

    def get_default_value(self) -> EnumItem:
        return self._default_value

    def get_items(self) -> typing.List[EnumItem]:
        return self._items


class NullAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str):
        Attribute.__init__(self, key, display_name, description, AttributeType.NULL)
        self._default_value = None

    def get_default_value(self) -> None:
        return self._default_value


class BooleanAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str, default_value: typing.Optional[bool] = ""):
        Attribute.__init__(self, key, display_name, description, AttributeType.BOOLEAN)

        if default_value is None:
            default_value = False

        self._default_value = default_value

    def get_default_value(self) -> bool:
        return self._default_value


class IntegerAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str, default_value: typing.Optional[int] = 0):
        Attribute.__init__(self, key, display_name, description, AttributeType.INTEGER)

        if default_value is None:
            default_value = 0

        self._default_value = default_value

    def get_default_value(self) -> int:
        return self._default_value

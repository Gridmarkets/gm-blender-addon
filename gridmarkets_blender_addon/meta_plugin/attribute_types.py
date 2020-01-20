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

__all__ = ['StringAttributeType', 'StringSubtype',
           'EnumAttributeType', 'EnumItem', 'EnumSubtype',
           'NullAttributeType',
           'BooleanAttributeType',
           'IntegerAttributeType', 'IntegerSubtype']

import typing
import enum
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute, AttributeType
from gridmarkets_blender_addon.meta_plugin.errors.invalid_attribute_error import InvalidAttributeError


class StringSubtype(enum.Enum):
    NONE = "NONE"
    FRAME_RANGES = "FRAME_RANGES"
    FILE_PATH = "FILE_PATH"


class StringAttributeType(Attribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 subtype_kwargs: typing.Dict,
                 default_value: typing.Optional[str] = "",
                 subtype: typing.Optional[StringSubtype] = StringSubtype.NONE.value,
                 max_length: typing.Optional[int] = None,
                 min_length: typing.Optional[int] = None):

        Attribute.__init__(self, key, display_name, description, AttributeType.STRING, subtype_kwargs)

        if default_value is None:
            default_value = ""

        if subtype is None:
            subtype = StringSubtype.NONE.value

        self._default_value = default_value
        self._subtype = subtype
        self._max_length = max_length
        self._min_length = min_length

    def get_default_value(self) -> typing.Optional[str]:
        return self._default_value

    def get_subtype(self) -> StringSubtype:
        return self._subtype

    def get_max_length(self) -> typing.Optional[int]:
        return self._max_length

    def get_min_length(self) -> typing.Optional[int]:
        return self._min_length

    def validate_value(self, value: any) -> None:
        if value is None:
            raise InvalidAttributeError("value must not be None")

        if type(value) != str:
            raise InvalidAttributeError("value must be string type")

        if self._max_length is not None and len(value) > self._max_length:
            raise InvalidAttributeError("value be be a maximum of " + str(self._max_length) + " characters long")

        if self._min_length is not None and len(value) < self._min_length:
            raise InvalidAttributeError("value be be a minimum of " + str(self._min_length) + " characters long")


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


class EnumSubtype(enum.Enum):
    NONE = "NONE"
    PRODUCT_VERSIONS = "PRODUCT_VERSIONS"


class EnumAttributeType(Attribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 subtype_kwargs: typing.Dict,
                 items: typing.List[EnumItem],
                 default_value: typing.Optional[str] = None,
                 subtype: typing.Optional[EnumSubtype] = EnumSubtype.NONE.value):

        Attribute.__init__(self, key, display_name, description, AttributeType.ENUM, subtype_kwargs)

        if len(items) <= 0 and subtype != EnumSubtype.PRODUCT_VERSIONS.value:
            raise ValueError("Enum '" + key + "' must have at least one possible value")

        self._items = items
        self._subtype = subtype

        if subtype == EnumSubtype.PRODUCT_VERSIONS.value:
            # items and default value do not matter for PRODUCT_VERSIONS subtype
            self._default_value = None
        elif default_value is None:
            # by default use the first enum item as a default value if no default value was provided
            self._default_value = items[0].get_key()
        else:
            self._default_value = default_value

    def get_default_value(self) -> typing.Optional[str]:
        return self._default_value

    def get_default_enum_item(self) -> typing.Optional[EnumItem]:
        for item in self._items:
            if item.get_key() == self.get_default_value():
                return item
        return None

    def get_subtype(self) -> EnumSubtype:
        return self._subtype

    def get_items(self) -> typing.List[EnumItem]:
        return self._items

    def validate_value(self, value: any) -> None:
        if value is None:
            raise InvalidAttributeError("value must not be None")

        if type(value) != str:
            raise InvalidAttributeError("value must be string type")

        # don't compare items for product version enums because they are dynamic
        if self.get_subtype() == EnumSubtype.PRODUCT_VERSIONS.value:
            return

        for item in self.get_items():
            if item.get_key() == value:
                return
        else:
            raise InvalidAttributeError("value must be one of the possible enum values")


class NullAttributeType(Attribute):

    def __init__(self, key: str, display_name: str, description: str, subtype_kwargs: typing.Dict):
        Attribute.__init__(self, key, display_name, description, AttributeType.NULL, subtype_kwargs)
        self._default_value = None

    def get_default_value(self) -> None:
        return self._default_value

    def validate_value(self, value: any) -> None:
        if value is not None:
            raise InvalidAttributeError("value must be None")


class BooleanAttributeType(Attribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 subtype_kwargs: typing.Dict,
                 default_value: typing.Optional[bool] = True):

        Attribute.__init__(self, key, display_name, description, AttributeType.BOOLEAN, subtype_kwargs)

        if default_value is None:
            default_value = False

        self._default_value = default_value

    def get_default_value(self) -> typing.Optional[bool]:
        return self._default_value

    def validate_value(self, value: any) -> None:
        if value is None:
            raise InvalidAttributeError("value must not be None")

        if type(value) != bool:
            raise InvalidAttributeError("value must be bool type")


class IntegerSubtype(enum.Enum):
    NONE = "NONE"
    INSTANCES = "INSTANCES"


class IntegerAttributeType(Attribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 subtype_kwargs: typing.Dict,
                 default_value: typing.Optional[int] = 0,
                 subtype: typing.Optional[IntegerSubtype] = IntegerSubtype.NONE.value):

        Attribute.__init__(self, key, display_name, description, AttributeType.INTEGER, subtype_kwargs)

        if default_value is None:
            default_value = 0

        self._default_value = default_value
        self._subtype = subtype

    def get_default_value(self) -> typing.Optional[int]:
        return self._default_value

    def get_subtype(self) -> IntegerSubtype:
        return self._subtype

    def validate_value(self, value: any) -> None:
        if value is None:
            raise InvalidAttributeError("value must not be None")

        if type(value) != int:
            raise InvalidAttributeError("value must be int type")

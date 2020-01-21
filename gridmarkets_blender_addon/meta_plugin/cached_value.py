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

__all__ = 'CachedValue'

import copy
import typing

T = typing.TypeVar('T')


class CachedValue(typing.Generic[T]):
    def __init__(self, value: T, is_cached: bool = False):
        self._initial_value = copy.copy(value)
        self._value = value
        self._is_cached = is_cached

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T):
        self._value = value
        self._is_cached = True

    def is_cached(self) -> bool:
        return self._is_cached

    def reset_and_clear_cache(self):
        self._value = copy.copy(self._initial_value)
        self._is_cached = False
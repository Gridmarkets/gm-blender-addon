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

from abc import ABC
from typing import Generic, Optional, TypeVar, List
from gridmarkets_blender_addon.meta_plugin.plugin_accessor import PluginAccessor


T = TypeVar('T')


class ListContainer(ABC, Generic[T], PluginAccessor):

    def __init__(self, items: List[T]):
        self._items = items
        self._selected = []

    def get_focused_item(self) -> Optional[T]:
        if len(self._selected) == 0:
            return None

        return self._selected[-1]

    def focus_item(self, item: T, clear_selection=True) -> None:
        if not self.contains(item):
            raise ValueError("Can not focus an item not in the list")

        if clear_selection:
            self._selected = []

        self._selected.append(item)

    def get_selected(self) -> List[T]:
        return self._selected

    def deselect(self, item) -> None:
        if not self.is_selected(item):
            raise ValueError("Can not deselect an item that is not already selected")

        self._selected.remove(item)

    def select_all(self):
        self._selected = []
        for item in self._items:
            self._selected.append(item)

    def deselect_all(self):
        self._selected = []

    def get_all(self) -> List[T]:
        return self._items

    def get_at(self, index: int) -> T:

        if index < 0 or index >= len(self._items):
            return None

        return self._items[index]

    def append(self, item: T, focus_new_item: bool = True) -> None:
        self._items.append(item)

        if focus_new_item:
            self.focus_item(item)

    def remove(self, item: T) -> None:
        self._selected.remove(item)
        self._items.remove(item)

    def remove_focused(self) -> None:
        if self._selected:
            focused_item = self._selected[-1]
            self.remove(focused_item)

    def remove_selected(self) -> None:
        while len(self._selected) > 0:
            item = self._selected[-1]
            self.remove(item)

    def contains(self, item: T) -> bool:
        return item in self._items

    def get_index(self, item: T) -> int:
        return self._items.index(item)

    def is_selected(self, item: T):
        return item in self._selected

    def size(self):
        return len(self._items)
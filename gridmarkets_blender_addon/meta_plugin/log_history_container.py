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

import typing

from gridmarkets_blender_addon.meta_plugin.log_item import LogItem
from gridmarkets_blender_addon.meta_plugin.list_container import ListContainer


class LogHistoryContainer(ListContainer, LogItem):

    def __init__(self, log_item: typing.List[LogItem]):
        ListContainer.__init__(self, log_item)

    def get_focused_item(self) -> typing.Optional[LogItem]:
        return ListContainer.get_focused_item(self)

    def focus_item(self, log_item: LogItem, clear_selection=True) -> None:
        ListContainer.focus_item(self, log_item, clear_selection=clear_selection)

    def get_selected(self) -> typing.List[LogItem]:
        return ListContainer.get_selected(self)

    def get_all(self) -> typing.List[LogItem]:
        return ListContainer.get_all(self)

    def get_at(self, index: int) -> LogItem:
        return ListContainer.get_at(self, index)

    def append(self, log_item: LogItem, focus_new_item: bool = True) -> None:
        ListContainer.append(self, log_item, focus_new_item=focus_new_item)

    def remove(self, log_item: LogItem) -> None:
        ListContainer.remove(self, log_item)

    def contains(self, log_item: LogItem) -> bool:
        return ListContainer.contains(self, log_item)

    def get_index(self, log_item: LogItem) -> int:
        return ListContainer.get_index(self, log_item)

    def is_selected(self, log_item: LogItem) -> bool:
        return ListContainer.is_selected(self, log_item)

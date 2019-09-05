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

from typing import List, Optional

from gridmarkets_blender_addon.meta_plugin.list_container import ListContainer
from gridmarkets_blender_addon.meta_plugin.user import User


class UserContainer(ListContainer[User]):

    def __init__(self, users: List[User], default_user: Optional[User] = None):
        ListContainer.__init__(self, users)

        self._default_user = None
        self.set_default_user(default_user)

    def append(self, item: User, focus_new_item: bool = True) -> None:
        ListContainer.append(self, item, focus_new_item = focus_new_item)

        if self.get_default_user() is None:
            self.set_default_user(self._items[-1])

    def remove(self, item: User) -> None:

        if item == self._default_user:
            self.set_default_user(None)

        ListContainer.remove(self, item)

    def get_default_user(self) -> Optional[User]:
        return self._default_user

    def set_default_user(self, user: Optional[User]) -> None:

        if user is None:
            self._default_user = None
        else:
            if not self.contains(user):
                raise ValueError("Can not set an item as default that is not already in the list")

            self._default_user = user

    def set_focused_as_default_user(self) -> None:
        self.set_default_user(self.get_focused_item())

    def load_focused_profile(self) -> None:
        plugin = self.get_plugin()

        focused_item = self.get_focused_item()

        if focused_item is not None:
            plugin.get_user_interface().load_profile(focused_item)

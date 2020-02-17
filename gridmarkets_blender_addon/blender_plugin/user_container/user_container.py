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

import bpy

import typing

from gridmarkets_blender_addon.meta_plugin.user_container import UserContainer as MetaUserContainer
from gridmarkets_blender_addon.blender_plugin.user.user import User

from gridmarkets_blender_addon import constants

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.blender_plugin.plugin.plugin import Plugin


class UserContainer(MetaUserContainer):

    def __init__(self, plugin: 'Plugin'):
        preferences = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        # get users
        users_props = preferences.saved_profiles.user_profiles
        users: typing.List[User] = []

        for user_props in users_props:
            user = User(user_props.auth_email, user_props.auth_accessKey)
            users.append(user)

        # get default user
        default_user_index = preferences.saved_profiles.default_user

        if default_user_index < 0 or default_user_index >= len(users):
            default_user = None
        else:
            try:
                default_user = users[default_user_index]
            except IndexError:
                default_user = None

        MetaUserContainer.__init__(self, plugin, users, default_user)

        # get focused user
        focused_user_index =  preferences.saved_profiles.focused_user
        try:
            focused_user = users[focused_user_index]
            self.focus_item(focused_user)
        except IndexError:
            focused_user = None

    def focus_item(self, item: User, clear_selection=True, update_props=True) -> None:
        if update_props:
            saved_profiles = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences.saved_profiles

            index = self.get_index(item)

            if index:
                saved_profiles.focused_user = index

        MetaUserContainer.focus_item(self, item, clear_selection)

    def append(self, item: User, focus_new_item: bool = True) -> None:
        MetaUserContainer.append(self, item, focus_new_item = focus_new_item)

        preferences = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences
        user_props = preferences.saved_profiles.user_profiles.add()
        user_props.auth_email = item.get_auth_email()
        user_props.auth_accessKey = item.get_auth_key()

        if self.get_default_user() is None:
            self.set_default_user(self._item[-1])

    def remove(self, item: User) -> None:
        index = self._items.index(item)

        if item == self._default_user:
            self.set_default_user(None)

        saved_profiles = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences.saved_profiles
        saved_profiles.user_profiles.remove(index)

        MetaUserContainer.remove(self, item)

    def get_default_user(self) -> typing.Optional[User]:
        saved_profiles = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences.saved_profiles
        default_user_index = saved_profiles.default_user
        return self.get_at(default_user_index)

    def set_default_user(self, user: typing.Optional[User]) -> None:
        saved_profiles = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences.saved_profiles

        if user is None:
            saved_profiles.default_user = -1
        else:
            if not self.contains(user):
                raise ValueError("Can not set an item as default that is not already in the list")

            saved_profiles.default_user = self.get_index(user)

    def set_focused_as_default_user(self) -> None:
        self.set_default_user(self.get_focused_item())

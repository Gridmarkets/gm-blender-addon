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
import typing


class PluginFetcher(ABC):

    _plugin = None

    @staticmethod
    @abstractmethod
    def get_plugin() -> 'Plugin':
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_plugin_if_initialised() -> typing.Optional['Plugin']:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete_cached_plugin() -> None:
        raise NotImplementedError

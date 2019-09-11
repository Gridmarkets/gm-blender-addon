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
from gridmarkets_blender_addon.meta_plugin.plugin_version import PluginVersion
from gridmarkets_blender_addon.meta_plugin.logging_coordinator import LoggingCoordinator
from gridmarkets_blender_addon.meta_plugin.preferences_container import PreferencesContainer
from gridmarkets_blender_addon.meta_plugin.api_client import APIClient
from gridmarkets_blender_addon.meta_plugin.user_interface import UserInterface
from gridmarkets_blender_addon.meta_plugin.remote_project_container import RemoteProjectContainer
from gridmarkets_blender_addon.meta_plugin.plugin_utils import PluginUtils


class Plugin(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_version(self) -> PluginVersion:
        raise NotImplementedError

    @abstractmethod
    def get_logging_coordinator(self) -> LoggingCoordinator:
        raise NotImplementedError

    @abstractmethod
    def get_preferences_container(self) -> PreferencesContainer:
        raise NotImplementedError

    @abstractmethod
    def get_api_client(self) -> APIClient:
        raise NotImplementedError

    @abstractmethod
    def get_user_interface(self) -> UserInterface:
        raise NotImplementedError

    @abstractmethod
    def get_remote_project_container(self) -> RemoteProjectContainer:
        raise NotImplementedError

    def get_plugin_utils(self) -> PluginUtils:
        raise NotImplementedError

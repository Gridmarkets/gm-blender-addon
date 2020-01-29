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

__all__ = 'Plugin'

import typing
from abc import ABC, abstractmethod

if typing.TYPE_CHECKING:
    from . import PluginVersion, LoggingCoordinator, PreferencesContainer, APIClient, UserInterface, \
        RemoteProjectContainer, ApplicationPoolAttributeSource, FactoryCollection, PluginUtils


class Plugin(ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_version(self) -> 'PluginVersion':
        raise NotImplementedError

    @abstractmethod
    def get_logging_coordinator(self) -> 'LoggingCoordinator':
        raise NotImplementedError

    @abstractmethod
    def get_preferences_container(self) -> 'PreferencesContainer':
        raise NotImplementedError

    @abstractmethod
    def get_api_client(self) -> 'APIClient':
        raise NotImplementedError

    @abstractmethod
    def get_user_interface(self) -> 'UserInterface':
        raise NotImplementedError

    @abstractmethod
    def get_remote_project_container(self) -> 'RemoteProjectContainer':
        raise NotImplementedError

    @abstractmethod
    def get_application_pool_attribute_source(self) -> 'ApplicationPoolAttributeSource':
        raise NotImplementedError

    @abstractmethod
    def get_factory_collection(self) -> 'FactoryCollection':
        raise NotImplementedError

    def get_plugin_utils(self) -> 'PluginUtils':
        raise NotImplementedError

    @abstractmethod
    def get_supported_applications(self) -> typing.List[str]:
        raise NotImplementedError

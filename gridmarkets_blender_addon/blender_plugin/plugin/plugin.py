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

from gridmarkets_blender_addon import bl_info

from gridmarkets_blender_addon.meta_plugin.plugin import Plugin as MetaPlugin
from gridmarkets_blender_addon.meta_plugin.plugin_version import PluginVersion
from gridmarkets_blender_addon.meta_plugin.logging_coordinator import LoggingCoordinator

from gridmarkets_blender_addon.blender_plugin.log_history_container.log_history_container import LogHistoryContainer
from gridmarkets_blender_addon.blender_plugin.preferences_container.preferences_container import PreferencesContainer
from gridmarkets_blender_addon.blender_plugin.user_container.user_container import UserContainer
from gridmarkets_blender_addon.blender_plugin.job_preset_container.job_preset_container import JobPresetContainer
from gridmarkets_blender_addon.blender_plugin.api_client.api_client import APIClient
from gridmarkets_blender_addon.blender_plugin.user_interface.user_interface import UserInterface
from gridmarkets_blender_addon.blender_plugin.remote_project_container.remote_project_container import \
    RemoteProjectContainer
from gridmarkets_blender_addon.blender_plugin.application_pool_attribute_source.application_pool_attribute_source import \
    ApplicationPoolAttributeSource
from gridmarkets_blender_addon.blender_plugin.plugin_utils.plugin_utils import PluginUtils


class Plugin(MetaPlugin):

    def __init__(self):
        version = bl_info['version']
        self._version = PluginVersion(version[0], version[1], version[2])
        self._logging_coordinator = LoggingCoordinator(LogHistoryContainer())
        self._preferences_container = PreferencesContainer(UserContainer(), JobPresetContainer())
        self._api_client = APIClient(self._logging_coordinator)
        self._user_interface = UserInterface()
        self._remote_project_container = RemoteProjectContainer()
        self._plugin_utils = PluginUtils()
        self._application_pool_attribute_source = ApplicationPoolAttributeSource()

    def get_name(self) -> str:
        return bl_info['name']

    def get_version(self) -> PluginVersion:
        return self._version

    def get_logging_coordinator(self) -> LoggingCoordinator:
        return self._logging_coordinator

    def get_preferences_container(self) -> PreferencesContainer:
        return self._preferences_container

    def get_api_client(self) -> APIClient:
        return self._api_client

    def get_user_interface(self) -> UserInterface:
        return self._user_interface

    def get_remote_project_container(self) -> RemoteProjectContainer:
        return self._remote_project_container

    def get_application_pool_attribute_source(self) -> ApplicationPoolAttributeSource:
        return self._application_pool_attribute_source

    def get_plugin_utils(self) -> PluginUtils:
        return self._plugin_utils

    def register_dynamic_props(self) -> None:
        job_presets = self._preferences_container.get_job_preset_container().get_all()
        for job_preset in job_presets:
            job_preset.register_props()

    def unregister_dynamic_props(self) -> None:
        job_presets = self._preferences_container.get_job_preset_container().get_all()
        for job_preset in job_presets:
            job_preset.unregister_props()

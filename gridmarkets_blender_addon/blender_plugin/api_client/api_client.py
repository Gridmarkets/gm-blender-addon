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

from gridmarkets_blender_addon.meta_plugin import User
from gridmarkets_blender_addon.meta_plugin.gridmarkets.api_client import GridMarketsAPIClient
from gridmarkets_blender_addon.meta_plugin.logging_coordinator import LoggingCoordinator
from gridmarkets_blender_addon import utils_blender
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.gridmarkets.remote_project import RemoteProject, convert_packed_project
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
import pathlib

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.meta_plugin.factory_collection import FactoryCollection
    from gridmarkets_blender_addon.meta_plugin.gridmarkets.api_schema import APISchema
    from gridmarkets_blender_addon.blender_plugin.plugin.plugin import Plugin


class APIClient(GridMarketsAPIClient):

    def __init__(self, plugin: 'Plugin', logging_coordinator: 'LoggingCoordinator', factory_collection: 'FactoryCollection'):
        GridMarketsAPIClient.__init__(self, plugin, logging_coordinator, factory_collection)
        self._signed_in_lock_extra = False

    def sign_in(self, user: User, skip_validation: bool = False) -> None:
        GridMarketsAPIClient.sign_in(self, user, skip_validation=skip_validation)

        from gridmarkets_blender_addon.operators.open_addon import register_schema
        register_schema(self)

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        plugin.get_user_interface().reset_project_attribute_props()

        # cache the machine options for blender
        self.get_machines(api_constants.PRODUCTS.BLENDER, 'render')

        self._signed_in_lock_extra = True
        utils_blender.force_redraw_addon()

    def sign_out(self) -> None:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        self._signed_in_lock_extra = False
        GridMarketsAPIClient.sign_out(self)
        plugin.get_remote_project_container().reset()
        utils_blender.force_redraw_addon()

    def is_user_signed_in(self) -> bool:
        return GridMarketsAPIClient.is_user_signed_in(self) and self._signed_in_lock_extra

    def connected(self) -> bool:
        raise NotImplementedError

    def upload_project(self,
                       packed_project: PackedProject,
                       upload_root_dir: bool,
                       delete_local_files_after_upload: bool = False) -> RemoteProject:

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        remote_project = GridMarketsAPIClient.upload_project(self, packed_project, upload_root_dir, delete_local_files_after_upload)
        plugin.get_remote_project_container().append(remote_project)
        plugin.get_user_interface().set_layout(constants.REMOTE_PROJECTS_LAYOUT_VALUE)
        return remote_project

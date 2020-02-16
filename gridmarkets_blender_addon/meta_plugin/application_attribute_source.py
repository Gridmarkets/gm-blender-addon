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

__all__ = 'ApplicationAttributeSource'

from abc import ABC, abstractmethod
import typing

from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
from gridmarkets_blender_addon.meta_plugin.errors import ApplicationAttributeNotFound
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.meta_plugin import Plugin


class ApplicationAttributeSource(ABC):

    def __init__(self, plugin: 'Plugin'):
        self._plugin = plugin

    def get_plugin(self) -> 'Plugin':
        return self._plugin

    @abstractmethod
    def get_attribute_value(self, app: str, version: str, key: str):
        raise NotImplementedError

    def get_project_attribute_values(self, project_name: str, app: str, version: str) -> typing.Dict:
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_schema = plugin.get_api_client().get_cached_api_schema()

        attributes = {}

        # project name
        root = api_schema.get_root_project_attribute()
        attributes[api_constants.API_KEYS.PROJECT_NAME] = project_name

        # product
        product_attribute = root.transition(project_name, force_transition=True)
        attributes[api_constants.API_KEYS.APP] = app

        # product version
        product_version_attribute = product_attribute.transition(app)
        attributes[api_constants.API_KEYS.APP_VERSION] = version

        # other attributes
        project_attribute = product_version_attribute.transition(app, force_transition=True)
        while True:
            attribute = project_attribute.get_attribute()

            if attribute.get_type() == AttributeType.NULL:
                attributes[api_constants.API_KEYS.PROJECT_TYPE_ID] = project_attribute.get_id()
                break

            # attempt to get the application inferred value for the project attributes
            try:
                app_inferred_value = self.get_attribute_value(app, version, project_attribute.get_attribute().get_key())
            except ApplicationAttributeNotFound as e:
                # if the application source does not recognise this attribute key then use the default value
                app_inferred_value = project_attribute.get_attribute().get_default_value()

            project_attribute = project_attribute.transition(app_inferred_value, force_transition=True)

        return attributes

    def set_project_attribute_values(self, project_name: str, app: str, version: str) -> None:
        plugin = self.get_plugin()

        # todo don't use "get_cached_api_schema"
        project_attribute = plugin.get_api_client().get_cached_api_schema().get_root_project_attribute()

        # set project name
        project_attribute.set_value(project_name)
        project_attribute = project_attribute.transition(project_attribute.get_value())

        # set product
        project_attribute.set_value(app)
        project_attribute = project_attribute.transition(project_attribute.get_value())

        # set product version
        project_attribute.set_value(version)
        project_attribute = project_attribute.transition(project_attribute.get_value())

        while True:
            attribute = project_attribute.get_attribute()

            if attribute.get_type() == AttributeType.NULL:
                break

            # attempt to set the project attributes value to the application inferred value
            try:
                app_inferred_value = self.get_attribute_value(app, version, project_attribute.get_attribute().get_key())
            except ApplicationAttributeNotFound as e:
                # if the application source does not recognise this attribute key then use the default value
                app_inferred_value = project_attribute.get_attribute().get_default_value()

            project_attribute.set_value(app_inferred_value)

            project_attribute = project_attribute.transition(project_attribute.get_value(),
                                                             force_transition=True)

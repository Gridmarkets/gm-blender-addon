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

from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType
from gridmarkets_blender_addon.meta_plugin.errors.application_attribute_not_found import ApplicationAttributeNotFound
from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import RejectedTransitionInputError
from gridmarkets_blender_addon.blender_plugin.project_attribute.project_attribute import get_project_attribute_value, \
    set_project_attribute_value
from gridmarkets_blender_addon.meta_plugin.application_attribute_sources.application_attribute_source import \
    ApplicationAttributeSource


class ApplicationPoolAttributeSource(ABC):

    def get_attribute_value(self, app: str, version: str, key: str):
        if app == 'blender':
            return self.get_blender_attribute_source().get_attribute_value(app, version, key)
        else:
            raise ValueError("Unrecognised application: " + str(app))

    def set_project_attribute_values(self, project_name: str, app: str, version: str) -> None:

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        project_attribute = plugin.get_api_client().get_api_schema().get_root_project_attribute()

        # set project name
        set_project_attribute_value(project_attribute, project_name)
        project_attribute = project_attribute.transition(get_project_attribute_value(project_attribute))

        # set product
        set_project_attribute_value(project_attribute, app)
        project_attribute = project_attribute.transition(get_project_attribute_value(project_attribute))

        # set product version
        set_project_attribute_value(project_attribute, version)
        project_attribute = project_attribute.transition(get_project_attribute_value(project_attribute))

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

            set_project_attribute_value(project_attribute, app_inferred_value)

            try:
                project_attribute = project_attribute.transition(get_project_attribute_value(project_attribute))
            except RejectedTransitionInputError as e:
                # if the transition is rejected because the current input is not valid attempt to manually transition
                # if there is only one transition path
                transitions = project_attribute.get_transitions()
                if len(transitions) == 1:
                    project_attribute = transitions[0].get_project_attribute()
                else:
                    raise e

    @abstractmethod
    def get_blender_attribute_source(self) -> ApplicationAttributeSource:
        raise NotImplementedError

    @abstractmethod
    def get_vray_attribute_source(self) -> ApplicationAttributeSource:
        raise NotImplementedError

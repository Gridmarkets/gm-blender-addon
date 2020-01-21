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

__all__ = ['JobPresetAttribute']

import typing

from .inference_source import InferenceSource

if typing.TYPE_CHECKING:
    from . import Plugin, JobPreset, RemoteProject, JobAttribute


class JobPresetAttribute:

    def __init__(self, parent_preset: 'JobPreset', job_attribute: 'JobAttribute',
                 inference_source: 'InferenceSource' = None,
                 value: any = None):

        self._parent_preset = parent_preset
        self._job_attribute = job_attribute
        self._id = parent_preset.get_id() + '_' + job_attribute.get_attribute().get_key()

        if inference_source is not None:
            if inference_source not in job_attribute.get_inference_sources():
                raise ValueError("Inference source must be set to a valid inference source.")
        else:
            inference_source = job_attribute.get_default_inference_source()
        self._inference_source = inference_source

        if value is None:
            value = job_attribute.get_attribute().get_default_value()
        self._value = value

    def get_parent_preset(self) -> 'JobPreset':
        return self._parent_preset

    def get_job_attribute(self) -> 'JobAttribute':
        return self._job_attribute

    def get_id(self) -> str:
        return self._id

    def get_key(self) -> str:
        return self.get_job_attribute().get_attribute().get_key()

    def get_inference_source(self) -> 'InferenceSource':
        return self._inference_source

    def set_inference_source(self, inference_source) -> None:

        if inference_source not in self.get_job_attribute().get_inference_sources():
            raise ValueError("Inference source must be set to a valid inference source.")

        self._inference_source = inference_source

    def get_value(self) -> any:
        return self._value

    def set_value(self, value: any) -> None:
        self._value = value

    def eval(self, plugin: 'Plugin', source_project: 'RemoteProject' = None):

        inference_source = self.get_inference_source()
        attribute = self._job_attribute.get_attribute()

        # application source
        if inference_source == InferenceSource.get_application_inference_source():
            # app and app version attributes must be either user defined or constants if also application defined
            app = self._parent_preset.get_job_preset_attribute_by_key('app').get_value()
            version = self._parent_preset.get_job_preset_attribute_by_key('app_version').get_value()

            if self.get_key() == 'app':
                return app

            if self.get_key() == 'app_version':
                return version

            application_pool_attribute_source = plugin.get_application_pool_attribute_source()
            return application_pool_attribute_source.get_attribute_value(app, version, self.get_key())

        # project source
        elif inference_source == InferenceSource.get_project_inference_source():
            if source_project is None:
                raise ValueError("Must provide source project for attribute '" + attribute.get_display_name() + "'")

            return source_project.get_attribute(attribute.get_key())

        # constant source
        elif inference_source == InferenceSource.get_constant_inference_source():
            return attribute.get_default_value()

        # user defined source
        elif inference_source == InferenceSource.get_user_defined_inference_source():
            return self.get_value()

        else:
            raise ValueError("Unknown inference source: " + str(inference_source))

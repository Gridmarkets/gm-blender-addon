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

__all__ = 'APISchema'

import typing
from . import constants as api_constants
from ..api_schema import APISchema as MetaAPISchema
from ..inference_source import InferenceSource

if typing.TYPE_CHECKING:
    from .. import JobDefinition, ProjectAttribute, Plugin


class APISchema(MetaAPISchema):

    def __init__(self,
                 plugin: 'Plugin',
                 job_definitions: typing.List['JobDefinition'],
                 project_attributes: typing.List['ProjectAttribute']):

        MetaAPISchema.__init__(self, plugin, job_definitions, project_attributes)

    def get_root_project_attribute(self) -> 'ProjectAttribute':
        return self.get_project_attribute_with_id(api_constants.ROOT_ATTRIBUTE_ID)

    def trim_unsupported_applications(self, plugin: 'Plugin'):

        for job_definition in self.get_job_definitions():
            app_attribute = job_definition.get_attribute_with_key(api_constants.API_KEYS.APP)

            if app_attribute:
                default_value = app_attribute.get_attribute().get_default_value()

                if default_value not in plugin.get_supported_applications():
                    # remove application inference sources from all job attributes
                    for job_attribute in job_definition.get_attributes():
                        inference_sources = job_attribute.get_inference_sources()

                        if InferenceSource.get_application_inference_source() in inference_sources:
                            inference_sources.remove(InferenceSource.get_application_inference_source())

                        job_attribute.set_inference_sources(inference_sources)

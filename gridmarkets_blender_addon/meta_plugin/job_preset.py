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
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.attribute_inference_source import AttributeInferenceSource
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute


class JobPreset(ABC):

    def __init__(self, name: str, id: str, job_definition: JobDefinition):
        self._name = name
        self._id = id
        self._job_definition = job_definition

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_id(self) -> str:
        return self._id

    def get_job_definition(self) -> JobDefinition:
        return self._job_definition

    @abstractmethod
    def get_attribute_value(self, job_attribute: JobAttribute, project_source: RemoteProject = None) -> any:
        raise NotImplementedError

    @abstractmethod
    def get_attribute_active_inference_source(self, job_attribute: JobAttribute) -> AttributeInferenceSource:
        raise NotImplementedError

    @abstractmethod
    def set_attribute_active_inference_source(self, job_attribute: JobAttribute,
                                              inference_source: AttributeInferenceSource) -> None:
        raise NotImplementedError

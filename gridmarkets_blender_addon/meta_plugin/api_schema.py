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
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute


class APISchema:

    def __init__(self, job_definitions: typing.List[JobDefinition], project_attributes: typing.List[ProjectAttribute]):
        self._job_definitions = job_definitions
        self._project_attributes = project_attributes

    def get_root_project_attribute(self) -> ProjectAttribute:
        return self.get_project_attribute_with_id("GM_PROJECT_NAME")

    def get_job_definitions(self) -> typing.List[JobDefinition]:
        return self._job_definitions

    def get_job_definition_with_id(self, id: str) -> JobDefinition:

        for job_definition in self.get_job_definitions():
            if job_definition.get_definition_id() == id:
                return job_definition

        raise ValueError("No job definition with id '" + id + "'")

    def get_project_attributes(self) -> typing.List[ProjectAttribute]:
        return self._project_attributes

    def get_project_attribute_with_id(self, id:str) -> ProjectAttribute:
        for project_attribute in self.get_project_attributes():
            if project_attribute.get_id() == id:
                return project_attribute

        raise ValueError("No project attribute with id '" + id + "'")

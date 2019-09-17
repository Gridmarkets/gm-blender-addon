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

from gridmarkets_blender_addon.meta_plugin.attribute import Attribute
from gridmarkets_blender_addon.meta_plugin.attribute_type import AttributeType
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.transition import Transition


class ProjectAttribute(Attribute):

    def __init__(self, id:str, key:str, display_name: str, description: str,
                 transitions: typing.List[Transition], compatible_job_definitions: typing.List[JobDefinition]):
        Attribute.__init__(self, key, display_name, description)

        self._id = id
        self._transitions = transitions
        self._compatible_job_definitions = compatible_job_definitions

    def get_id(self) -> str:
        return self._id

    def get_type(self) -> AttributeType:
        raise NotImplementedError

    def has_transitions(self) -> bool:
        return len(self._transitions) > 0

    def get_transitions(self) -> typing.List[Transition]:
        return self._transitions

    def has_compatible_job_definitions(self) -> bool:
        return len(self._compatible_job_definitions) > 0

    def get_compatible_job_definitions(self) -> typing.List[JobDefinition]:
        return self._compatible_job_definitions

    def get_children(self) -> typing.List['ProjectAttribute']:
        return list(map(lambda x: x.get_project_attribute(), self.get_transitions()))

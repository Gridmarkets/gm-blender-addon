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

__all__ = 'APISchemaFactory'

from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from . import APISchema, ProjectAttribute, Plugin, JobDefinition


class APISchemaFactory(ABC):

    @abstractmethod
    def get_api_schema(self,
                       plugin: 'Plugin',
                       job_definitions: typing.List['JobDefinition'],
                       project_attributes: typing.List['ProjectAttribute']) -> 'APISchema':
        raise NotImplementedError

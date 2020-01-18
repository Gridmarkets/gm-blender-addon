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

__all__ = 'ProjectAttributeFactory'

from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from .attribute import Attribute
    from .project_attribute import ProjectAttribute
    from .transition import Transition
    from .job_definition import JobDefinition


class ProjectAttributeFactory(ABC):

    @abstractmethod
    def get_project_attribute(self,
                              id: str,
                              attribute: 'Attribute',
                              transitions: typing.List['Transition'],
                              compatible_job_definitions: typing.List['JobDefinition']) -> 'ProjectAttribute':
        raise NotImplementedError

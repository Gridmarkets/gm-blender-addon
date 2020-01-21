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
from . import constants
from ..api_schema import APISchema as MetaAPISchema

if typing.TYPE_CHECKING:
    from .. import JobDefinition, ProjectAttribute


class APISchema(MetaAPISchema):

    def __init__(self, job_definitions: typing.List['JobDefinition'],
                 project_attributes: typing.List['ProjectAttribute']):
        MetaAPISchema.__init__(self, job_definitions, project_attributes)

    def get_root_project_attribute(self) -> 'ProjectAttribute':
        return self.get_project_attribute_with_id(constants.ROOT_ATTRIBUTE_ID)

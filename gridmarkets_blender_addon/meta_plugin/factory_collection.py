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

__all__ = 'FactoryCollection'

import typing

if typing.TYPE_CHECKING:
    from . import ProjectAttributeFactory


class FactoryCollection:
    def __init__(self, project_attribute_factory: 'ProjectAttributeFactory'):
        self._project_attribute_factory = project_attribute_factory

    def get_project_attribute_factory(self) -> 'ProjectAttributeFactory':
        return self._project_attribute_factory

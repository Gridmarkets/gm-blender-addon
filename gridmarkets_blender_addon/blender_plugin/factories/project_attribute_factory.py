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

from gridmarkets_blender_addon.meta_plugin.project_attribute_factory import \
    ProjectAttributeFactory as MetaProjectAttributeFactory

from ..project_attribute.project_attribute import ProjectAttribute

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.meta_plugin.attribute import Attribute
    from gridmarkets_blender_addon.meta_plugin.transition import Transition
    from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition


class ProjectAttributeFactory(MetaProjectAttributeFactory):

    def get_project_attribute(self,
                              id: str,
                              attribute: 'Attribute',
                              transitions: typing.List['Transition'],
                              compatible_job_definitions: typing.List['JobDefinition']) -> 'ProjectAttribute':

        return ProjectAttribute(id, attribute, transitions, compatible_job_definitions)

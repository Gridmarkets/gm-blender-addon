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

__all__ = 'PackedSceneBuilder'

from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from . import Plugin, PackedProject


class PackedSceneBuilder(ABC):

    def __init__(self, plugin: 'Plugin'):
        self._plugin = plugin

    def get_plugin(self):
        return self._plugin

    @abstractmethod
    def _build_scene_internal(self,
                              project_name: str,
                              product: str,
                              product_version: str,
                              attributes: typing.Dict[str, any]) -> 'PackedProject':
        raise NotImplementedError

    def get_current_scene(self,
                          project_name: str,
                          product: str,
                          product_version: str,
                          attributes: typing.Dict[str, any] = None) -> 'PackedProject':
        """
        todo make it so you only pass the project attribute and all other values are pased from it. Requires project
          attribute instances
        """

        if attributes is None:
            attributes = {}

        packed_project = self._build_scene_internal(project_name, product, product_version, attributes)

        packed_project.set_name(project_name)

        if attributes:
            for key, value in attributes.items():

                # If the key is not already in the packed project's attribute list
                if key not in packed_project.get_attributes():
                    # Then set the attribute
                    packed_project.set_attribute(key, value)

        return packed_project

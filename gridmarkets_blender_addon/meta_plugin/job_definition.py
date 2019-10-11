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
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute


class JobDefinition:

    def __init__(self, id: str, display_name: str, attributes: typing.List[JobAttribute]):
        self._id = id
        self._display_name = display_name
        self._attributes = attributes

    def get_definition_id(self) -> str:
        return self._id

    def get_display_name(self) -> str:
        return self._display_name

    def get_attributes(self) -> typing.List[JobAttribute]:
        return self._attributes

    def get_attribute_with_key(self, key: str) -> JobAttribute:
        for job_attribute in self.get_attributes():
            if job_attribute.get_attribute().get_key() == key:
                return job_attribute
        else:
            raise ValueError("Could not find attribute with key '" + key + "'")

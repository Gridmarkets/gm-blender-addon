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

from typing import List

from gridmarkets_blender_addon.meta_plugin.attribute import Attribute
from gridmarkets_blender_addon.meta_plugin.attribute_type import AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute_inference_source import AttributeInferenceSource


class JobAttribute(Attribute):

    def __init__(self,
                 key:str,
                 display_name: str,
                 description: str,
                 inference_sources: List[AttributeInferenceSource],
                 is_optional: bool):

        Attribute.__init__(self, key, display_name, description)
        self._inference_sources = inference_sources
        self._is_optional = is_optional

    def is_optional(self) -> bool:
        return self._is_optional

    def get_inference_sources(self) -> List[AttributeInferenceSource]:
        return self._inference_sources

    def get_type(self) -> AttributeType:
        raise NotImplementedError

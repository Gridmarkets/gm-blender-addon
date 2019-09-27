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

__all__ = ['JobAttribute', 'StringJobAttribute', 'EnumJobAttribute', 'NullJobAttribute']

from abc import ABC
import typing

from gridmarkets_blender_addon.meta_plugin.attribute import Attribute
from gridmarkets_blender_addon.meta_plugin.attribute_types import *
from gridmarkets_blender_addon.meta_plugin.attribute_inference_source import AttributeInferenceSource


class JobAttribute(ABC):

    def __init__(self,
                 inference_sources: typing.List[AttributeInferenceSource],
                 is_optional: bool):

        self._inference_sources = inference_sources
        self._is_optional = is_optional

    def is_optional(self) -> bool:
        return self._is_optional

    def get_inference_sources(self) -> typing.List[AttributeInferenceSource]:
        return self._inference_sources


class StringJobAttribute(StringAttributeType, JobAttribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 inference_sources: typing.List[AttributeInferenceSource],
                 is_optional: bool,
                 default_value: typing.Optional[str] = ""):
        StringAttributeType.__init__(self, key, display_name, description, default_value=default_value)
        JobAttribute.__init__(self, inference_sources, is_optional)


class EnumJobAttribute(EnumAttributeType, JobAttribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 inference_sources: typing.List[AttributeInferenceSource],
                 is_optional: bool,
                 items: typing.List[EnumItem],
                 default_value: typing.Optional[str] = None):
        EnumAttributeType.__init__(self, key, display_name, description, items, default_value=default_value)
        JobAttribute.__init__(self, inference_sources, is_optional)


class NullJobAttribute(NullAttributeType, JobAttribute):

    def __init__(self,
                 key: str,
                 display_name: str,
                 description: str,
                 inference_sources: typing.List[AttributeInferenceSource],
                 is_optional: bool):
        NullAttributeType.__init__(self, key, display_name, description)
        JobAttribute.__init__(self, inference_sources, is_optional)

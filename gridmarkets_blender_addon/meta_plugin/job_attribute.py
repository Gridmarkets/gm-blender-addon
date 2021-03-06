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

__all__ = ['JobAttribute']

import typing

if typing.TYPE_CHECKING:
    from . import Attribute, InferenceSource


class JobAttribute:

    def __init__(self,
                 attribute: 'Attribute',
                 inference_sources: typing.List['InferenceSource'],
                 is_optional: bool):

        if inference_sources is None or len(inference_sources) < 1:
            raise ValueError("JobAttribute has no inference sources")

        self._attribute = attribute
        self._inference_sources = inference_sources
        self._is_optional = is_optional

    def get_attribute(self) -> 'Attribute':
        return self._attribute

    def is_optional(self) -> bool:
        return self._is_optional

    def get_inference_sources(self) -> typing.List['InferenceSource']:
        return self._inference_sources

    def set_inference_sources(self, inference_sources):
        self._inference_sources = inference_sources

    def get_default_inference_source(self) -> 'InferenceSource':
        return self.get_inference_sources()[0]

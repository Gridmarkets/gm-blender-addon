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

__all__ = 'BlenderAttributeSource'

from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.application_attribute_source import ApplicationAttributeSource
from gridmarkets_blender_addon.meta_plugin.errors import ApplicationAttributeNotFound

import re


class BlenderAttributeSource(ApplicationAttributeSource):

    def get_attribute_value(self, app: str, app_version: str, key: str):
        import bpy

        if app != api_constants.PRODUCTS.BLENDER:
            raise ValueError

        if key == api_constants.API_KEYS.APP_VERSION:
            return app_version

        if re.match(api_constants.BLENDER_VERSIONS.SERIES_2_8X, app_version):
            if key == api_constants.API_KEYS.OUTPUT_FORMAT:
                return bpy.context.scene.render.image_settings.file_format
            elif key == api_constants.API_KEYS.FRAMES:
                from gridmarkets_blender_addon.utils_blender import get_blender_frame_range
                return get_blender_frame_range(bpy.context)
            elif key == api_constants.API_KEYS.GPU:
                return bpy.context.scene.cycles.device == 'GPU'

        if re.match(api_constants.BLENDER_VERSIONS.SERIES_2_7X, app_version):
            if key == api_constants.API_KEYS.OUTPUT_FORMAT:
                return bpy.context.scene.render.image_settings.file_format
            elif key == api_constants.API_KEYS.FRAMES:
                from gridmarkets_blender_addon.utils_blender import get_blender_frame_range
                return get_blender_frame_range(bpy.context)
            elif key == api_constants.API_KEYS.GPU:
                return bpy.context.scene.cycles.device == 'GPU'

        raise ApplicationAttributeNotFound(app, app_version, key)

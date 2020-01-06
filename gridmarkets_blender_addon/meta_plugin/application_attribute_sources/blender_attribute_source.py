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

from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as meta_constants
from gridmarkets_blender_addon.meta_plugin.application_attribute_sources.application_attribute_source import \
    ApplicationAttributeSource
from gridmarkets_blender_addon.meta_plugin.errors.application_attribute_not_found import ApplicationAttributeNotFound


class BlenderAttributeSource(ApplicationAttributeSource):
    APP = 'blender'

    def get_attribute_value(self, app: str, app_version: str, key: str):
        import bpy

        if app != self.APP:
            raise ValueError

        if app_version == meta_constants.BLENDER_VERSIONS.V_2_80 or app_version == meta_constants.BLENDER_VERSIONS.V_2_81A:
            if key == 'output_format':
                return bpy.context.scene.render.image_settings.file_format
            elif key == 'frames':
                from gridmarkets_blender_addon.utils_blender import get_blender_frame_range
                return get_blender_frame_range(bpy.context)

        raise ApplicationAttributeNotFound(app, app_version, key)

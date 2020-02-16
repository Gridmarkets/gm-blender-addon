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

from gridmarkets_blender_addon.meta_plugin import PackedSceneBuilder as MetaPackedSceneBuilder
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter

import typing

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.meta_plugin import PackedProject


class PackedSceneBuilder(MetaPackedSceneBuilder):

    def _build_scene_internal(self,
                              project_name: str,
                              product: str,
                              product_version: str,
                              attributes: typing.Dict[str, any]) -> 'PackedProject':

        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager
        temp_dir = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

        if product == api_constants.PRODUCTS.BLENDER:
            packed_project = BlenderSceneExporter().export(temp_dir)
        elif product == api_constants.PRODUCTS.VRAY:
            packed_project = VRaySceneExporter().export(temp_dir)
        else:
            raise RuntimeError("Unknown project type")

        return packed_project

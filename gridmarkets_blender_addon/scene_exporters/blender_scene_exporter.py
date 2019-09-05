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

from gridmarkets_blender_addon.meta_plugin.scene_exporter import SceneExporter
from gridmarkets_blender_addon import utils_blender

import bpy
import tempfile
import pathlib

from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.file_packers.blender_file_packer import BlenderFilePacker

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class BlenderSceneExporter(SceneExporter):

    @staticmethod
    def _save_scene_to_file(target: str):
        log.info("Saving scene to temporary file: " + target)
        bpy.ops.wm.save_as_mainfile(copy=True, filepath=target, relative_remap=True,
                                    compress=True)

    def export(self, output_dir: pathlib.Path) -> PackedProject:
        # save a copy of blender scene to a temporary .blend file
        tmp_dir = tempfile.TemporaryDirectory(prefix='gm-temp-dir-')
        blend_file_name = utils_blender.get_blend_file_name()
        blend_file_path = pathlib.Path(tmp_dir.name) / blend_file_name
        BlenderSceneExporter._save_scene_to_file(str(blend_file_path))

        packed_project = BlenderFilePacker().pack(blend_file_path, output_dir)

        # delete temporary pre-packed .blend file
        tmp_dir.cleanup()

        return packed_project

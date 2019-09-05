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

from gridmarkets_blender_addon.meta_plugin.file_packer import FilePacker
from gridmarkets_blender_addon import utils_blender

import pathlib

from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class BlenderFilePacker(FilePacker):
    def pack(self, target_file: pathlib.Path, output_dir: pathlib.Path) -> PackedProject:

        # pack the .blend file to the pack directory
        # _set_progress(progress=60, status="Packing scene data")
        utils_blender.pack_blend_file(str(target_file), str(output_dir))

        # delete pack-info.txt if it exists
        pack_info_file = output_dir / 'pack-info.txt'
        if pack_info_file.is_file():
            log.info("Removing '%s'..." % str(pack_info_file))
            pack_info_file.unlink()

        return PackedProject(output_dir.stem,
                                       output_dir,
                                       output_dir / target_file.name,
                                       set(),
                                       {"PRODUCT": "blender"})

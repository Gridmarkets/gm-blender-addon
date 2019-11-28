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

import pathlib

from gridmarkets_blender_addon.meta_plugin.file_packer import FilePacker
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject


class BlenderFilePacker(FilePacker):
    BAT_PACK_INFO_FILE_NAME = "pack-info.txt"

    def pack(self, target_file: pathlib.Path, output_dir: pathlib.Path) -> PackedProject:
        from gridmarkets_blender_addon.bat_progress_callback import BatProgressCallback
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon import constants

        plugin = PluginFetcher.get_plugin()
        logging_coordinator = plugin.get_logging_coordinator()
        log = logging_coordinator.get_logger(__name__)

        # pack the .blend file to the pack directory
        self.pack_blend_file(str(target_file), str(output_dir), BatProgressCallback(log))

        # delete pack-info.txt if it exists
        pack_info_file = output_dir / self.BAT_PACK_INFO_FILE_NAME
        if pack_info_file.is_file():
            log.info("Removing '%s'..." % str(pack_info_file))
            pack_info_file.unlink()

        return PackedProject(output_dir.stem,
                             output_dir,
                             {output_dir / target_file.name},
                             {"PRODUCT": "blender", constants.MAIN_PROJECT_FILE: output_dir / target_file.name})

    @staticmethod
    def pack_blend_file(blend_file_path, target_dir_path, progress_cb=None):
        """ Packs a Blender .blend file to a target folder using blender_asset_tracer

        :param blend_file_path: The .blend file to pack
        :type blend_file_path: str
        :param target_dir_path: The path to the directory which will contain the packed files
        :type target_dir_path: str
        :param progress_cb: The progress reporting callback instance
        :type progress_cb: blender_asset_tracer.pack.progress.Callback
        """
        from blender_asset_tracer import pack

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        log = PluginFetcher.get_plugin().get_logging_coordinator().get_logger(__name__)
        log.info("Starting pack operation....")

        blend_file_path = pathlib.Path(blend_file_path)
        project_root_path = blend_file_path.parent
        target_dir_path = pathlib.Path(target_dir_path)

        log.info("blend_file_path: %s" % str(blend_file_path))
        log.info("project_root_path: %s" % str(project_root_path))
        log.info("target_dir_path: %s" % str(target_dir_path))

        # create packer
        with pack.Packer(blend_file_path,
                         project_root_path,
                         target_dir_path,
                         noop=False,  # no-op mode, only shows what will be done
                         compress=False,
                         relative_only=False
                         ) as packer:

            log.info("Created packer")

            if progress_cb:
                log.info("Setting packer progress callback...")
                packer._progress_cb = progress_cb

            # plan the packing operation (must be called before execute)
            log.info("Plan packing operation...")
            packer.strategise()

            # attempt to pack the project
            try:
                log.info("Plan packing operation...")
                packer.execute()
            except pack.transfer.FileTransferError as ex:
                log.warning(str(len(ex.files_remaining)) + " files couldn't be copied, starting with " +
                            str(ex.files_remaining[0]))
                raise SystemExit(1)
            finally:
                log.info("Exiting packing operation...")

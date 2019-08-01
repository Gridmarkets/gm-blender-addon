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

from blender_asset_tracer.pack.progress import Callback
import pathlib
import typing


class BatProgressCallback(Callback):
    """ Represents a callback class which logs the progress made by BAT.pack and BAT.trace"""

    def __init__(self, logger):
        """ Constructor
        :param logger: The logger instance which should be used to log the progress
        :type logger: blender_logging_wrapper.BlenderLoggingWrapper
        """
        self.log = logger

    def pack_start(self) -> None:
        self.log.info('Starting BAT Pack operation')

    def pack_done(self,
                  output_blendfile: pathlib.Path,
                  missing_files: typing.Set[pathlib.Path]) -> None:
        if missing_files:
            self.log.info('There were %d missing files' % len(missing_files))
        else:
            self.log.info('Pack of %s done' % output_blendfile.name)

    def pack_aborted(self, reason: str):
        self.log.info('Aborted: %s' % reason)

    def trace_blendfile(self, filename: pathlib.Path) -> None:
        """Called for every .blend file opened when tracing dependencies."""
        self.log.info('Inspecting %s' % filename.name)

    def trace_asset(self, filename: pathlib.Path) -> None:
        if filename.stem == '.blend':
            return
        self.log.info('Found asset %s' % filename.name)

    def rewrite_blendfile(self, orig_filename: pathlib.Path) -> None:
        self.log.info('Rewriting cloned %s (This will not modify your original file / scene)' % orig_filename.name)

    def transfer_file(self, src: pathlib.Path, dst: pathlib.Path) -> None:
        self.log.info('Transferring %s' % src.name)

    def transfer_file_skipped(self, src: pathlib.Path, dst: pathlib.Path) -> None:
        self.log.info('Skipped %s' % src.name)

    def transfer_progress(self, total_bytes: int, transferred_bytes: int) -> None:
        self.log.info("Progress: %s" % str(round(100 * transferred_bytes / total_bytes)))

    def missing_file(self, filename: pathlib.Path) -> None:
        self.log.warning("Missing asset: %s" % filename.name)
        pass

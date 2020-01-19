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
from gridmarkets_blender_addon.meta_plugin.gridmarkets.remote_project import RemoteProject


class RemoteVRayProject(RemoteProject):

    ATTRIBUTE_REMAP_FILE_KEY = "REMAP_FILE"

    def __init__(self, root_dir: pathlib.Path, main_file: pathlib.Path, remap_file: pathlib.Path):
        from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

        attributes = {
            api_constants.API_KEYS.PATH: main_file,
            api_constants.API_KEYS.APP: api_constants.PRODUCTS.VRAY,
            self.ATTRIBUTE_REMAP_FILE_KEY: remap_file
        }

        RemoteProject.__init__(self,
                               root_dir.stem,
                               root_dir,
                               set(),  # empty set for now since they are not used
                               attributes)

    def get_remap_file(self) -> pathlib.Path:
        return self.get_attribute(self.ATTRIBUTE_REMAP_FILE_KEY)

    def set_name(self, name: str) -> None:
        pass

    def exists(self) -> bool:
        pass

    def delete(self) -> None:
        pass

    def get_size(self) -> int:
        pass

    def set_size(self, size: int) -> None:
        pass

    def get_total_bytes_done_uploading(self, force_update: bool = False) -> int:
        pass

    def set_total_bytes_done_uploading(self, bytes: int) -> None:
        pass

    def get_remaining_bytes_to_upload(self, force_update: bool = False) -> int:
        pass

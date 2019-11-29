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
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject


class RemoteVRayProject(RemoteProject):
    ATTRIBUTE_REMAP_FILE_KEY = "REMAP_FILE"

    def __init__(self, root_dir: pathlib.Path, main_file: pathlib.Path, remap_file: pathlib.Path):
        from gridmarkets_blender_addon import api_constants

        attributes = {
            "MAIN_PROJECT_FILE": main_file,
            "PRODUCT": api_constants.PRODUCTS.VRAY,
            self.ATTRIBUTE_REMAP_FILE_KEY: remap_file
        }

        RemoteProject.__init__(self,
                               root_dir.stem,
                               root_dir,
                               set(),  # empty set for now since they are not used
                               attributes)

    def get_remap_file(self) -> pathlib.Path:
        return self.get_attribute(self.ATTRIBUTE_REMAP_FILE_KEY)

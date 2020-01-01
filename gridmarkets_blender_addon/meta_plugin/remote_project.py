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

from gridmarkets_blender_addon.meta_plugin.project import Project
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
import pathlib
import typing


class RemoteProject(Project):

    def __init__(self,
                 name: str,
                 root_dir: pathlib.Path,
                 files: typing.Set[pathlib.Path],
                 attributes: typing.Dict[str, any]):
        Project.__init__(self,
                         name,
                         root_dir,
                         files,
                         attributes)

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def exists(self) -> bool:
        raise NotImplementedError

    def delete(self) -> None:
        raise NotImplementedError

    def get_size(self) -> int:
        raise NotImplementedError

    @staticmethod
    def convert_packed_project(packed_project: PackedProject) -> 'RemoteProject':

        root_dir = pathlib.Path(packed_project.get_name())

        # convert files from absolute local paths to absolute remote paths
        files = set(map(lambda file: pathlib.Path('/') / root_dir / file, packed_project.get_relative_files()))
        attributes = packed_project.get_attributes()

        # convert all pathlib.Path attributes into a relative path
        for key, attribute in attributes.items():
            if isinstance(attribute, pathlib.Path):
                attributes[key] = packed_project.get_relative_file_path(attribute)

        # TODO update files into relative files

        return RemoteProject(packed_project.get_name(),
                             root_dir,
                             files,
                             attributes)

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

__all__ = 'PackedProject'

import pathlib
import typing

from .local_project import LocalProject
from .utils import remove_directory


class PackedProject(LocalProject):

    def __init__(self,
                 name: str,
                 root_dir: pathlib.Path,
                 files: typing.Set[pathlib.Path],
                 attributes: typing.Dict[str, any]):

        LocalProject.__init__(self,
                              name,
                              root_dir,
                              files,
                              attributes)

    def get_relative_file_path(self, file: pathlib.Path) -> pathlib.Path:
        root_dir = self.get_root_dir()

        if not file.is_absolute():
            raise ValueError("file \"" + str(file) + "\" must be absolute")

        if file.anchor != root_dir.anchor:
            raise ValueError("file \"" + str(file) + "\" must be on same drive as project directory (\"" +
                             str(root_dir.anchor) + "\")")

        return file.relative_to(root_dir)

    def get_relative_files(self) -> typing.Set[pathlib.Path]:
        relative_files = map(self.get_relative_file_path, self.get_files())
        return set(relative_files)

    def exists(self) -> bool:
        if self.get_root_dir().is_dir():
            return True

    def delete(self) -> None:
        if self.exists():
            remove_directory(self.get_root_dir())

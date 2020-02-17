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

__all__ = 'LocalProject'

from abc import abstractmethod
import pathlib
import typing

from .project import Project


class LocalProject(Project):

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

    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    def get_size(self) -> int:
        project_size = 0
        for file in self.get_files():
            project_size += file.stat().st_size
        return project_size

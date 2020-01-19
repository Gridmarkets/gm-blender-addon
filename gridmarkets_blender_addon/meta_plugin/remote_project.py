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

__all__ = 'RemoteProject'

from abc import ABC, abstractmethod

from gridmarkets_blender_addon.meta_plugin.project import Project
import pathlib
import typing

if typing.TYPE_CHECKING:
    pass


class RemoteProject(Project, ABC):

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
    def get_files(self, force_update=False) -> typing.Set[pathlib.Path]:
        raise NotImplementedError

    @abstractmethod
    def set_file_list(self, files: typing.Set[pathlib.Path]) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_name(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_size(self, size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_total_bytes_done_uploading(self, force_update: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_total_bytes_done_uploading(self, bytes: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_remaining_bytes_to_upload(self, force_update: bool = False) -> int:
        raise NotImplementedError

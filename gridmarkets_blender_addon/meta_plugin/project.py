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

from abc import ABC, abstractmethod
import typing
import pathlib


class Project(ABC):

    def __init__(self,
                 name: str,
                 root_dir: pathlib.Path,
                 main_file: pathlib.Path,
                 files: typing.Set[pathlib.Path],
                 attributes: typing.Dict[str, any]):
        self._name = name
        self._root_dir = root_dir
        self._main_file = main_file
        self._files = files
        self._attributes = attributes

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_attributes(self) -> typing.Dict[str, any]:
        return self._attributes

    def get_attribute(self, key: str) -> any:
        return self._attributes[key]

    def set_attribute(self, key: str, value: any) -> None:
        self._attributes[key] = value

    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    def get_root_dir(self) -> pathlib.Path:
        return self._root_dir

    def get_main_file(self) -> typing.Optional[pathlib.Path]:
        return self._main_file

    def get_files(self) -> typing.Set[pathlib.Path]:
        return self._files

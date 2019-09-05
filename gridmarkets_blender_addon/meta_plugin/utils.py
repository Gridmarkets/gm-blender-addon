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

import typing
import pathlib


def remove_directory(directory: pathlib.Path) -> None:

    if not directory.is_dir():
        return

    for item in directory.iterdir():
        if item.is_dir():
            remove_directory(item)
        else:
            item.unlink()

    directory.rmdir()


def get_files_in_directory(directory:pathlib.Path) -> typing.Set[pathlib.Path]:

    files = set()

    if not directory.is_dir():
        return files

    for item in directory.iterdir():
        if item.is_dir():
            files.update(get_files_in_directory(item))
        else:
            files.add(item)

    return files
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

class PluginVersion:

    def __init__(self, major: int, minor: int, build: int):
        self._major = major
        self._minor = minor
        self._build = build

    def get_major_version(self) -> int:
        return self._major

    def get_minor_version(self) -> int:
        return self._minor

    def get_build_version(self) -> int:
        return self._build

    def to_string(self) -> str:
        return str(self._major) + '.' + str(self._minor) + '.' + str(self._build)

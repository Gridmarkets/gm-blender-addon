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

__all__ = 'MachineOption'


class MachineOption:

    def __init__(self, machine_id: str, name: str, is_default: bool, is_gpu: bool):
        self._machine_id = machine_id
        self._name = name
        self._is_default = is_default
        self._is_gpu = is_gpu

    def get_id(self) -> str:
        return self._machine_id

    def get_name(self) -> str:
        return self._name

    def is_default(self) -> bool:
        return self._is_default

    def is_gpu_machine(self) -> bool:
        return self._is_gpu

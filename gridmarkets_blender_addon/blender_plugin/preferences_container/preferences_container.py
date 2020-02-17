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

from gridmarkets_blender_addon.meta_plugin.preferences_container import PreferencesContainer as MetaPreferencesContainer
from gridmarkets_blender_addon.blender_plugin.user_container.user_container import UserContainer
from gridmarkets_blender_addon.blender_plugin.job_preset_container.job_preset_container import JobPresetContainer


class PreferencesContainer(MetaPreferencesContainer):

    def __init__(self, user_container: UserContainer, job_preset_container: JobPresetContainer):
        self._user_container = user_container
        self._job_preset_container = job_preset_container

    def get_user_container(self) -> UserContainer:
        return self._user_container

    def get_job_preset_container(self) -> JobPresetContainer:
        return self._job_preset_container

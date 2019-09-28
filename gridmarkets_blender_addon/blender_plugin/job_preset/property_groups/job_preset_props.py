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

import bpy


class JobPresetProps(bpy.types.PropertyGroup):

    def _get_name(self):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin is None:
            return ""

        job_preset_container = plugin.get_preferences_container().get_job_preset_container()

        for job_preset in job_preset_container.get_all():
            if job_preset.get_id() == self.id:
                return job_preset.get_name()

    def _set_name(self, value):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin:
            job_preset_container = plugin.get_preferences_container().get_job_preset_container()

            for job_preset in job_preset_container.get_all():
                if job_preset.get_id() == self.id:
                    job_preset.set_name(value)
                    break

    name: bpy.props.StringProperty(
        name="Name",
        get=_get_name,
        set=_set_name,
        options={'SKIP_SAVE', 'HIDDEN'}
    )

    id: bpy.props.IntProperty(
        name="id",
        description="A arbitrary unique identifier generated locally to differentiate between log items",
        options={'SKIP_SAVE', 'HIDDEN'}
    )

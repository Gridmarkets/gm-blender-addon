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
from gridmarkets_blender_addon.blender_plugin.job_preset.property_groups.job_preset_props import JobPresetProps
from gridmarkets_blender_addon import constants


class JobPresetContainerProps(bpy.types.PropertyGroup):

    def _get_focused_item(self):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        if plugin is None:
            return -1

        job_preset_container = plugin.get_preferences_container().get_job_preset_container()
        focused_item = job_preset_container.get_focused_item()

        if focused_item is None:
            return -1

        return job_preset_container.get_index(focused_item)

    def _set_focused_item(self, value):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin_if_initialised()

        if plugin:
            job_preset_container = plugin.get_preferences_container().get_job_preset_container()
            item = job_preset_container.get_at(value)
            job_preset_container.focus_item(item, update_props=False)

    show_presets_for_all_products: bpy.props.EnumProperty(
        name="Show Job Presets for All Products",
        description="Show all types of Job Presets, even ones for non-blender projects.",
        items=[
            ("0", "Show only Blender Job Types", ""),
            (constants.SHOW_ALL_JOB_DEFINITIONS, "Show All Job Types", "")
        ],
        options={'SKIP_SAVE'}
    )

    focused_item: bpy.props.IntProperty(
        options={'SKIP_SAVE', 'HIDDEN'},
        get=_get_focused_item,
        set=_set_focused_item
    )

    items: bpy.props.CollectionProperty(
        type=JobPresetProps
    )



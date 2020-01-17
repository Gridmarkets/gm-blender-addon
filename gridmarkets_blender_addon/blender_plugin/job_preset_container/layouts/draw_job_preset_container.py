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


def draw_job_preset_container(layout, context):
    from gridmarkets_blender_addon import constants

    from gridmarkets_blender_addon.blender_plugin.job_preset_container.menus.create_new_job_preset import \
        GRIDMARKETS_MT_new_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.remove_focused_job_preset import \
        GRIDMARKETS_OT_remove_focused_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.toggle_job_preset_locked_state import \
        GRIDMARKETS_OT_toggle_job_preset_locked_state

    from gridmarkets_blender_addon.blender_plugin.job_preset.list_items.job_preset_list import GRIDMARKETS_UL_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset.layouts.draw_job_preset import draw_job_preset
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    job_preset_container = plugin.get_preferences_container().get_job_preset_container()
    job_preset = job_preset_container.get_focused_item()
    focued = job_preset is not None

    props = context.scene.props
    job_preset_container_props = props.job_preset_container

    layout.label(text='Job Presets', icon=constants.ICON_JOB_PRESET)
    layout.menu(GRIDMARKETS_MT_new_job_preset.bl_idname, icon=constants.ICON_NEW_JOB_PRESET)

    layout.template_list(GRIDMARKETS_UL_job_preset.bl_idname, "",
                         job_preset_container_props, "items",
                         job_preset_container_props, "focused_item",
                         rows=3)

    if focued:
        locked_icon = constants.ICON_LOCKED if job_preset.is_locked() else constants.ICON_UNLOCKED
        locked_text = "Unlock" if job_preset.is_locked() else "Lock"
    else:
        locked_icon = constants.ICON_NONE
        locked_text = None

    row = layout.row()
    row.operator(GRIDMARKETS_OT_toggle_job_preset_locked_state.bl_idname, text=locked_text, icon=locked_icon)
    row.enabled = focued

    row = layout.row()
    row.operator(GRIDMARKETS_OT_remove_focused_job_preset.bl_idname)
    row.enabled = focued and not job_preset.is_locked()

    layout.separator()
    draw_job_preset(layout, context)

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

if typing.TYPE_CHECKING:
    import bpy


def draw_job_preset_container(layout: 'bpy.types.UILayout', context: 'bpy.types.Context'):
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
    user_interface = plugin.get_user_interface()

    props = context.scene.props
    job_preset_container_props = props.job_preset_container

    row = layout.box().row(align=True)
    row2 = row.row(align=True)
    row2.menu(GRIDMARKETS_MT_new_job_preset.bl_idname, icon=constants.ICON_NEW_JOB_PRESET)
    row2.enabled = not user_interface.is_running_operation()

    row2 = row.row(align=True)
    row2.prop_menu_enum(job_preset_container_props, "show_presets_for_all_products", text="", icon=constants.ICON_COLLAPSEMENU)
    row2.alignment = "RIGHT"

    row = layout.box().row()
    row.template_list(GRIDMARKETS_UL_job_preset.bl_idname, "",
                         job_preset_container_props, "items",
                         job_preset_container_props, "focused_item",
                         rows=3)

    col = row.column()
    col.alignment = "RIGHT"

    job_preset_container = plugin.get_preferences_container().get_job_preset_container()
    job_preset = job_preset_container.get_focused_item()
    focused = job_preset is not None

    if focused:
        locked_icon = constants.ICON_UNLOCKED if job_preset.is_locked() else constants.ICON_LOCKED
    else:
        locked_icon = constants.ICON_LOCKED

    row2 = col.row()
    row2.operator(GRIDMARKETS_OT_remove_focused_job_preset.bl_idname, text="", icon=constants.ICON_TRASH)
    row2.enabled = focused and not job_preset.is_locked()

    row2 = col.row()
    row2.operator(GRIDMARKETS_OT_toggle_job_preset_locked_state.bl_idname, text='', icon=locked_icon)
    row2.enabled = focused

    draw_job_preset(layout, context)

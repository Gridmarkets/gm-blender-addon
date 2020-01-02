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
    from gridmarkets_blender_addon.blender_plugin.job_preset_container.menus.create_new_job_preset import \
        GRIDMARKETS_MT_new_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset_container.operators.remove_focused_job_preset import \
        GRIDMARKETS_OT_remove_focused_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset.list_items.job_preset_list import GRIDMARKETS_UL_job_preset
    from gridmarkets_blender_addon.blender_plugin.job_preset.layouts.draw_job_preset import draw_job_preset

    props = context.scene.props
    job_preset_container_props = props.job_preset_container

    layout.label(text='Job Presets')
    layout.menu(GRIDMARKETS_MT_new_job_preset.bl_idname)

    layout.template_list(GRIDMARKETS_UL_job_preset.bl_idname, "",
                         job_preset_container_props, "items",
                         job_preset_container_props, "focused_item",
                         rows=3)

    layout.operator(GRIDMARKETS_OT_remove_focused_job_preset.bl_idname)
    layout.separator()
    draw_job_preset(layout, context)

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


def draw_logging_console(self, context):
    from gridmarkets_blender_addon import constants
    from gridmarkets_blender_addon.blender_plugin.log_item.list_items.log_item_list import GRIDMARKETS_UL_log_item
    from gridmarkets_blender_addon.blender_plugin.log_history_container.menus.display_options import \
        GRIDMARKETS_MT_logging_display_options
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.clear_logs import \
        GRIDMARKETS_OT_clear_logs
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.copy_logs_to_clipboard import \
        GRIDMARKETS_OT_copy_logs_to_clipboard
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.save_logs_to_file import \
        GRIDMARKETS_OT_save_logs_to_file

    layout = self.layout
    props = context.scene.props
    log_history_container_props = props.log_history_container

    row = layout.box().row()

    row.template_list(GRIDMARKETS_UL_log_item.bl_idname, "",
                      log_history_container_props, "log_history_items",
                      log_history_container_props, "focused_log_item",
                      rows=6, sort_lock=True)

    col = row.column()
    col.alignment="RIGHT"
    col.scale_y = 1.4
    col.ui_units_x = 4.5
    col.menu(GRIDMARKETS_MT_logging_display_options.bl_idname, icon=constants.ICON_COLLAPSEMENU, text="Options")

    col.separator()

    sub = col.column(align = True)
    sub.operator(GRIDMARKETS_OT_clear_logs.bl_idname, icon=constants.ICON_TRASH, text="Clear logs")

    col.separator()

    sub = col.column(align=True)
    sub.operator(GRIDMARKETS_OT_copy_logs_to_clipboard.bl_idname, icon=constants.ICON_COPY_TO_CLIPBOARD, text="Copy logs")
    sub.operator(GRIDMARKETS_OT_save_logs_to_file.bl_idname, icon=constants.ICON_SAVE_TO_FILE, text="Save logs")

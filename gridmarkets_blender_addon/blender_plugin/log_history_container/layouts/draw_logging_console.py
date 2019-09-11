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
    from gridmarkets_blender_addon.blender_plugin.log_history_container.operators.toggle_logging_console import \
        GRIDMARKETS_OT_toggle_logging_console

    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    user_interface = plugin.get_user_interface()
    is_open = user_interface.is_logging_console_open()

    layout = self.layout
    props = context.scene.props
    log_history_container_props = props.log_history_container

    box = layout.box()

    row = box.row(align=True)

    row.operator(
        GRIDMARKETS_OT_toggle_logging_console.bl_idname,
        text="",
        icon=constants.ICON_DISCLOSURE_TRI_DOWN if is_open else constants.ICON_DISCLOSURE_TRI_RIGHT,
        emboss=False
    )

    row.label(icon=constants.ICON_CONSOLE, text="Logging console:")

    if is_open:
        sub = row.column()
        sub.alignment = "RIGHT"
        sub.menu(GRIDMARKETS_MT_logging_display_options.bl_idname, icon=constants.ICON_COLLAPSEMENU, text="Diplay options")


        row = box.row()
        row.template_list(GRIDMARKETS_UL_log_item.bl_idname, "",
                          log_history_container_props, "log_history_items",
                          log_history_container_props, "focused_log_item",
                          rows=6)

        col = row.column()
        col.alignment = "RIGHT"
        col.scale_y = 1.3

        sub = col.column(align=True)
        sub.operator(GRIDMARKETS_OT_clear_logs.bl_idname, icon=constants.ICON_TRASH, text="")

        col.separator()

        sub = col.column(align=True)
        sub.operator(GRIDMARKETS_OT_copy_logs_to_clipboard.bl_idname, icon=constants.ICON_COPY_TO_CLIPBOARD, text="")
        sub.operator(GRIDMARKETS_OT_save_logs_to_file.bl_idname, icon=constants.ICON_SAVE_TO_FILE, text="")

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


def draw_logging_controls(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_log_dates import \
        GRIDMARKETS_OT_toggle_show_log_dates
    from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_log_times import \
        GRIDMARKETS_OT_toggle_show_log_times
    from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_logger_names import \
        GRIDMARKETS_OT_toggle_show_logger_names

    plugin = PluginFetcher.get_plugin()
    user_interface = plugin.get_user_interface()

    show_dates = user_interface.show_log_dates()
    show_times = user_interface.show_log_times()
    show_names = user_interface.show_logger_names()

    layout = self.layout

    split = layout.split()

    col1 = split.column()
    row = col1.row()
    row.active = show_dates
    row.operator(GRIDMARKETS_OT_toggle_show_log_dates.bl_idname)

    col2 = split.column()
    row = col2.row()
    row.active = show_times
    row.operator(GRIDMARKETS_OT_toggle_show_log_times.bl_idname)

    row = layout.row()
    row.active = show_names
    row.operator(GRIDMARKETS_OT_toggle_show_logger_names.bl_idname)

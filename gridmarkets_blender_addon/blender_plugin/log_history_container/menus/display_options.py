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


class GRIDMARKETS_MT_logging_display_options(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_logging_display_options"
    bl_label = "Logging display options"

    def draw(self, context):
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_log_dates import \
            GRIDMARKETS_OT_toggle_show_log_dates
        from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_log_times import \
            GRIDMARKETS_OT_toggle_show_log_times
        from gridmarkets_blender_addon.blender_plugin.user_interface.operators.toggle_show_logger_names import \
            GRIDMARKETS_OT_toggle_show_logger_names

        layout = self.layout
        plugin = PluginFetcher.get_plugin()
        user_interface = plugin.get_user_interface()

        show_dates = user_interface.show_log_dates()
        show_times = user_interface.show_log_times()
        show_names = user_interface.show_logger_names()

        row = layout.row()
        icon = constants.ICON_CHECKBOX_SELECTED if show_dates else constants.ICON_CHECKBOX
        row.operator(GRIDMARKETS_OT_toggle_show_log_dates.bl_idname, text="Display dates", icon=icon)

        row = layout.row()
        icon = constants.ICON_CHECKBOX_SELECTED if show_times else constants.ICON_CHECKBOX
        row.operator(GRIDMARKETS_OT_toggle_show_log_times.bl_idname, text="Display times", icon=icon)

        row = layout.row()
        icon = constants.ICON_CHECKBOX_SELECTED if show_names else constants.ICON_CHECKBOX
        row.operator(GRIDMARKETS_OT_toggle_show_logger_names.bl_idname, text="Display logger names", icon=icon)


classes = (
    GRIDMARKETS_MT_logging_display_options,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

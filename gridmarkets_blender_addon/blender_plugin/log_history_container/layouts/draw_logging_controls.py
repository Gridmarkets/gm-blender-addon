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
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.clear_logs import \
        GRIDMARKETS_OT_clear_logs
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.copy_logs_to_clipboard import \
        GRIDMARKETS_OT_copy_logs_to_clipboard
    from gridmarkets_blender_addon.blender_plugin.logging_coordinator.operators.save_logs_to_file import \
        GRIDMARKETS_OT_save_logs_to_file

    layout = self.layout

    split = layout.split()

    col1 = split.column()
    col1.operator(GRIDMARKETS_OT_clear_logs.bl_idname)

    col2 = split.column()
    col2.operator(GRIDMARKETS_OT_copy_logs_to_clipboard.bl_idname)

    row = layout.row()
    row.operator(GRIDMARKETS_OT_save_logs_to_file.bl_idname)

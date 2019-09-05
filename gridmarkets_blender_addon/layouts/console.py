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

from gridmarkets_blender_addon import constants


def draw_console(self, context):
    layout = self.layout
    props = context.scene.props
    box = layout.box()

    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=6)

    split = box.split()
    col1 = split.column()
    col2 = split.column()

    col1.operator(constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME)
    col2.operator(constants.OPERATOR_CLEAR_LOGS_ID_NAME)

    box.operator(constants.OPERATOR_SAVE_LOGS_TO_FILE_ID_NAME)


def draw_compact_console(self, context):
    layout = self.layout
    props = context.scene.props
    box = layout.box()
    box.alignment = "RIGHT"
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=4)

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


def draw_sidebar(self, context):
    layout = self.layout
    props = context.scene.props

    layout.label(text="Links")

    col = layout.column()
    col.scale_x = 1
    col.scale_y = 2

    # Portal manager link
    col.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME, icon=constants.ICON_URL)

    # Cost calculator
    col.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME, icon=constants.ICON_URL)
    col.operator(constants.OPERATOR_OPEN_PREFERENCES_ID_NAME, icon=constants.ICON_PREFERENCES, text="Preferences")
    col.operator(constants.OPERATOR_OPEN_HELP_URL_ID_NAME, icon=constants.ICON_HELP)

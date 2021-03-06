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

__all__ = ['draw_header', 'draw_layout_option']

from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.operators.set_ui_layout import \
    GRIDMARKETS_OT_set_layout as _set_upload_method


def draw_header(layout, text: str, icon=constants.ICON_NONE, icon_value=0):
    row = layout.row()
    row.scale_y = 1.5
    row.label(text=text, icon=icon, icon_value=icon_value)


def draw_layout_option(layout, layout_tuple):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    user_interface = plugin.get_user_interface()
    ui_layout = user_interface.get_layout()

    layout.separator()

    row = layout.row()
    icon = constants.ICON_RADIOBUT_ON if ui_layout == layout_tuple[0] else constants.ICON_RADIOBUT_OFF
    row.operator(_set_upload_method.bl_idname, text=layout_tuple[1],
                 icon=icon).layout = layout_tuple[0]

    description = layout.row()
    description.label(text=layout_tuple[2])
    description.enabled = False
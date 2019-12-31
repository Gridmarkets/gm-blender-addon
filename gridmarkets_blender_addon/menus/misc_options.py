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

__all__ = ['GRIDMARKETS_MT_misc_options']

import bpy
from gridmarkets_blender_addon import constants
from .utils import draw_header, draw_operator_option


class GRIDMARKETS_MT_misc_options(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_misc_options"
    bl_label = "Misc"
    icon = constants.ICON_COLLAPSEMENU

    def draw(self, context):
        layout = self.layout
        draw_header(layout, "Miscellaneous:", icon=self.icon)
        draw_operator_option(layout, constants.UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_TUPLE)

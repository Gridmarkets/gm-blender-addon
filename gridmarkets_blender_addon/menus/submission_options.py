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

__all__ = ['GRIDMARKETS_MT_submit_options']

import bpy
from gridmarkets_blender_addon import constants
from .utils import draw_header, draw_operator_option


class GRIDMARKETS_MT_submit_options(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_submission_options"
    bl_label = "Submit"

    @staticmethod
    def get_icon():
        from gridmarkets_blender_addon.icon_loader import IconLoader
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        return preview_collection[constants.UPLOAD_ICON_ID].icon_id

    def draw(self, context):
        layout = self.layout
        layout.label(text="nothing here")

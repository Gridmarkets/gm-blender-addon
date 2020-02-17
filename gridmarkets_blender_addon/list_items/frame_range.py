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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_UL_frame_range(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """ Defines how frame range item is drawn in a template list """
        from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset

        row = layout.row()
        row.active = item.enabled

        # users should be familiar with the restrict render icon and understand what it denotes
        enabled_icon = (constants.ICON_RESTRICT_RENDER_OFF if item.enabled else constants.ICON_RESTRICT_RENDER_ON)

        attribute_key = active_propname[:-len(JobPreset.FRAME_RANGE_FOCUSED)]
        collection = getattr(data, attribute_key + JobPreset.FRAME_RANGE_COLLECTION)

        sub = row.row(align=True)
        sub.enabled = len(collection) > 1
        sub.prop(item, "enabled", icon=enabled_icon, text="", emboss=item.enabled)

        sub = row.row(align=True)
        sub.prop(item, "name", text="", expand=True, emboss=False)

        row.prop(item, "frame_start", text="Start")
        row.prop(item, "frame_end", text="End")
        row.prop(item, "frame_step", text="Step")

    def invoke(self, context, event):
        pass


classes = (
    GRIDMARKETS_UL_frame_range,
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

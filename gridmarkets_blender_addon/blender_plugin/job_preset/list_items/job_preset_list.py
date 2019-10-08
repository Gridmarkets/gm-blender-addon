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
from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
from gridmarkets_blender_addon.blender_plugin.log_item.property_groups.log_item_props import LogItemProps


class GRIDMARKETS_UL_job_preset(bpy.types.UIList):
    bl_idname = "GRIDMARKETS_UL_job_preset"

    def draw_item(self, context, layout, data, item: LogItemProps, icon, active_data, active_property, index=0,
                  flt_flag=0):

        from gridmarkets_blender_addon.blender_plugin.api_schema.api_schema import get_icon_for_job_definition

        plugin = PluginFetcher.get_plugin()
        job_preset_item = plugin.get_preferences_container().get_job_preset_container().get_at(index)
        job_definition = job_preset_item.get_job_definition()

        row = layout.row()

        icon = get_icon_for_job_definition(job_definition)
        row.prop(item, 'name', text='', emboss=False, translate=False, icon=icon[0], icon_value=icon[1])


classes = (
    GRIDMARKETS_UL_job_preset,
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

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

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_project import GRIDMARKETS_OT_upload_project
from gridmarkets_blender_addon.blender_plugin.project_attribute.layouts import draw_project_attribute
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants

def draw_pack_and_upload_current_scene(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    api_schema = plugin.get_api_client().get_api_schema()
    project_name_attribute =api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)

    # project name
    draw_project_attribute(layout, context, project_name_attribute, draw_linked_attributes=False)

    # product version
    render_engine = context.scene.render.engine
    if render_engine == constants.RENDER_ENGINE_VRAY_RT:
        product_version_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.VRAY_VERSION)
    else:
        product_version_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.BLENDER_VERSION)
    draw_project_attribute(layout, context, product_version_attribute, draw_linked_attributes=False)

    layout.separator()

    row = layout.row()
    row.operator(GRIDMARKETS_OT_upload_project.bl_idname)
    row.scale_y = 2.5

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

def draw_remote_project_container(layout: bpy.types.UILayout, context: bpy.types.Context):
    from gridmarkets_blender_addon import constants, utils_blender
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    from gridmarkets_blender_addon.blender_plugin.remote_project.layouts.draw_remote_project import draw_remote_project
    from gridmarkets_blender_addon.blender_plugin.remote_project.operators.open_remote_project_definition_popup import \
        GRIDMARKETS_OT_open_remote_project_definition_popup
    from gridmarkets_blender_addon.blender_plugin.remote_project.list_items.remote_project_list import \
        GRIDMARKETS_UL_remote_project

    props = context.scene.props
    plugin = PluginFetcher.get_plugin()
    user_interface = plugin.get_user_interface()

    def get_upload_tuple():
        method = user_interface.get_layout()
        for tuple in constants.LAYOUTS:
            if tuple[0] == method:
                return tuple
        raise RuntimeError("Could not find project action tuple")

    remote_project_container_props = props.remote_project_container

    # draw header
    row = layout.row(align=True)  #
    row.label(text="Remote Projects", icon=constants.ICON_REMOTE_PROJECT)
    row.operator(GRIDMARKETS_OT_open_remote_project_definition_popup.bl_idname, text="",
                 icon=constants.ICON_INFO, emboss=False)

    row = layout.row()
    col = row.column()
    col.template_list(GRIDMARKETS_UL_remote_project.bl_idname, "",
                      remote_project_container_props, "remote_projects",
                      remote_project_container_props, "focused_remote_project",
                      rows=2)

    draw_remote_project(layout, context)

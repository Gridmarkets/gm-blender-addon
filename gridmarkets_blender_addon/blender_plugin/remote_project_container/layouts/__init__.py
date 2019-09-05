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

def draw_remote_project_container(self, context):
    from types import SimpleNamespace
    from gridmarkets_blender_addon import constants
    from gridmarkets_blender_addon.layouts.projects import _draw_project_info_view, GRIDMARKETS_MT_add_new_project

    from gridmarkets_blender_addon.blender_plugin.remote_project.list_items.remote_project_list import GRIDMARKETS_UL_remote_project

    layout = self.layout
    props = context.scene.props
    remote_project_container_props = props.remote_project_container

    row = layout.row()
    row.template_list(GRIDMARKETS_UL_remote_project.bl_idname, "",
                      remote_project_container_props, "remote_projects",
                      remote_project_container_props, "focused_remote_project",
                      rows=2)

    row = layout.row(align=True)

    GRIDMARKETS_MT_add_new_project.draw(SimpleNamespace(layout=row), context)
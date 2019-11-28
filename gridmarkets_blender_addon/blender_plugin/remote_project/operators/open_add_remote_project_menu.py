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


class GRIDMARKETS_OT_open_add_project_menu(bpy.types.Operator):
    bl_idname = "gridmarkets.open_add_project_menu"
    bl_label = "Open Add Project Menu"
    bl_description = "Opens a menu of different ways of adding a new project"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        from gridmarkets_blender_addon.layouts.projects import GRIDMARKETS_MT_add_new_project
        bpy.ops.wm.call_menu(name=GRIDMARKETS_MT_add_new_project.bl_idname)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_open_add_project_menu,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

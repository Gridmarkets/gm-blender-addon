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


class GRIDMARKETS_OT_open_remote_project_definition_popup(bpy.types.Operator):
    bl_idname = "gridmarkets.open_remote_project_definition_popup"
    bl_label = "Open Remote Project Definition Pop-up"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        def draw_popup(self, context):
            from gridmarkets_blender_addon import constants

            layout = self.layout
            layout.alignment = "EXPAND"
            layout.label(text="Remote Projects:", icon=constants.ICON_REMOTE_PROJECT)

            col = layout.column(align=True)
            col.label(text="Remote Projects are projects that have been uploaded (or are uploading) to the " +
                           constants.COMPANY_NAME + " cloud.")
            col.label(text="There are many different sub-types of projects each with their own set of jobs that can " +
                           "be run against them. ")

        context.window_manager.popover(draw_popup, ui_units_x=30)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_open_remote_project_definition_popup,
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

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
from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager


class GRIDMARKETS_OT_copy_temporary_file_location(bpy.types.Operator):
    bl_idname = constants.OPERATOR_COPY_TEMPORARY_FILE_LOCATION_ID_NAME
    bl_label = constants.OPERATOR_COPY_TEMPORARY_FILE_LOCATION_LABEL
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.props
        project_count = len(props.projects)
        selected_project_index = props.selected_project

        # get the selected project
        if project_count > 0 and selected_project_index >= 0 and selected_project_index < project_count:
            project = props.projects[selected_project_index]
            temporary_directory_manager = TempDirectoryManager.get_temp_directory_manager()
            association = temporary_directory_manager.get_association_with_project_name(project.name)

            bpy.context.window_manager.clipboard = association.get_temp_dir_name()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_copy_temporary_file_location,
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

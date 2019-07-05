import bpy
import os
import constants
from temp_directory_manager import TempDirectoryManager

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_delete_temporary_project_files(bpy.types.Operator):
    bl_idname = constants.OPERATOR_DELETE_TEMPORARY_PROJECT_FILES_ID_NAME
    bl_label = constants.OPERATOR_DELETE_TEMPORARY_PROJECT_FILES_LABEL
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
            association.delete_temporary_directory()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_delete_temporary_project_files,
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

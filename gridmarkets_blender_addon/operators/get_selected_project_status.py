import bpy
import os
import constants
import utils_blender

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_selected_project_status(bpy.types.Operator):
    bl_idname = constants.OPERATOR_GET_SELECTED_PROJECT_STATUS_ID_NAME
    bl_label = constants.OPERATOR_GET_SELECTED_PROJECT_STATUS_LABEL
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.props
        project_count = len(props.projects)
        selected_project_index = props.selected_project

        # get the selected project
        if project_count > 0 and selected_project_index >= 0 and selected_project_index < project_count:
            project = props.projects[selected_project_index]
            utils_blender.get_project_status(project)

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_selected_project_status,
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

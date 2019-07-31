import bpy
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_copy_logs_to_clipboard(bpy.types.Operator):
    bl_idname = constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME
    bl_label = constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_LABEL
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}


    def execute(self, context):
        log.info("Copying logs to clipboard...")
        bpy.context.window_manager.clipboard = utils_blender.get_logs(self, context)
        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_copy_logs_to_clipboard,
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

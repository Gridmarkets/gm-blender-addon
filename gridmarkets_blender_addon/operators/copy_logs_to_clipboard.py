import bpy
import os
import constants

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_copy_logs_to_clipboard(bpy.types.Operator):
    bl_idname = constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME
    bl_label = constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_LABEL
    bl_icon = 'BLEND_FILE'
    bl_options = {'UNDO'}

    @staticmethod
    def _get_log_text(item):
        text = ''

        if item.date:
            text = text + item.date + ' '

        if item.time:
            text = text + item.time + ' '

        if item.name:
            text = text + item.name + ' ' + item.level + ' '

        text = text + item.body

        return text

    def execute(self, context):
        props = context.scene.props
        output = ''

        for log_item in props.log_items:
            output = output + os.linesep + GRIDMARKETS_OT_copy_logs_to_clipboard._get_log_text(log_item)

        log.info("Copying logs to clipboard...")
        bpy.context.window_manager.clipboard = output

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

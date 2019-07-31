import bpy
from bpy_extras.io_utils import ExportHelper
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_save_logs_to_file(bpy.types.Operator, ExportHelper):
    bl_idname = constants.OPERATOR_SAVE_LOGS_TO_FILE_ID_NAME
    bl_label = constants.OPERATOR_SAVE_LOGS_TO_FILE_LABEL

    filename_ext = ".txt"

    DEFAULT_FILTER = "*.txt"
    DEFAULT_NAME = "GM_blender_logs"

    filter_glob: bpy.props.StringProperty(
        default= DEFAULT_FILTER,
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    filepath: bpy.props.StringProperty(
        default= DEFAULT_NAME,
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        log.info("Writing logs to file \"%s\"..." % self.filepath);

        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(utils_blender.get_logs(self, context))
            f.close()

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_save_logs_to_file,
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

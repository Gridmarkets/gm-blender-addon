import bpy
import constants

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_toggle_submission_summary(bpy.types.Operator):
    """ Toggles the submission summary view to open / close it"""

    bl_idname = constants.OPERATOR_TOGGLE_SUBMISSION_SUMMARY_ID_NAME
    bl_label = constants.OPERATOR_TOGGLE_SUBMISSION_SUMMARY_label
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.props
        log.info("%s submission summary view" % ("Closing" if props.submission_summary_open else "Opening"))
        props.submission_summary_open = not props.submission_summary_open
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_toggle_submission_summary,
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

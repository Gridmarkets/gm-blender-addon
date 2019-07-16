import bpy
import constants

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_toggle_output_prefix_view(bpy.types.Operator):

    bl_idname = constants.OPERATOR_TOGGLE_OUTPUT_PREFIX_VIEW_ID_NAME
    bl_label = constants.OPERATOR_TOGGLE_OUTPUT_PREFIX_VIEW_LABEL
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.props
        log.info("%s output prefix view" % ("Closing" if props.custom_settings_views.output_prefix_view else "Opening"))
        props.custom_settings_views.output_prefix_view = not props.custom_settings_views.output_prefix_view
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_toggle_output_prefix_view,
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

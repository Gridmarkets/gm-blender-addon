import bpy
from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_open_help_url(bpy.types.Operator):
    """Class to represent the 'Help' operation. Opens the Add-on's help page in the user's browser."""

    bl_idname = constants.OPERATOR_OPEN_HELP_URL_ID_NAME
    bl_label = constants.OPERATOR_OPEN_HELP_URL_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        log.info("Opening documentation...")

        # open the render manager url in the users browser
        bpy.ops.wm.url_open(url=constants.HELP_URL)
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_help_url,
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

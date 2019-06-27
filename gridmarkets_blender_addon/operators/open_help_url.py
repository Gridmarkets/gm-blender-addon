import bpy
import constants


class GRIDMARKETS_OT_open_help_url(bpy.types.Operator):
    """Class to represent the 'Help' operation. Opens the Add-on's help page in the user's browser."""

    bl_idname = constants.OPERATOR_OPEN_HELP_URL_ID_NAME
    bl_label = constants.OPERATOR_OPEN_HELP_URL_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
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

import bpy
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_open_preferences(bpy.types.Operator):
    bl_idname = constants.OPERATOR_OPEN_PREFERENCES_ID_NAME
    bl_label = constants.OPERATOR_OPEN_PREFERENCES_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        log.info("Opening Gridmarkets add-on preferences menu...")

        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        context.user_preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = constants.ADDON_NAME

        mod, info = utils_blender.get_addon(constants.ADDON_NAME)

        # expand the preferences box
        info['show_expanded'] = True

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_preferences,
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

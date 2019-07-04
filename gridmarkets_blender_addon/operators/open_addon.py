import bpy
import constants
import utils_blender
from panels.main import GRIDMARKETS_PT_Main

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_open_preferences(bpy.types.Operator):
    bl_idname = constants.OPERATOR_OPEN_ADDON_ID_NAME
    bl_label = constants.OPERATOR_OPEN_ADDON_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        log.info("Opening Gridmarkets add-on preferences menu...")

        for window in context.window_manager.windows:
            screen = window.screen
            if screen.name == constants.INJECTED_SCREEN_NAME:

                # create a new context for the delete and close operations
                c = {"screen": screen, "window": window}

                # delete the screen for the existing add-on window
                # bpy.ops.screen.delete(c, 'INVOKE_DEFAULT')

                # close the existing add-on window so that it can be re-opened with focus
                # (no way in blender that I know of to change window focus so I delete and re-open)
                bpy.ops.wm.window_close(c, 'INVOKE_DEFAULT')

                return {'FINISHED'}

        # get the scenes render settings
        render = bpy.context.scene.render

        # save old settings so that they can be restored later
        old_settings = {'x': render.resolution_x,
                        'y': render.resolution_y,
                        'res_percent': render.resolution_percentage,
                        'display_mode': render.display_mode}

        # try finally block so that old settings are guaranteed to be restored
        try:
            pixel_size = context.preferences.system.pixel_size

            # Size multiplier to use when drawing custom user interface elements, so that they are scaled correctly on
            # screens with different DPI. This value is based on operating system DPI settings and Blender display scale
            scale_factor = context.preferences.system.ui_scale * pixel_size



            print("scale_factor", scale_factor)
            print("dpi", context.preferences.system.dpi)
            print("pixel_size", context.preferences.system.pixel_size)

            # set the new window settings
            render.resolution_x = constants.DEFAULT_WINDOW_WIDTH * scale_factor
            render.resolution_y = constants.DEFAULT_WINDOW_HIEGHT * scale_factor
            render.resolution_percentage = 100
            render.display_mode = "WINDOW"

            # Call image editor window. This window just happens to use the render resolution settings for its
            # dimensions.
            bpy.ops.render.view_show("INVOKE_DEFAULT")

            # duplicate this window to create a new window which we can use to hold the add-on. This is necessary
            # because the previous window is a 'special' blender window which will be re-used by other operators, if
            # we were to modify how it worked it could have unintended consequences.
            bpy.ops.screen.area_dupli("INVOKE_DEFAULT")

            # now close the first new window
            bpy.ops.wm.window_close("INVOKE_DEFAULT")

            # get all other windows
            windows = context.window_manager.windows

            # bpy.ops.screen.screen_set("INVOKE_DEFAULT", delta=2)

            # get screen, area, and regions
            window = windows[-1]
            screen = window.screen #bpy.context.window_manager.windows[-1].screen
            area = screen.areas[0]
            regions = area.regions

            # Change area type to the Preferences editor
            area.type = "PREFERENCES"

            # switch to the add-ons tab
            context.preferences.active_section = 'ADDONS'

            screen.name = constants.INJECTED_SCREEN_NAME

            #area.header_text_set(constants.ADDON_NAME)

            print()
            print("screen")
            print(dir(screen))

            print()
            print("area")
            print(dir(area))


        finally:
            # reset render settings
            render.resolution_x = old_settings['x']
            render.resolution_y = old_settings['y']
            render.resolution_percentage = old_settings['res_percent']
            render.display_mode = old_settings['display_mode']

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

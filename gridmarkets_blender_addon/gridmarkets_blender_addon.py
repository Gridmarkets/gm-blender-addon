import bpy

import constants
import properties
import utils
import utils_blender


from temp_directory_manager import TempDirectoryManager
from icon_loader import IconLoader
from invalid_input_error import InvalidInputError

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

# ------------------------------------------------------------------------
#    Lists
# ------------------------------------------------------------------------


class GRIDMARKETS_UL_frame_range(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """ A function which defines how each list item is drawn """

        row = layout.row()
        row.active = item.enabled

        # users should be familiar with the restrict render icon and understand what it denotes
        enabled_icon = ("RESTRICT_RENDER_OFF" if item.enabled else "RESTRICT_RENDER_ON")

        row.prop(item, "enabled", icon=enabled_icon, text="", emboss=item.enabled)
        row.label(text = item.name)
        row.prop(item, "frame_start", text="Start")
        row.prop(item, "frame_end", text="End")
        row.prop(item, "frame_step", text="Step")

    def invoke(self, context, event):
        pass


class GRIDMARKETS_UL_project(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon=constants.PROJECT_ICON)


class GRIDMARKETS_UL_job(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", icon=constants.JOB_ICON, emboss=False)


class GRIDMARKETS_UL_log(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        props = context.scene.props

        row = layout.row(align=True)
        row.alignment = 'LEFT'

        # line text
        row.alert = item.level == 'ERROR' # if the message is an error then colour red

        text = ''

        if item.date and props.show_log_dates:
            text = text + item.date + ' '

        if item.time and props.show_log_times:
            text = text + item.time + ' '

        if item.name and props.show_log_modules:
            text = text + item.name + ' '

        text = text + item.body

        row.label(text=text)

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class delete_unused_screens(bpy.types.Operator):
    bl_idname = "gridmarkets.delete_unused_screens"
    bl_label = "Delete unused screens"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        screen_items = list(map(lambda t: t[1], bpy.data.screens.items()))
        print()
        print("screen items")
        for screen_item in screen_items:
            print("name: ", screen_item.name)

        unused_screens = []
        for screen_item in screen_items:
            if screen_item.name.startswith("GRIDMARKETS_INJECTION_SCREEN"):
                unused_screens.append(screen_item)

        print()
        print("unused screens")
        for screen_item in unused_screens:
            print(screen_item.name)

        if screen_item in unused_screens:
            #bpy.ops.screen.delete({'screen': screen_item})


            """
            screen_to_delete = screen_item.name

            current_screen = bpy.context.window.screen.name
            delete = screen_to_delete
            bpy.ops.screen.delete({'screen': bpy.data.screens[delete]})
            bpy.context.window.screen = bpy.data.screens[current_screen]
            """

        #bpy.ops.screen.screen_set(delta=1)
        return {"FINISHED"}


class GRIDMARKETS_MT_options(bpy.types.Menu):

    bl_label = "Gridmarkets"
    bl_idname = "dks_sp.menu"

    def draw(self, context):

        layout = self.layout
        layout.label(text="bob")

        # get the Gridmarkets icon
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

        layout.operator(constants.OPERATOR_OPEN_ADDON_ID_NAME, icon_value=iconGM.icon_id, text="Open Add-on")
        #layout.operator(delete_unused_screens.bl_idname, icon_value=iconGM.icon_id, text="delete")
        layout.operator(constants.OPERATOR_OPEN_PREFERENCES_ID_NAME, icon="PREFERENCES", text="Preferences")


def draw_top_bar_menu_options(self, context):
    self.layout.separator()

    # get the Gridmarkets icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    if utils_blender.get_addon_window():
        text = 'Close Gridmarkets add-on'
    else:
        text = 'Open Gridmarkets add-on'

    self.layout.emboss = "PULLDOWN_MENU"
    self.layout.operator(constants.OPERATOR_OPEN_ADDON_ID_NAME, icon_value=iconGM.icon_id, text=text)
    #self.layout.menu(GRIDMARKETS_MT_options.bl_idname)

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


classes = (
    GRIDMARKETS_UL_frame_range,
    GRIDMARKETS_UL_project,
    GRIDMARKETS_UL_job,
    GRIDMARKETS_UL_log,
    delete_unused_screens,
    GRIDMARKETS_MT_options
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    if hasattr(bpy.types, "TOPBAR_MT_render"):
        # bpy.types.TOPBAR_MT_render.append(draw_top_bar_menu_options)
        bpy.types.TOPBAR_MT_editor_menus.append(draw_top_bar_menu_options)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

    if hasattr(bpy.types, "TOPBAR_MT_render"):
        #bpy.types.TOPBAR_MT_render.remove(draw_top_bar_menu_options)
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_top_bar_menu_options)

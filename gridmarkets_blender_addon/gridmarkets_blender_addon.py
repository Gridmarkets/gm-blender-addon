import bpy

import constants
import utils_blender
from icon_loader import IconLoader


def draw_top_bar_menu_options(self, context):
    """ Draws the top bar button that opens the add-on window

    :param self: The menu instance that's drawing this button
    :type self: bpy.types.Menu
    :param context: The blender context
    :type context: bpy.context
    :rtype: void
    """

    self.layout.separator()

    # get the Gridmarkets icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    if utils_blender.get_addon_window():
        text = 'Close Gridmarkets add-on'
    else:
        text = 'Open Gridmarkets add-on'

    self.layout.emboss = "PULLDOWN_MENU"

    # todo work out why reloading the script does not work
    if hasattr(bpy.types, 'GRIDMARKETS_OT_open_addon'):
        self.layout.operator(constants.OPERATOR_OPEN_ADDON_ID_NAME, icon_value=iconGM.icon_id, text=text)


def register():
    if hasattr(bpy.types, "TOPBAR_MT_render"):
        bpy.types.TOPBAR_MT_editor_menus.append(draw_top_bar_menu_options)


def unregister():
    if hasattr(bpy.types, "TOPBAR_MT_render"):
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_top_bar_menu_options)

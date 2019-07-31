import bpy

from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.icon_loader import IconLoader

_old_header_draw = None


def draw_GM_operator(layout, context):
    # get the Gridmarkets icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    if utils_blender.get_addon_window():
        text = 'Close Gridmarkets add-on'
    else:
        text = 'Open Gridmarkets add-on'

    layout.operator(constants.OPERATOR_OPEN_ADDON_ID_NAME, icon_value=iconGM.icon_id, text=text)


def draw_top_bar_menu_options(layout, context):
    """ Draws the top bar button that opens the add-on window

    :param self: The menu instance that's drawing this button
    :type self: bpy.types.Menu
    :param context: The blender context
    :type context: bpy.context
    :rtype: void
    """

    # call the old dar menu method to draw the normal menu elements
    _old_header_draw(layout, context)

    layout.separator()

    # then draw a button to open the GM blender add-on main window
    draw_GM_operator(layout, context)


def register():
    global _old_header_draw
    _old_header_draw = bpy.types.INFO_MT_editor_menus.draw_menus

    bpy.types.INFO_MT_editor_menus.draw_menus = draw_top_bar_menu_options


def unregister():
    bpy.types.INFO_MT_editor_menus.draw_menus = _old_header_draw


# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2021  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "GridMarkets Blender Add-on",
    "description": "Allows users to submit Blender jobs to the GridMarkets render farm from within Blender.",
    "author": "GridMarkets",
    "version": (2, 2, 1),
    "blender": (2, 80, 0),
    "location": "Info > Header",
    "warning": "", # used for warning icon and text in add-ons panel
    "wiki_url": "https://www.gridmarkets.com/blender",
    "category": "Render"
}

import bpy

import os
import sys
import typing

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR_DIR = PARENT_DIR

LOGGER_NAME = 'gridmarkets_blender_addon'
PRODUCT = 'blender'
META_INFO = 'gridmarkets_blender_addon version: {}\nblender version: {}'.format(str(bl_info.get('version', '')),
                                                                                str(bpy.app.version))
DEBUG_MODE = os.path.exists(os.path.join(PARENT_DIR, 'debug'))


import configparser
config = configparser.ConfigParser()
config.read(os.path.join(CONFIG_DIR_DIR, 'config.ini'))
ENVOY_PYTHON_PATH = config['default']['ENVOY_PYTHON_PATH']
if config.has_section('submit2gm'):
    SUBMIT2GM_PATH = config.get('submit2gm', 'SUBMIT2GM_PATH')
else:
    SUBMIT2GM_PATH = config.get('default', 'SUBMIT2GM_PATH')

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"
GRIDMARKETS_LOGO_ID = "gridmarkets_logo"
GM_GREYSCALE_LOGO = "logo_greyscale.png"
MAIN_COLLECTION_ID = "main"

# Operator constants
OPERATOR_OPEN_SUBMIT2GM_ID_NAME = "gridmarkets.open_submit2gm"
OPERATOR_OPEN_SUBMIT2GM_LABEL = "Open Submit2gm"
OPERATOR_PRINT_DEBUG_STATUS_ID_NAME = "gridmarkets.print_debug_status"
OPERATOR_PRINT_DEBUG_STATUS_LABEL = "Print debug status"
OPERATOR_RAISE_WINDOW_ID_NAME = "gridmarkets.raise_window"
OPERATOR_RAISE_WINDOW_LABEL = "Raise window"
OPERATOR_STOP_SUBMIT2GM_ID_NAME = "gridmarkets.stop_submit2gm"
OPERATOR_STOP_SUBMIT2GM_LABEL = "Stop Submit2gm"
MENU_DEBUG_ID_NAME = "GRIDMARKETS_MT_gm_debug_menu"
MENU_DEBUG_LABEL = "GM Debug"

TOP_BAR_LABEL = 'Open GridMarkets add-on'

# pre-append the lib folder to sys.path so local dependencies can be found. Pre-append so that these paths take
# precedence over blender's existing packed modules which can be different versions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))


class IconLoader:
    """ Singleton class for loading custom icons """

    # Used to store any previews for images
    _icon_preview_collections = {}
    _initialised = False

    @staticmethod
    def get_preview_collections():
        """ Getter
        :return: Returns the icon preview collections dictionary that stores all loaded icon previews
        :rtype: Dictionary of previews
        """
        if not IconLoader._initialised:
            IconLoader._register_icons()

        return IconLoader._icon_preview_collections

    @staticmethod
    def initialise():
        """ Initialise the singleton

        :return: The new instance of an IconLoader
        :rtype: IconLoader
        """

        if not IconLoader._initialised:
            IconLoader._register_icons()
        else:
            raise Exception("Attempted to initialise IconLoader twice.")

    @staticmethod
    def _register_icons():
        """ loads icons from the /icons folder and stores their previews"""

        from bpy.utils import previews

        # create new icon previews collection
        preview_collection = bpy.utils.previews.new()

        # path to the folder where the icon is
        # the path is calculated relative to this py file inside the add-on folder
        my_icons_dir = os.path.join(os.path.dirname(__file__), ICONS_FOLDER)

        # load a preview thumbnail of the icon and store in the previews collection
        preview_collection.load(GRIDMARKETS_LOGO_ID,
                                os.path.join(my_icons_dir, GM_GREYSCALE_LOGO),
                                'IMAGE')

        IconLoader._icon_preview_collections[MAIN_COLLECTION_ID] = preview_collection

        IconLoader._initialised = True

    @staticmethod
    def clean_up():
        """ Removes all the previews from the preview collection and then removes the collection itself """

        if IconLoader._initialised:
            # clear the preview collections object of icons
            for preview_collection in IconLoader._icon_preview_collections.values():
                bpy.utils.previews.remove(preview_collection)

            IconLoader._icon_preview_collections.clear()
            IconLoader._initialised = False


def draw_top_bar(self, context: bpy.types.Context) -> None:
    """ Draws the top bar button that opens the add-on window

    :param self: The menu instance that's drawing this button
    :type self: bpy.types.Menu
    :param context: The blender context
    :type context: bpy.context
    :rtype: void
    """

    self.layout.separator()

    # get the GridMarkets icon
    preview_collection = IconLoader.get_preview_collections()[MAIN_COLLECTION_ID]
    iconGM = preview_collection[GRIDMARKETS_LOGO_ID]

    self.layout.emboss = "PULLDOWN_MENU"
    self.layout.operator(OPERATOR_OPEN_SUBMIT2GM_ID_NAME, icon_value=iconGM.icon_id, text=TOP_BAR_LABEL)

    if DEBUG_MODE:
        self.layout.menu(MENU_DEBUG_ID_NAME)


@bpy.app.handlers.persistent
def process_qt_events() -> float:
    try:
        from submit2gm.command_port_server_utils import process_events
        process_events()
    except ImportError:
        pass

    return 0.01


def close_application() -> None:
    try:
        from submit2gm.command_port_server_utils import stop_submit2gm
        stop_submit2gm()
    except ImportError as e:
        print(e)
        pass


def evaluate_code(code: str, return_variables: typing.List[str]):

    # Execute the provided code
    try:
        exec(code)
    except Exception as e:
        print("exception:", e)
        raise e

    results = {}

    for variable in return_variables:
        results[variable] = eval(variable)

    return results


def import_submit2gm():
    # Get the location of the submit2gm python package
    submit2gm_package_path = os.path.join(os.path.dirname(SUBMIT2GM_PATH), 'submit2gm')

    # Import the submit2gm package
    submit2gm_init_path = os.path.join(submit2gm_package_path, "__init__.py")

    from importlib import util as importlib_util
    spec = importlib_util.spec_from_file_location('submit2gm', submit2gm_init_path)
    module = importlib_util.module_from_spec(spec)

    sys.modules[spec.name] = module
    spec.loader.exec_module(module)


class GRIDMARKETS_OT_open_submit2gm(bpy.types.Operator):
    """ Opens the GridMarkets Submit2gm app."""

    bl_idname = OPERATOR_OPEN_SUBMIT2GM_ID_NAME
    bl_label = OPERATOR_OPEN_SUBMIT2GM_LABEL
    bl_options = {'REGISTER'}

    def execute(self, context: bpy.types.Context):
        import_submit2gm()

        from submit2gm.command_port_server_utils import start_command_port_server
        start_command_port_server(ENVOY_PYTHON_PATH,
                                  LOGGER_NAME,
                                  PRODUCT,
                                  META_INFO,
                                  evaluate_code,
                                  DEBUG_MODE)

        return {"FINISHED"}


class GRIDMARKETS_OT_print_debug_status(bpy.types.Operator):
    """ Prints debug information surrounding the command_port_utils state."""

    bl_idname = OPERATOR_PRINT_DEBUG_STATUS_ID_NAME
    bl_label = OPERATOR_PRINT_DEBUG_STATUS_LABEL
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context: bpy.types.Context):
        import_submit2gm()
        from submit2gm.command_port_server_utils import print_debug_status
        print_debug_status()
        return {"FINISHED"}


class GRIDMARKETS_OT_raise_window_status(bpy.types.Operator):
    """ Raises the GridMarkets Submit2gm app window."""

    bl_idname = OPERATOR_RAISE_WINDOW_ID_NAME
    bl_label = OPERATOR_RAISE_WINDOW_LABEL
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context: bpy.types.Context):
        import_submit2gm()
        from submit2gm.command_port_server_utils import raise_window
        raise_window()
        return {"FINISHED"}


class GRIDMARKETS_OT_stop_submit2gm_status(bpy.types.Operator):
    """ Stops the GridMarkets Submit2gm app."""

    bl_idname = OPERATOR_STOP_SUBMIT2GM_ID_NAME
    bl_label = OPERATOR_STOP_SUBMIT2GM_LABEL
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context: bpy.types.Context):
        import_submit2gm()
        from submit2gm.command_port_server_utils import stop_submit2gm
        stop_submit2gm()
        return {"FINISHED"}


class GRIDMARKETS_MT_debug_menu(bpy.types.Menu):
    bl_idname = MENU_DEBUG_ID_NAME
    bl_label = MENU_DEBUG_LABEL

    def draw(self, context):
        layout = self.layout
        layout.operator(OPERATOR_PRINT_DEBUG_STATUS_ID_NAME)
        layout.operator(OPERATOR_RAISE_WINDOW_ID_NAME)
        layout.operator(OPERATOR_STOP_SUBMIT2GM_ID_NAME)


classes = (
    GRIDMARKETS_OT_open_submit2gm,
    GRIDMARKETS_OT_print_debug_status,
    GRIDMARKETS_OT_raise_window_status,
    GRIDMARKETS_OT_stop_submit2gm_status,
    GRIDMARKETS_MT_debug_menu
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    IconLoader.initialise()
    bpy.types.TOPBAR_MT_editor_menus.append(draw_top_bar)

    # Start a timer for processing qt events
    bpy.app.timers.register(process_qt_events, persistent=True)

    import atexit
    atexit.register(close_application)


def unregister():
    from bpy.utils import unregister_class

    # Unregister the qt event timer
    if bpy.app.timers.is_registered(process_qt_events):
        bpy.app.timers.unregister(process_qt_events)

    bpy.types.TOPBAR_MT_editor_menus.remove(draw_top_bar)
    IconLoader.clean_up()

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

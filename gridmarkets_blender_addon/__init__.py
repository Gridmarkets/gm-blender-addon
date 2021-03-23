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
    "version": (2, 0, 0),
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

import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
ENVOY_PYTHON_PATH = config['default']['ENVOY_PYTHON_PATH']
SUBMIT2GM_PATH = config['default']['SUBMIT2GM_PATH']

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"
GRIDMARKETS_LOGO_ID = "gridmarkets_logo"
GM_GREYSCALE_LOGO = "logo_greyscale.png"
MAIN_COLLECTION_ID = "main"
OPERATOR_OPEN_SUBMIT2GM_ID_NAME = "gridmarkets.open_submit2gm"
OPERATOR_OPEN_SUBMIT2GM_LABEL = "Open Submit2gm"
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


class GRIDMARKETS_OT_open_submit2gm(bpy.types.Operator):
    """ Opens the GridMarkets Submit2gm app."""

    bl_idname = OPERATOR_OPEN_SUBMIT2GM_ID_NAME
    bl_label = OPERATOR_OPEN_SUBMIT2GM_LABEL
    bl_options = {'REGISTER'}

    def import_submit2gm(self):
        # Get the location of the submit2gm python package
        submit2gm_package_path = os.path.join(os.path.dirname(SUBMIT2GM_PATH), 'submit2gm')

        # Import the submit2gm package
        submit2gm_init_path = os.path.join(submit2gm_package_path, "__init__.py")

        from importlib import util as importlib_util
        spec = importlib_util.spec_from_file_location('submit2gm', submit2gm_init_path)
        module = importlib_util.module_from_spec(spec)

        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

    def execute(self, context: bpy.types.Context):
        self.import_submit2gm()

        from submit2gm.command_port_server_utils import start_command_port_server
        envoy_python_path = ENVOY_PYTHON_PATH
        logger_name = 'gridmarkets_blender_addon'
        product = 'blender'
        meta_info = 'gridmarkets_blender_addon version: ' + str(bl_info.get('version', '')) + '\n'
        meta_info += 'blender version: ' + str(bpy.app.version)
        evaluate_code_cb = evaluate_code
        debug_mode = True

        start_command_port_server(envoy_python_path, logger_name, product, meta_info, evaluate_code_cb, debug_mode)

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_submit2gm,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    IconLoader.initialise()
    bpy.types.TOPBAR_MT_editor_menus.append(draw_top_bar)


def unregister():
    from bpy.utils import unregister_class

    bpy.types.TOPBAR_MT_editor_menus.remove(draw_top_bar)
    IconLoader.clean_up()

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

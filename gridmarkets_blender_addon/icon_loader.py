# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
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

import bpy
import os
from gridmarkets_blender_addon import constants


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
        my_icons_dir = os.path.join(os.path.dirname(__file__), constants.ICONS_FOLDER)

        # load a preview thumbnail of the icon and store in the previews collection
        preview_collection.load(constants.GRIDMARKETS_LOGO_ID,
                                os.path.join(my_icons_dir, constants.GM_GREYSCALE_LOGO),
                                'IMAGE')

        # load a preview thumbnail of the icon and store in the previews collection
        preview_collection.load(constants.VRAY_LOGO_ID,
                                os.path.join(my_icons_dir, constants.VRAY_LOGO),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_0_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_0),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_1_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_1),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_2_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_2),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_3_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_3),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_4_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_4),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_5_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_5),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_6_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_6),
                                'IMAGE')

        preview_collection.load(constants.CUSTOM_SPINNER_ICON_7_ID,
                                os.path.join(my_icons_dir, constants.CUSTOM_SPINNER_ICON_7),
                                'IMAGE')

        IconLoader._icon_preview_collections[constants.MAIN_COLLECTION_ID] = preview_collection

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


def register():
    # initialise the singleton
    IconLoader.initialise()


def unregister():
    # clean up instance
    IconLoader.clean_up()

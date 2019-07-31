import bpy
import os
from gridmarkets_blender_addon import constants


class IconLoader:
    """ Singleton class for loading custom icons """

    # Used to store any previews for images (In this case the Gridmarkets custom icon)
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
                                os.path.join(my_icons_dir,
                                             constants.GM_COLOURED_LOGO),
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

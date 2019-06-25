import bpy
import pathlib
import os


import constants
import utils

from invalid_input_error import InvalidInputError
from property_sanitizer import PropertySanitizer
from temp_directory_manager import TempDirectoryManager
from validation_response import ValidationResponse

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

def validate_credentials(email = None, access_key = None):
    """Blender specific authentication validator, uses the gridmarkets validate_auth() function internally but adds
        additional checks and blender specific error messages.

    :param email: The user's Gridmarkets account email, if None or not given then it will be read from the preferences
    :type email: str
    :param access_key: The user's Gridmarkets access key, if None or not given then it will be read from the preferences
    :type access_key: str
    :return: true if credentials are valid
    :rtype: bool

    :raises: InvalidInputError, AuthenticationError
    """

    # only read from preferences if a parameter is None
    if email == None or access_key == None:

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        if email == None:
            email = addon_prefs.auth_email

        if access_key == None:
            access_key = addon_prefs.auth_accessKey

    hasEmail = False
    hasKey = False

    # check an email address has been entered
    if isinstance(email, str) and len(email) > 0:
        hasEmail = True

    # check a auth key has been entered
    if isinstance(access_key, str) and len(access_key) > 0:
        hasKey = True

    # validate
    if not hasEmail and not hasKey:
        raise InvalidInputError(message="No Gridmarkets email address or access key provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)
    elif not hasEmail:
        raise InvalidInputError(message="No Gridmarketes email address provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)
    elif not hasKey:
        raise InvalidInputError(message="No Gridmarketes access key provided." +
                                        constants.AUTHENTICATION_HELP_MESSAGE)

    # if initial checks pass try the Gridmarkets validate_auth function
    # create an instance of Envoy client
    client = EnvoyClient(email=email, access_key=access_key)
    client.validate_auth()

    return True


def get_new_envoy_client():
    """ Gets a new EnvoyClient instance using the authentication preferences for credentials

    :return: The envoy client
    :rtype: EnvoyClient

    :raises: InvalidInputError, AuthenticationError
    """

    # get the add-on preferences
    addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

    # validate the authentication credentials
    validation_response = validate_credentials(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)

    # return the new client
    return EnvoyClient(email=addon_prefs.auth_email, access_key=addon_prefs.auth_accessKey)



def upload_project(project_name, temp_dir_manager):
    """

    :param project_name: The name of the project as it will appear in Envoy
    :type project_name: str
    :param temp_dir_manager: The temporary directory manager used to store packed projects
    :type temp_dir_manager: TempDirectoryManager
    :rtype: void
    :raises: InvalidInputError, AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
    """

    # create an instance of Envoy client
    client = get_new_envoy_client()

    blend_file_name = None

    # if the file has been saved
    if bpy.context.blend_data.is_saved:
        # use the name of the saved .blend file
        blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
    else:
        # otherwise create a name for the packed .blend file
        blend_file_name = 'main_GM_blend_file_packed.blend'

    # create a new temp directory
    temp_dir_path = temp_dir_manager.get_temp_directory()

    blend_file_path = temp_dir_path / blend_file_name

    # save a copy of the current scene to the temp directory. This is so that if the file has not been saved
    # or if it has been modified since it's last save then the submitted .blend file will represent the
    # current state of the scene
    bpy.ops.wm.save_as_mainfile(copy=True, filepath=str(blend_file_path), relative_remap=True,
                                compress=True)

    # create directory to contain packed project
    packed_dir = temp_dir_path / project_name
    os.mkdir(str(packed_dir))

    # pack the .blend file to the pack directory
    utils.pack_blend_file(str(blend_file_path), str(packed_dir))

    # delete pack-info.txt if it exists
    pack_info_file = pathlib.Path(packed_dir / 'pack-info.txt')
    if pack_info_file.is_file():
        pack_info_file.unlink()

    # create the project
    project = Project(str(packed_dir), project_name)

    # associate this project with the temp directory so the temp directory can be removed once the project is
    # complete
    temp_dir_manager.associate_project(temp_dir_path, project)

    # add files to project
    # only files and folders within the project path can be added, use relative or full path
    # any other paths passed will be ignored
    project.add_folders(str(packed_dir))

    # submit project
    resp = client.submit_project(project)  # returns project name

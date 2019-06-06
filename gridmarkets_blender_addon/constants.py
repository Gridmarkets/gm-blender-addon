# the add-ons package name
ADDON_PACKAGE_NAME = "gridmarkets_blender_addon"

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"

# the name of the gridmarkets logo file
LOGO_ICON_FILE_NAME = "logo.png"

# directory for the add-on to output temporary files
TEMP_FILES_FOLDER = ".gm_temp_files"

# the url of the render manager
RENDER_MANAGER_URL = "https://portal.gridmarkets.com/init/member_plugin/index"

# relative paths in blender start with a double /
DEFAULT_OUTPUT_PATH = "//gm_results\\"

# plugin versioning
PLUGIN_VERSION = { "major": 0, "minor": 3, "build" : 2}

FRAME_RANGE_PREFIX = 'range_'
DEFAULT_FRAME_RANGE_START_VALUE = 1
DEFAULT_FRAME_RANGE_END_VALUE = 255
DEFAULT_FRAME_RANGE_STEP_VALUE = 1


# register module
def register():
    pass


# unregister module
def unregister():
    pass
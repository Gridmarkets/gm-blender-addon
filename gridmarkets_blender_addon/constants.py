# the add-ons package name
ADDON_PACKAGE_NAME = "gridmarkets_blender_addon"

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"

# the name of the gridmarkets logo file
LOGO_ICON_FILE_NAME = "logo.png"

GRIDMARKETS_LOGO_ID = "gridmarkets_logo"
MAIN_COLLECTION_ID = "main"

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

PANEL_MAIN_ID_NAME = "gridmarkets_main_panel"
PANEL_MAIN_ID_LABEL = "GridMarkets"
PANEL_JOB_INFO_ID_NAME = "gridmarkets_job_info_sub_panel"
PANEL_JOB_INFO_LABEL = "Job Info"
PANEL_RENDER_SETTINGS_ID_NAME = "gridmarkets_render_settings_sub_panel"
PANEL_RENDER_SETTINGS_LABEL = "Render Settings"
PANEL_OUTPUT_SETTINGS_ID_NAME = "gridmarkets_output_settings_sub_panel"
PANEL_OUTPUT_SETTINGS_LABEL = "Output Settings"
PANEL_SPACE_TYPE = "PROPERTIES"
PANEL_REGION_TYPE = "WINDOW"
PANEL_CONTEXT = "render"

OPERATOR_SUBMIT_ID_NAME = "gridmarkets.render"
OPERATOR_SUBMIT_LABEL = "Submit"
OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME = "gridmarkets.open_portal"
OPERATOR_OPEN_MANAGER_PORTAL_LABEL = "Open Manager Portal"
OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME = "gridmarkets.list_action"
OPERATOR_FRAME_RANGE_ACTIONS_LABEL = "List Action"
OPERATOR_EDIT_FRAME_RANGE_ID_NAME = "gridmarkets.edit_frame_range"
OPERATOR_EDIT_FRAME_RANGE_LABEL = "Edit Frame Range"

# register module
def register():
    pass


# unregister module
def unregister():
    pass
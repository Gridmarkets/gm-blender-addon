"""
Constants used throughout the add-on

Stored in one central file to prevent circular dependencies
"""

# the add-ons package name
ADDON_PACKAGE_NAME = "gridmarkets_blender_addon"

# the name to search for in blenders add-on list
ADDON_NAME = "Gridmarkets Blender Add-on"

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"

# the name of the gridmarkets logo file
GM_COLOURED_LOGO = "logo.png"
GM_GREYSCALE_LOGO = "logo_greyscale.png"

GRIDMARKETS_LOGO_ID = "gridmarkets_logo"
MAIN_COLLECTION_ID = "main"

# directory for the add-on to output temporary files
TEMP_FILES_FOLDER = ".gm_temp_files"

BLEND_FILE_EXTENSION = ".blend"

# the url of the render manager
RENDER_MANAGER_URL = "https://portal.gridmarkets.com/init/member_plugin/index"

COST_CALCULATOR_URL = "https://www.gridmarkets.com/calculator"

HELP_URL = "https://www.gridmarkets.com/blender"

# relative paths in blender start with a double /
DEFAULT_OUTPUT_PATH = "//gm_results\\"

DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HIEGHT = 550

BLENDER_TEMP_DIRECTORY = '/tmp\\'

# plugin version
PLUGIN_VERSION = { "major": 0, "minor": 4, "build" : 1}

PROJECT_PREFIX = 'Project_'
JOB_PREFIX = 'Job_'

AUTHENTICATION_HELP_MESSAGE = "\nEnter your Gridmarkets credentials by going to: Edit -> Preferences -> Add-ons -> " \
                              "Gridmarkets Blender Add-on -> preferences"

TEMPORARY_FILES_DELETED = "Temporary Files Deleted"

FRAME_RANGE_PREFIX = 'range_'
DEFAULT_FRAME_RANGE_START_VALUE = 1
DEFAULT_FRAME_RANGE_END_VALUE = 255
DEFAULT_FRAME_RANGE_STEP_VALUE = 1

INJECTED_SCREEN_NAME = "GRIDMARKETS_INJECTION_SCREEN"

# panels
PANEL_MAIN_ID_NAME = "GRIDMARKETS_PT_Main"
PANEL_MAIN_ID_LABEL = "GridMarkets"

PANEL_PROJECTS_ID_NAME = "GRIDMARKETS_PT_Projects"
PANEL_PROJECTS_LABEL = "Projects"

PANEL_JOBS_ID_NAME = "GRIDMARKETS_PT_Jobs"
PANEL_JOBS_LABEL = "Jobs"

PANEL_OUTPUT_SETTINGS_ID_NAME = "GRIDMARKETS_PT_Output_Settings"
PANEL_OUTPUT_SETTINGS_LABEL = "Output Settings"

PANEL_CONSOLE_ID_NAME = "GRIDMARKETS_PT_console"
PANEL_CONSOLE_LABEL = "Console"

PANEL_PREFERENCES_ID_NAME = "GRIDMARKETS_PT_preferences"
PANEL_PREFERENCES_LABEL = "Preferences"

PANEL_SPACE_TYPE = "PROPERTIES"
PANEL_REGION_TYPE = "WINDOW"
PANEL_CONTEXT = "render"

WINDOW_SPACE_TYPE = "PREFERENCES"

# operators
OPERATOR_SUBMIT_ID_NAME = "gridmarkets.render"
OPERATOR_SUBMIT_LABEL = "Submit"
OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME = "gridmarkets.open_portal"
OPERATOR_OPEN_MANAGER_PORTAL_LABEL = "Open Manager Portal"
OPERATOR_OPEN_COST_CALCULATOR_ID_NAME = "gridmarkets.open_cost_calculator"
OPERATOR_OPEN_COST_CALCULATOR_LABEL = "Cost Calculator"
OPERATOR_OPEN_HELP_URL_ID_NAME = "gridmarkets.open_help_url"
OPERATOR_OPEN_HELP_URL_LABEL = "Help"
OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME = "gridmarkets.project_list_actions"
OPERATOR_PROJECT_LIST_ACTIONS_LABEL = "Project List Actions"
OPERATOR_JOB_LIST_ACTIONS_ID_NAME= "gridmarkets.job_list_actions"
OPERATOR_JOB_LIST_ACTIONS_LABEL = "Job List Actions"
OPERATOR_UPLOAD_PROJECT_ID_NAME = "gridmarkets.upload_project"
OPERATOR_UPLOAD_PROJECT_LABEL = "Upload Project"
OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME = "gridmarkets.frame_range_list_actions"
OPERATOR_FRAME_RANGE_LIST_ACTIONS_LABEL = "Frame Range List Actions"
OPERATOR_EDIT_FRAME_RANGE_ID_NAME = "gridmarkets.edit_frame_range"
OPERATOR_EDIT_FRAME_RANGE_LABEL = "Edit Frame Range"
OPERATOR_TRACE_PROJECT_ID_NAME = "gridmarkets.trace_blend_file"
OPERATOR_TRACE_PROJECT_LABEL = "Trace .blend file"
OPERATOR_TOGGLE_SUBMISSION_SUMMARY_ID_NAME = "gridmarkets.toggle_submission_summary"
OPERATOR_TOGGLE_SUBMISSION_SUMMARY_LABEL = "Toggle submission summary"
OPERATOR_TOGGLE_FRAME_RANGES_VIEW_ID_NAME = "gridmarkets.toggle_frame_ranges_view"
OPERATOR_TOGGLE_FRAME_RANGES_VIEW_LABEL = "Toggle frame ranges view"
OPERATOR_TOGGLE_OUTPUT_FORMAT_VIEW_ID_NAME = "gridmarkets.toggle_output_format_view"
OPERATOR_TOGGLE_OUTPUT_FORMAT_VIEW_LABEL = "Toggle output format view"
OPERATOR_TOGGLE_OUTPUT_PATH_VIEW_ID_NAME = "gridmarkets.toggle_output_path_view"
OPERATOR_TOGGLE_OUTPUT_PATH_VIEW_LABEL = "Toggle output path view"
OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_ID_NAME = "gridmarkets.toggle_render_engine_view"
OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_LABEL = "Toggle render engine view"
OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME = "gridmarkets.copy_logs_to_clipboard"
OPERATOR_COPY_LOGS_TO_CLIPBOARD_LABEL = "Copy logs to clipboard"
OPERATOR_OPEN_PREFERENCES_ID_NAME = "gridmarkets.open_preferences"
OPERATOR_OPEN_PREFERENCES_LABEL = "Open Gridmarkets add-on preferences"
OPERATOR_OPEN_ADDON_ID_NAME = "gridmarkets.open_addon"
OPERATOR_OPEN_ADDON_LABEL = "Open Gridmarkets add-on"
OPERATOR_COPY_TEMPORARY_FILE_LOCATION_ID_NAME = "gridmarkets.delete_temporary_project_files"
OPERATOR_COPY_TEMPORARY_FILE_LOCATION_LABEL = "Delete temporary project files"
OPERATOR_GET_SELECTED_PROJECT_STATUS_ID_NAME = "gridmarkets.get_selected_project_status"
OPERATOR_GET_SELECTED_PROJECT_STATUS_LABEL = "Get selected project status"

# enum values
PROJECT_OPTIONS_STATIC_COUNT = 1
PROJECT_OPTIONS_NEW_PROJECT_VALUE = 'NEW_PROJECT'
PROJECT_OPTIONS_NEW_PROJECT_LABEL = 'Submit Scene as New Project'
PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION = 'Upload the current scene as a new project to Gridmarkets'

JOB_OPTIONS_STATIC_COUNT = 1
JOB_OPTIONS_BLENDERS_SETTINGS_VALUE = "BLENDER_JOB_SETTINGS"
JOB_OPTIONS_BLENDERS_SETTINGS_LABEL = "Use Blender's Render Settings"
JOB_OPTIONS_BLENDERS_SETTINGS_DESCRIPTION = "Use Blender's render settings when determining the job options."

# API constants
JOB_PRODUCT_TYPE = "blender"
JOB_PRODUCT_VERSION = "2.80"
JOB_OPERATION = "render"

# add-on tabs
TAB_SUBMISSION_SETTINGS = "Submission Settings"
TAB_PROJECTS = "Projects"
TAB_JOB_PRESETS = "Job Presets"
TAB_CREDENTIALS = "Credentials"
TAB_LOGGING = "Logging Output"

# icons
ICON_ADD = "ADD"
ICON_REMOVE = "REMOVE"
ICON_MODIFIER = "MODIFIER"
ICON_TRIA_UP = "TRIA_UP"
ICON_TRIA_DOWN = "TRIA_DOWN"
ICON_RESTRICT_RENDER_OFF = "RESTRICT_RENDER_OFF"
ICON_RESTRICT_RENDER_ON = "RESTRICT_RENDER_ON"
ICON_PROJECT = 'FILE_BLEND'
ICON_JOB = 'FILE_VOLUME'
ICON_BLEND_FILE = 'BLEND_FILE'
ICON_ERROR = 'ERROR'
ICON_CONSOLE = 'CONSOLE'
ICON_DISCLOSURE_TRI_DOWN = 'DISCLOSURE_TRI_DOWN'
ICON_DISCLOSURE_TRI_RIGHT = 'DISCLOSURE_TRI_RIGHT'
ICON_HELP = 'HELP'
ICON_PREFERENCES = 'PREFERENCES'
ICON_URL = 'URL'


# register module
def register():
    pass


# unregister module
def unregister():
    pass
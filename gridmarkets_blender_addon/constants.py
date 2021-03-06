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

"""
Constants used throughout the add-on

Stored in one central file to prevent circular dependencies
"""

# the add-ons package name
ADDON_PACKAGE_NAME = "gridmarkets_blender_addon"

# The name of the company
COMPANY_NAME = "GridMarkets"

# the name to search for in blenders add-on list
ADDON_NAME = COMPANY_NAME + " Blender Add-on"

# the icons folder contains custom icons for the UI
ICONS_FOLDER = "icons"

# the name of the gridmarkets logo file
GM_COLOURED_LOGO = "logo.png"
GM_GREYSCALE_LOGO = "logo_greyscale.png"

GRIDMARKETS_LOGO_ID = "gridmarkets_logo"
MAIN_COLLECTION_ID = "main"

MOE_LOGO_ID = "moe_logo"
MOE_LOGO = "moe_logo.png"

VRAY_LOGO_ID = "vray_logo"
VRAY_LOGO = "vray_logo.png"

UPLOAD_PROJECT_ICON = "upload_project_icon.png"
UPLOAD_PROJECT_ICON_ID = "upload_project_icon"

UPLOAD_ICON = "upload_icon.png"
UPLOAD_ICON_ID = "upload_icon"

USER_ICON = "user_icon.png"
USER_ICON_ID = "user_icon.png"

PACK_ICON = "pack_icon.png"
PACK_ICON_ID = "pack_icon"

CUSTOM_SPINNER_ICON_0 = "spinner_0.png"
CUSTOM_SPINNER_ICON_1 = "spinner_1.png"
CUSTOM_SPINNER_ICON_2 = "spinner_2.png"
CUSTOM_SPINNER_ICON_3 = "spinner_3.png"
CUSTOM_SPINNER_ICON_4 = "spinner_4.png"
CUSTOM_SPINNER_ICON_5 = "spinner_5.png"
CUSTOM_SPINNER_ICON_6 = "spinner_6.png"
CUSTOM_SPINNER_ICON_7 = "spinner_7.png"
CUSTOM_SPINNER_ICON_0_ID = "SPINNER_0"
CUSTOM_SPINNER_ICON_1_ID = "SPINNER_1"
CUSTOM_SPINNER_ICON_2_ID = "SPINNER_2"
CUSTOM_SPINNER_ICON_3_ID = "SPINNER_3"
CUSTOM_SPINNER_ICON_4_ID = "SPINNER_4"
CUSTOM_SPINNER_ICON_5_ID = "SPINNER_5"
CUSTOM_SPINNER_ICON_6_ID = "SPINNER_6"
CUSTOM_SPINNER_ICON_7_ID = "SPINNER_7"

# directory for the add-on to output temporary files
TEMP_FILES_FOLDER = ".gm_temp_files"

BLEND_FILE_EXTENSION = ".blend"
VRAY_SCENE_FILE_EXTENSION = '.vrscene'

# the url of the render manager
REGISTER_ACCOUNT_LINK = "https://www.gridmarkets.com/sign-up"

RENDER_MANAGER_URL = "https://portal.gridmarkets.com"

COST_CALCULATOR_URL = "https://www.gridmarkets.com/calculator"

FAQ_URL = "https://www.gridmarkets.com/faq"

HELP_URL = "https://www.gridmarkets.com/blender"

SECURITY_URL = "https://www.gridmarkets.com/security"

GRIDMARKETS_WEBSITE_URL = "https://www.gridmarkets.com/"

GITHUB_REPO = "https://github.com/Gridmarkets/gm-blender-addon"
LICENCE_URL = "https://github.com/Gridmarkets/gm-blender-addon/blob/master/LICENCE"
RELEASE_NOTES_URL = "https://github.com/Gridmarkets/gm-blender-addon/releases"

ENVOY_URL = "https://www.gridmarkets.com/envoy"
ENVOY_LOGS_URL = "http://localhost:8090/logs"

SUPPORT_EMAIL = "support@gridmarkets.com"

# relative paths in blender start with a double /
DEFAULT_OUTPUT_PATH = "//gm_results\\"
DEFAULT_JOB_PRESET_NAME = "Use Blender's current Settings"
DEFAULT_WINDOW_WIDTH = 1000
DEFAULT_WINDOW_HIEGHT = 550

BLENDER_TEMP_DIRECTORY = '/tmp\\'

PROJECT_PREFIX = 'Project_'
JOB_PREFIX = 'Job_'
REMOTE_SOURCE_SUFFIX = "_remote"

AUTHENTICATION_HELP_MESSAGE = "\nEnter your " + COMPANY_NAME + " credentials by going to: Edit -> Preferences -> " \
                              "Add-ons -> " + ADDON_NAME + " -> preferences"

TEMPORARY_FILES_DELETED = "Temporary Files Deleted"

FRAME_RANGE_PREFIX = 'range_'
DEFAULT_FRAME_RANGE_START_VALUE = 1
DEFAULT_FRAME_RANGE_END_VALUE = 255
DEFAULT_FRAME_RANGE_STEP_VALUE = 1

INJECTED_SCREEN_NAME = "GRIDMARKETS_INJECTION_SCREEN"
PANEL_REGION_TYPE = "WINDOW"
WINDOW_SPACE_TYPE = "PREFERENCES"

PROJECT_ATTRIBUTE_SPLIT_FACTOR = 0.2

SHOW_ALL_JOB_DEFINITIONS = "show_all_job_definitions"

# operators
OPERATOR_ADD_REMOTE_PROJECT_ID_NAME = "gridmarkets.add_remote_project"
OPERATOR_ADD_REMOTE_PROJECT_LABEL = "Manually specify details for existing Remote Project"
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
OPERATOR_UPLOAD_PROJECT_LABEL = "Upload Current Scene"
OPERATOR_PACK_CURRENT_SCENE_ID_NAME = "gridmarkets.pack_current_scene"
OPERATOR_PACK_CURRENT_SCENE_LABEL = "Pack Current Scene"
OPERATOR_PACK_CURRENT_SCENE_DESCRIPTION = "Save the current scene to a local folder and then package all external assets into the project"
OPERATOR_PACK_BLEND_FILE_ID_NAME = "gridmarkets.pack_blend_file"
OPERATOR_PACK_BLEND_FILE_LABEL = "Pack External Project"
OPERATOR_PACK_BLEND_FILE_DESCRIPTION = "Package a provided .blend file to a local folder"
OPERATOR_UPLOAD_PACKED_PROJECT_ID_NAME = "gridmarkets.upload_packed_project"
OPERATOR_UPLOAD_PACKED_PROJECT_LABEL = "Upload Packed Project"
OPERATOR_UPLOAD_PACKED_PROJECT_DESCRIPTION = "Uploads a project which has already had it's external assets packed into one folder"
OPERATOR_UPLOAD_FILE_AS_PROJECT_ID_NAME = "gridmarkets.upload_file_as_project"
OPERATOR_UPLOAD_FILE_AS_PROJECT_LABEL = "Upload External Project"
OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME = "gridmarkets.frame_range_list_actions"
OPERATOR_FRAME_RANGE_LIST_ACTIONS_LABEL = "Frame Range List Actions"
OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME = "gridmarkets.vray_frame_range_list_actions"
OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_LABEL = "Frame Range List Actions"
OPERATOR_EDIT_FRAME_RANGE_ID_NAME = "gridmarkets.edit_frame_range"
OPERATOR_EDIT_FRAME_RANGE_LABEL = "Edit Frame Range"
OPERATOR_EDIT_VRAY_FRAME_RANGE_ID_NAME = "gridmarkets.edit_vray_frame_range"
OPERATOR_EDIT_VRAY_FRAME_RANGE_LABEL = "Edit Frame Range"
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
OPERATOR_TOGGLE_OUTPUT_PREFIX_VIEW_ID_NAME = "gridmarkets.toggle_output_prefix_view"
OPERATOR_TOGGLE_OUTPUT_PREFIX_VIEW_LABEL = "Toggle output prefix view"
OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_ID_NAME = "gridmarkets.toggle_render_engine_view"
OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_LABEL = "Toggle render engine view"
OPERATOR_OPEN_PREFERENCES_ID_NAME = "gridmarkets.open_preferences"
OPERATOR_OPEN_PREFERENCES_LABEL = "Open " + COMPANY_NAME + " add-on preferences"
OPERATOR_OPEN_REGISTER_ACCOUNT_LINK_ID_NAME = "gridmarkets.open_register_account_link"
OPERATOR_OPEN_REGISTER_ACCOUNT_LINK_LABEL = "Register"
OPERATOR_OPEN_REPOSITORY_ID_NAME = "gridmarkets.open_github_repo"
OPERATOR_OPEN_REPOSITORY_LABEL = "Open GitHub repository"
OPERATOR_OPEN_ADDON_ID_NAME = "gridmarkets.open_addon"
OPERATOR_OPEN_ADDON_LABEL = "Open " + COMPANY_NAME + " add-on"
OPERATOR_COPY_TEMPORARY_FILE_LOCATION_ID_NAME = "gridmarkets.delete_temporary_project_files"
OPERATOR_COPY_TEMPORARY_FILE_LOCATION_LABEL = "Delete temporary project files"
OPERATOR_COPY_SUPPORT_EMAIL_ID_NAME = "gridmarkets.copy_support_email"
OPERATOR_COPY_SUPPORT_EMAIL_LABEL = "Support"
OPERATOR_GET_SELECTED_PROJECT_STATUS_ID_NAME = "gridmarkets.get_selected_project_status"
OPERATOR_GET_SELECTED_PROJECT_STATUS_LABEL = "Get selected project status"
OPERATOR_NULL_ID_NAME = "gridmarkets.null_operator"
OPERATOR_NULL_LABEL = ""

RENDER_DEVICE_GPU = "GPU"
RENDER_DEVICE_CPU = "CPU"

# enum values
PROJECT_OPTIONS_STATIC_COUNT = 1
PROJECT_OPTIONS_NEW_PROJECT_VALUE = 'NEW_PROJECT'
PROJECT_OPTIONS_NEW_PROJECT_LABEL = 'Submit Scene as New Project'
PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION = 'Upload the current scene as a new project to ' + COMPANY_NAME

JOB_OPTIONS_STATIC_COUNT = 1
JOB_OPTIONS_BLENDERS_SETTINGS_VALUE = "BLENDER_JOB_SETTINGS"
JOB_OPTIONS_BLENDERS_SETTINGS_LABEL = "Use Blender's Render Settings"
JOB_OPTIONS_BLENDERS_SETTINGS_DESCRIPTION = "Use Blender's render settings when determining the job options."

# API constants
JOB_PRODUCT_TYPE = "blender"
JOB_OPERATION = "render"

# render engine constants
RENDER_ENGINE_CYCLES = "CYCLES"
RENDER_ENGINE_EEVEE = "BLENDER_EEVEE"
RENDER_ENGINE_BLENDER_INTERNAL = "BLENDER_RENDER"
RENDER_ENGINE_BLENDER_WORKBENCH = "BLENDER_WORKBENCH"
RENDER_ENGINE_VRAY_RT = "VRAY_RENDER_RT"

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
ICON_REMOTE_PROJECT = 'FILE_VOLUME'
ICON_JOB = 'FILE_VOLUME'
ICON_JOB_PRESET = 'PRESET'
ICON_NEW_JOB_PRESET = 'PRESET_NEW'
ICON_BLEND_FILE = 'BLEND_FILE'
ICON_BLENDER = 'BLENDER'
ICON_ERROR = 'ERROR'
ICON_CONSOLE = 'CONSOLE'
ICON_DISCLOSURE_TRI_DOWN = 'DISCLOSURE_TRI_DOWN'
ICON_DISCLOSURE_TRI_RIGHT = 'DISCLOSURE_TRI_RIGHT'
ICON_HELP = 'HELP'
ICON_PREFERENCES = 'PREFERENCES'
ICON_URL = 'URL'
ICON_INFO = 'QUESTION'
ICON_LOCKED = 'LOCKED'
ICON_UNLOCKED = 'UNLOCKED'
ICON_DEFAULT_USER = 'SOLO_ON'
ICON_NON_DEFAULT_USER = 'SOLO_OFF'
ICON_COLLAPSEMENU = 'COLLAPSEMENU'
ICON_CHECKBOX = 'CHECKBOX_DEHLT'
ICON_CHECKBOX_SELECTED = 'CHECKBOX_HLT'
ICON_RADIOBUT_OFF = 'RADIOBUT_OFF'
ICON_RADIOBUT_ON = 'RADIOBUT_ON'
ICON_COPY_TO_CLIPBOARD = 'COPYDOWN'
ICON_SAVE_TO_FILE = 'FILE_NEW'
ICON_RELOAD = "FILE_REFRESH"
ICON_TRASH = 'TRASH'
ICON_EDIT = "MODIFIER_ON"
ICON_FILE_FOLDER = 'FILE_FOLDER'
ICON_VIEWZOOM = 'VIEWZOOM'
ICON_HIDE_OFF = 'HIDE_OFF'
ICON_MONKEY = 'MONKEY'
ICON_NONE = 'NONE'
ICON_BLANK = 'BLANK1'  # blank takes up space where as NONE does not

# layout enum values
REMOTE_PROJECTS_LAYOUT_VALUE = 'projects'
REMOTE_PROJECTS_LAYOUT_LABEL = 'Projects'
REMOTE_PROJECTS_LAYOUT_DESCRIPTION = 'View your projects in the projects view.'
REMOTE_PROJECTS_LAYOUT_ICON = ''
REMOTE_PROJECTS_LAYOUT_ID = 0
REMOTE_PROJECTS_LAYOUT_TUPLE = (REMOTE_PROJECTS_LAYOUT_VALUE,
                                REMOTE_PROJECTS_LAYOUT_LABEL,
                                REMOTE_PROJECTS_LAYOUT_DESCRIPTION,
                                REMOTE_PROJECTS_LAYOUT_ICON,
                                REMOTE_PROJECTS_LAYOUT_ID)

JOB_PRESETS_LAYOUT_VALUE = 'job_presets'
JOB_PRESETS_LAYOUT_LABEL = 'Job Presets'
JOB_PRESETS_LAYOUT_DESCRIPTION = 'View your job presets.'
JOB_PRESETS_LAYOUT_ICON = ''
JOB_PRESETS_LAYOUT_ID = 1
JOB_PRESETS_LAYOUT_TUPLE = (JOB_PRESETS_LAYOUT_VALUE,
                            JOB_PRESETS_LAYOUT_LABEL,
                            JOB_PRESETS_LAYOUT_DESCRIPTION,
                            JOB_PRESETS_LAYOUT_ICON,
                            JOB_PRESETS_LAYOUT_ID)

UPLOAD_CURRENT_SCENE_VALUE = OPERATOR_UPLOAD_PROJECT_ID_NAME
UPLOAD_CURRENT_SCENE_LABEL = OPERATOR_UPLOAD_PROJECT_LABEL
UPLOAD_CURRENT_SCENE_DESCRIPTION = 'Packs your current scene to a temporary directory and uploads it as a new project to ' + COMPANY_NAME
UPLOAD_CURRENT_SCENE_TUPLE = (UPLOAD_CURRENT_SCENE_VALUE,
                              UPLOAD_CURRENT_SCENE_LABEL,
                              UPLOAD_CURRENT_SCENE_DESCRIPTION,
                              ICON_PROJECT,
                              2)

PACK_CURRENT_SCENE_TUPLE = (OPERATOR_PACK_CURRENT_SCENE_ID_NAME,
                            OPERATOR_PACK_CURRENT_SCENE_LABEL,
                            OPERATOR_PACK_CURRENT_SCENE_DESCRIPTION,
                            ICON_PROJECT,
                            3)

PACK_BLEND_FILE_TUPLE = (OPERATOR_PACK_BLEND_FILE_ID_NAME,
                         OPERATOR_PACK_BLEND_FILE_LABEL,
                         OPERATOR_PACK_BLEND_FILE_DESCRIPTION,
                         ICON_PROJECT,
                         4)

UPLOAD_PACKED_PROJECT_TUPLE = (OPERATOR_UPLOAD_PACKED_PROJECT_ID_NAME,
                               OPERATOR_UPLOAD_PACKED_PROJECT_LABEL,
                               OPERATOR_UPLOAD_PACKED_PROJECT_DESCRIPTION,
                               ICON_PROJECT,
                               5)

UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_VALUE = OPERATOR_ADD_REMOTE_PROJECT_ID_NAME
UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_LABEL = OPERATOR_ADD_REMOTE_PROJECT_LABEL
UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_DESCRIPTION = 'Manually specify the details of a project that has already been uploaded to ' + COMPANY_NAME
UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_TUPLE = (UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_VALUE,
                                               UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_LABEL,
                                               UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_DESCRIPTION,
                                               ICON_VIEWZOOM,
                                               6)

SUBMISSION_SETTINGS_VALUE = 'submission_settings'
SUBMISSION_SETTINGS_LABEL = 'Submission Settings'
SUBMISSION_SETTINGS_DESCRIPTION = 'Submit a job to ' + COMPANY_NAME
SUBMISSION_SETTINGS_ICON = ''
SUBMISSION_SETTINGS_ID = 7
SUBMISSION_SETTINGS_TUPLE = (SUBMISSION_SETTINGS_VALUE,
                             SUBMISSION_SETTINGS_LABEL,
                             SUBMISSION_SETTINGS_DESCRIPTION,
                             SUBMISSION_SETTINGS_ICON,
                             SUBMISSION_SETTINGS_ID)

LAYOUTS = (
    SUBMISSION_SETTINGS_TUPLE,
    JOB_PRESETS_LAYOUT_TUPLE,
    REMOTE_PROJECTS_LAYOUT_TUPLE,
    UPLOAD_CURRENT_SCENE_TUPLE,
    UPLOAD_PACKED_PROJECT_TUPLE,
    PACK_CURRENT_SCENE_TUPLE,
    PACK_BLEND_FILE_TUPLE,
    UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_TUPLE
)

PROJECT_STATUS_POLLING_ENABLED = False

VRAY_RENDER_RT = "VRAY_RENDER_RT"

PROJECT_ATTRIBUTES_POINTER_KEY = "project_attributes"

INSTANCES_SUBTYPE_PROPERTY_USE_DEFAULT = "_default"

# register module
def register():
    pass


# unregister module
def unregister():
    pass

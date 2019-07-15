bl_info = {
    "name": "Gridmarkets Blender Add-on",
    "description": "Allows users to submit Blender jobs to the Gridmarkets render farm from within Blender.",
    "author": "GridMarkets",
    "version": (0, 5, 0),
    "blender": (2, 80, 0),
    "location": "Info > Header",
    "warning": "", # used for warning icon and text in add-ons panel
    "wiki_url": "https://www.gridmarkets.com/blender",
    "category": "Render"
}

import os
import sys
import importlib

# list of modules to import
modulesNames = ['constants',
                'icon_loader',
                'property_groups.main_props',
                'addon_preferences',
                'blender_logging_wrapper',
                'operators.trace_project',
                'operators.submit',
                'operators.open_manager_portal',
                'operators.open_cost_calculator',
                'operators.open_help_url',
                'operators.project_list_actions',
                'operators.job_list_actions',
                'operators.upload_project',
                'operators.frame_range_list_actions',
                'operators.edit_frame_range',
                'operators.copy_logs_to_clipboard',
                'operators.open_preferences',
                'operators.open_addon',
                'operators.toggle_submission_summary',
                'operators.toggle_frame_ranges_view',
                'operators.toggle_output_format_view',
                'operators.toggle_output_path_view',
                'operators.toggle_render_engine_view',
                'operators.copy_temporary_file_location',
                'operators.get_selected_project_status',
                'gridmarkets_blender_addon',
                'list_items.frame_range',
                'list_items.job',
                'list_items.log',
                'list_items.project',
                'panels.main',
                'panels.projects',
                'panels.jobs',
                'panels.output_settings',
                'panels.console',
                'panels.preferences',
                'panel_injections']

# We pre-append so that these paths take precedence over blenders packed modules which can be different versions
# pre-append this folder to sys.path so local dependencies can be found
sys.path.insert(0, os.path.dirname(__file__))

# pre-append the lib folder to sys.path so local dependencies can be found
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

for path in sys.path:
    print(path)

# create a dictionary to hold the full names of modules
modulesFullNames = {}

# record module names differently depending on if Debug mode is active
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

# iterate through modules and attempt to load the module 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

# register modules
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
# unregister modules
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()
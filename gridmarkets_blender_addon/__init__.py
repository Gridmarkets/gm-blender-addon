bl_info = {
    "name": "Gridmarkets Blender Add-on",
    "description": "Allows users to submit Blender jobs to the Gridmarkets render farm from within Blender.",
    "author": "GridMarkets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
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
                'utils_blender',
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
                'operators.upload_file_as_project',
                'operators.frame_range_list_actions',
                'operators.edit_frame_range',
                'operators.copy_logs_to_clipboard',
                'operators.open_preferences',
                'operators.open_addon',
                'operators.save_logs_to_file',
                'operators.toggle_submission_summary',
                'operators.toggle_frame_ranges_view',
                'operators.toggle_output_format_view',
                'operators.toggle_output_path_view',
                'operators.toggle_output_prefix_view',
                'operators.toggle_render_engine_view',
                'operators.copy_temporary_file_location',
                'operators.get_selected_project_status',
                'list_items.frame_range',
                'list_items.job',
                'list_items.log',
                'list_items.project',
                'layouts.console',
                'layouts.empty',
                'layouts.header',
                'layouts.jobs',
                'layouts.preferences',
                'layouts.projects',
                'layouts.sidebar',
                'layouts.submission_settings',
                'layouts.body',
                'panel_overloaders.panel_overloader',
                'panel_overloaders.addons',
                'panel_overloaders.header',
                'panel_overloaders.tabs',
                'blender_plugin']

# pre-append the lib folder to sys.path so local dependencies can be found. Pre-append so that these paths take
# precedence over blender's existing packed modules which can be different versions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# create a dictionary to hold the full names of modules
modulesFullNames = {}

# Iterate though all the module names
for currentModuleName in modulesNames:
    # And add the module's full name to modulesFullNames
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

# iterate through modules and attempt to load the module 
for currentModuleFullName in modulesFullNames.values():

    # sys.modules is a dictionary that maps module names to modules which have been loaded. This can be manipulated to
    # force reloading of specific modules (as well as other tricks)
    # Checking if the currentModuleFullName can be found in the sys.modules dictionary
    if currentModuleFullName in sys.modules:

        # importlib is package that defines pythons import function. When an import statement is written it is using
        # importlib.__import__() under the hood, it is just another way to do the same thing. Here importlib.reload is
        # used to reloads a previously imported module. We do this so that if the modules source code has been changed
        # in an external editor Python wont use the old version if it has already been imported.
        importlib.reload(sys.modules[currentModuleFullName])

    else:
        # This imports the module and makes it global. Calling globals() will return a dictionary of all the global
        # symbols (methods, variables, etc..). By doing globals()[currentModuleFullName] we add an entry in to global
        # symbol table for each module.
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


# register modules
def register():
    for name in modulesFullNames.values():
        if name in sys.modules:
            if hasattr(sys.modules[name], 'register'):
                sys.modules[name].register()


# unregister modules
def unregister():
    for name in modulesFullNames.values():
        if name in sys.modules:
            if hasattr(sys.modules[name], 'unregister'):
                sys.modules[name].unregister()


if __name__ == "__main__":
    register()

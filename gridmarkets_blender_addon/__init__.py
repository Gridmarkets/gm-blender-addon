bl_info = {
    "name": "Gridmarkets Blender Add-on",
    "description": "Allows users to submit Blender jobs to the Gridmarkets render farm from within Blender.",
    "author": "Oliver Dawes",
    "version": (0, 3, 2),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in add-ons panel
    "wiki_url": "https://www.gridmarkets.com/",
    "tracker_url": "",
    "category": "Render"
}

import os
import sys
import importlib

# list of modules to import
modulesNames = ['constants',
                'icon_loader',
                'properties',
                'property_sanitizer',
                'addon_preferences',
                'operators.trace_project',
                'operators.submit',
                'gridmarkets_blender_addon',
                'panels.main',
                'panels.projects',
                'panels.jobs',
                #'panels.job_info',
                'panels.frame_ranges',
                'panels.output_settings']

# append this folder to sys.path so local dependencies can be found
sys.path.append(os.path.dirname(__file__))

# append the lib folder to sys.path so local dependencies can be found
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

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
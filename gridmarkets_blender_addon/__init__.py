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

bl_info = {
    "name": "GridMarkets Blender Add-on",
    "description": "Allows users to submit Blender jobs to the GridMarkets render farm from within Blender.",
    "author": "GridMarkets",
    "version": (1, 4, 3),
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
modulesNames = ['meta_plugin.scene_exporter',
                'file_packers.blender_file_packer',
                'scene_exporters.blender_scene_exporter',
                'scene_exporters.vray_scene_exporter',
                'constants',
                #'blender_plugin.plugin_fetcher.plugin_fetcher', # don't reload otherwise state is lost on add-on reload
                'utils_blender',
                'icon_loader',
                'property_groups.main_props',
                'addon_preferences',
                'blender_plugin.remote_project_container.operators.add_remote_project',
                'operators.trace_project',
                'operators.submit',
                'operators.open_manager_portal',
                'operators.open_cost_calculator',
                'operators.open_envoy_url',
                'operators.open_help_url',
                'operators.project_list_actions',
                'operators.job_list_actions',
                'menus',
                'blender_plugin.remote_project_container.operators.upload_project',
                'blender_plugin.remote_project_container.operators.upload_packed_project',
                'blender_plugin.remote_project_container.operators.pack_current_scene',
                'blender_plugin.remote_project_container.operators.pack_blend_file',
                'blender_plugin.remote_project_container.operators.refresh_project_list',
                'blender_plugin.remote_project_container.operators.refresh_project_file_list',
                'operators.frame_range_list_actions',
                'operators.edit_frame_range',
                'operators.open_preferences',
                'operators.open_register_account_link',
                'operators.open_repository',
                'operators.open_addon',
                'operators.toggle_submission_summary',
                'operators.toggle_frame_ranges_view',
                'operators.toggle_output_format_view',
                'operators.toggle_output_path_view',
                'operators.toggle_output_prefix_view',
                'operators.toggle_render_engine_view',
                'operators.copy_support_email',
                'operators.copy_temporary_file_location',
                'operators.get_selected_project_status',
                'operators.test_operator',
                'operators.null_operator',
                'operators.set_ui_layout',
                'list_items.frame_range',
                'list_items.job',
                'list_items.project',
                'blender_plugin.attribute.layouts.draw_attribute_input',
                'blender_plugin.remote_project.list_items.remote_project_list',
                'blender_plugin.job_attribute.operators.set_inference_source',
                'blender_plugin.job_preset_attribute.layouts.draw_job_preset_attribute',
                'blender_plugin.job_preset.layouts.draw_job_preset',
                'blender_plugin.job_preset.list_items.job_preset_list',
                'blender_plugin.job_preset.operators.open_job_preset_definition_popup',
                'blender_plugin.job_preset_container.layouts.draw_job_preset_container',
                'blender_plugin.job_preset_container.menus.create_new_job_preset',
                'blender_plugin.job_preset_container.operators.create_new_job_preset',
                'blender_plugin.job_preset_container.operators.remove_focused_job_preset',
                'blender_plugin.job_preset_container.operators.toggle_job_preset_locked_state',
                'blender_plugin.job_preset_container.operators.set_focused_job_preset',
                'blender_plugin.log_item.list_items.log_item_list',
                'blender_plugin.log_history_container.layouts.draw_logging_console',
                'blender_plugin.log_history_container.menus.display_options',
                'blender_plugin.log_history_container.operators.toggle_logging_console',
                'blender_plugin.logging_coordinator.operators.clear_logs',
                'blender_plugin.logging_coordinator.operators.copy_logs_to_clipboard',
                'blender_plugin.logging_coordinator.operators.save_logs_to_file',
                'blender_plugin.remote_project.operators.open_remote_project_definition_popup',
                'blender_plugin.remote_project.layouts.draw_remote_project',
                'blender_plugin.remote_project_container.layouts.draw_remote_project_container',
                'blender_plugin.user.list_items.user_list',
                'blender_plugin.user_container.layouts',
                'blender_plugin.user_container.operators.delete_focused_profile',
                'blender_plugin.user_container.operators.load_focused_profile',
                'blender_plugin.user_container.operators.set_focused_profile_as_default',
                'blender_plugin.user_container.operators.show_user_credits',
                'blender_plugin.user_container.operators.sign_in',
                'blender_plugin.user_container.operators.sign_out',
                'blender_plugin.user_container.operators.switch_user',
                'blender_plugin.user_interface.operators.toggle_show_log_dates',
                'blender_plugin.user_interface.operators.toggle_show_log_times',
                'blender_plugin.user_interface.operators.toggle_show_logger_names',
                'blender_plugin.plugin.plugin',
                'layouts.empty',
                'layouts.header',
                'layouts.preferences',
                'layouts.sidebar',
                'layouts.submission_settings',
                'layouts.body',
                'layouts.top_bar',
                'panel_overloaders.panel_overloader',
                'panel_overloaders.addons',
                'panel_overloaders.header',
                'panel_overloaders.navigation_bar',
                'panel_overloaders.save_preferences',
                'gui_entry_point']

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

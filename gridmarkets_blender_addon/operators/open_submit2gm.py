# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2021  GridMarkets
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


import bpy

import importlib
import os
import sys

from gridmarkets_blender_addon import constants, config


def evaluate_code(code, return_variables):

    # Execute the provided code
    try:
        exec(code)
    except Exception as e:
        print("exception:", e)
        raise e

    results = {}

    for variable in return_variables:
        results[variable] = eval(variable)

    return results


class GRIDMARKETS_OT_open_submit2gm(bpy.types.Operator):
    """ Opens the GridMarkets Submit2gm app."""

    bl_idname = constants.OPERATOR_OPEN_SUBMIT2GM_ID_NAME
    bl_label = constants.OPERATOR_OPEN_SUBMIT2GM_LABEL
    bl_options = {'REGISTER'}

    def import_submit2gm(self):
        # Read config file to find submit2gm install location
        submit2gm_path = config.SUBMIT2GM_PATH

        # Get the location of the submit2gm python package
        submit2gm_package_path = os.path.join(os.path.dirname(submit2gm_path), 'submit2gm')

        # Import the submit2gm package
        submit2gm_init_path = os.path.join(submit2gm_package_path, "__init__.py")

        spec = importlib.util.spec_from_file_location('submit2gm', submit2gm_init_path)
        module = importlib.util.module_from_spec(spec)

        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

    def execute(self, context):
        self.import_submit2gm()

        from submit2gm.command_port_server_utils import start_command_port_server
        envoy_python_path = config.ENVOY_PYTHON_PATH
        logger_name = 'gridmarkets_blender_addon'
        product = 'blender'
        meta_info = ''
        evaluate_code_cb = evaluate_code
        debug_mode = True

        start_command_port_server(envoy_python_path, logger_name, product, meta_info, evaluate_code_cb, debug_mode)

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_submit2gm,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

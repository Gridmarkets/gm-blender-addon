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

import bpy

import pathlib

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject

from gridmarkets_blender_addon.meta_plugin.errors import *


class GRIDMARKETS_OT_upload_packed_project(BaseOperator):
    bl_idname = constants.OPERATOR_UPLOAD_PACKED_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PACKED_PROJECT_LABEL
    bl_description = constants.OPERATOR_UPLOAD_PACKED_PROJECT_DESCRIPTION
    bl_options = {'REGISTER'}

    def handle_expected_result(self, result: any) -> bool:

        if isinstance(result, RemoteProject):
            return True

        elif type(result) == NotSignedInError:
            msg = "Could not upload your current scene. You are not signed in."
            self.report_and_log({'ERROR'}, msg)
            return True

        elif type(result) == APIClientError:
            msg = "Could not upload your current scene. " + result.user_message
            self.report_and_log({'ERROR'}, msg)
            return True

        return False

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.setup_operator()

        plugin = self.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_cached_api_schema()

        # get project name
        project_name_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)
        project_name = project_name_attribute.get_value()

        # ask for confirmation if uploading to existing project
        root_directories = api_client.get_root_directories(ignore_cache=True)
        if project_name in root_directories:
            return context.window_manager.invoke_props_dialog(self, width=500)

        return self.execute(context)

    def execute(self, context: bpy.types.Context):
        plugin = self.get_plugin()
        logger = self.get_logger()

        user_interface = plugin.get_user_interface()

        # validate that the project attributes make up a valid project
        try:
            # do not force transition as all inputs should be valid
            attributes = utils_blender.get_project_attributes()
        except RejectedTransitionInputError as e:
            # if a transition failed then one of the attributes is invalid
            self.report_and_log({'ERROR'}, e.user_message)
            return {"FINISHED"}

        # validate that the selected root directory exists
        root_dir = pathlib.Path(user_interface.get_root_directory())
        if not root_dir.exists():
            self.report_and_log({'ERROR_INVALID_INPUT'}, "Root Directory does not exist.")
            return {"FINISHED"}

        # collect the files included in the packed project
        upload_everything = user_interface.get_upload_all_files_in_root()
        project_files = set(utils_blender.get_project_files([]))

        # check that all the files are under the root directory
        for file in project_files:

            # make the file path absolute / resolve symlinks
            file.resolve()

            if root_dir not in file.parents:
                self.report_and_log({'ERROR_INVALID_INPUT'}, "Project file \"" + str(file) +
                                    "\" is outside of the root directory.")
                return {"FINISHED"}

        packed_project = PackedProject(attributes[api_constants.API_KEYS.PROJECT_NAME],
                                       root_dir,
                                       project_files,
                                       attributes)

        logger.info("Uploading packed project...")

        ################################################################################################################

        method = plugin.get_api_client().upload_project

        args = (
            packed_project,
            upload_everything
        )

        kwargs = {
            "delete_local_files_after_upload": False,
        }

        running_operation_message = "Uploading packed project..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)


    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.separator()
        layout.label(text="A remote project already exists with this name. Existing files will be overwritten.",
                     icon=constants.ICON_ERROR)
        layout.separator()
        layout.label(text="Press ok to continue.")


classes = (
    GRIDMARKETS_OT_upload_packed_project,
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

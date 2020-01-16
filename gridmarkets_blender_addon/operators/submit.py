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

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon import constants, utils
from gridmarkets_blender_addon.meta_plugin.errors import *

from gridmarkets_blender_addon.blender_plugin.remote_project import RemoteProject


class GRIDMARKETS_OT_Submit(BaseOperator):
    """Class to represent the 'Submit' operation."""

    bl_idname = constants.OPERATOR_SUBMIT_ID_NAME
    bl_label = constants.OPERATOR_SUBMIT_LABEL

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
        default="",
        maxlen=256
    )

    def handle_expected_result(self, result: any) -> bool:
        if type(result) == NotSignedInError:
            self.report_and_log({'ERROR'}, result.user_message)
            return True

        elif type(result) == FilePackingError:
            msg = "Could not finish packing your project. " + result.user_message
            self.report_and_log({'ERROR'}, msg)
            return True

        elif type(result) == NotSignedInError:
            msg = "Could not upload your current scene. You are not signed in."
            self.report_and_log({'ERROR'}, msg)
            return True

        elif type(result) == APIClientError:
            self.report_and_log({'ERROR'}, result.user_message)
            return True

        elif type(result) == RemoteProject: # a remote project is returned when submitting a new project
            self.get_plugin().get_remote_project_container().append(result)
            return True

        elif result is None: # None is returned when submitting to an existing project
            return True

        return False

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        props = context.scene.props
        remote_projects = props.remote_project_container.remote_projects

        # only show project name pop up dialog if submitting a new project
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            # if the file has been saved use the name of the file as the prefix
            if bpy.context.blend_data.is_saved:
                blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)

                if blend_file_name.endswith(constants.BLEND_FILE_EXTENSION):
                    blend_file_name = blend_file_name[:-len(constants.BLEND_FILE_EXTENSION)] + "_"

                self.project_name = utils.create_unique_object_name(remote_projects, name_prefix=blend_file_name)
            else:
                self.project_name = utils.create_unique_object_name(remote_projects,
                                                                    name_prefix=constants.PROJECT_PREFIX)

            # create popup
            return context.window_manager.invoke_props_dialog(self, width=400)
        else:
            return self.execute(context)

    def submit_new_project(self, context: bpy.types.Context):
        pass

    def submit_to_existing_project(self, context: bpy.types.Context):
        plugin = self.get_plugin()

        # get the remote project
        props = context.scene.props
        remote_project_container = plugin.get_remote_project_container()
        remote_project = remote_project_container.get_project_with_id(props.project_options)

        # get the job preset
        from gridmarkets_blender_addon.property_groups.main_props import get_selected_job_option
        job_preset = get_selected_job_option(context)

        if job_preset is None:
            self.report_and_log({"ERROR"}, "No Job Preset option selected for submission")

        ################################################################################################################

        method = plugin.get_api_client().submit_to_remote_project

        args = (
            remote_project,
            job_preset
        )

        kwargs = {}

        running_operation_message = "Submitting project..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)

    def execute(self, context: bpy.types.Context):
        self.setup_operator()

        props = context.scene.props

        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            return self.submit_new_project(context)
        else:
            return self.submit_to_existing_project(context)


classes = (
    GRIDMARKETS_OT_Submit,
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

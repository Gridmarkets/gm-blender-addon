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
import typing

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon import constants, utils, utils_blender
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter
from gridmarkets_blender_addon.meta_plugin.errors import *

from gridmarkets_blender_addon.meta_plugin.gridmarkets.remote_project import RemoteProject

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset


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

    root_directories = []

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

        elif type(result) == UnsupportedApplicationError:
            self.report({'ERROR'}, result.user_message)
            return True

        elif type(result) == RemoteProject:  # a remote project is returned when submitting a new project
            self.get_plugin().get_remote_project_container().append(result)
            return True

        elif result is None:  # None is returned when submitting to an existing project
            return True

        return False

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.setup_operator()
        plugin = self.get_plugin()

        props = context.scene.props
        remote_projects = props.remote_project_container.remote_projects

        # only show project name pop up dialog if submitting a new project
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:

            # set root directories
            api_client = plugin.get_api_client()
            self.root_directories = api_client.get_root_directories(ignore_cache=True)

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
            return context.window_manager.invoke_props_dialog(self, width=500)
        else:
            return self.execute(context)

    def _execute_submit_new_project(self,
                                    project_name: str,
                                    product: str,
                                    product_version: str,
                                    attributes: typing.Dict[str, any],
                                    job_preset: 'JobPreset'):
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

        temp_dir = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

        if product == api_constants.PRODUCTS.BLENDER:
            packed_project = BlenderSceneExporter().export(temp_dir)
        elif product == api_constants.PRODUCTS.VRAY:
            packed_project = VRaySceneExporter().export(temp_dir)
        else:
            raise RuntimeError("Unknown project type")

        packed_project.set_name(project_name)
        for key, value in attributes.items():
            # If the key is not already in the packed project's attribute list
            if key not in packed_project.get_attributes():
                # Then set the attribute
                packed_project.set_attribute(key, value)

        api_client = self.get_plugin().get_api_client()
        return api_client.submit_new_project(packed_project, job_preset, delete_local_files_after_upload=False)

    def submit_new_project(self, context: bpy.types.Context):
        plugin = self.get_plugin()
        user_interface = plugin.get_user_interface()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()

        # check render engine
        if not user_interface.is_render_engine_supported():
            return {'FINISHED'}

        # get project name
        project_name_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)
        project_name = project_name_attribute.get_value()

        # set product (either blender or vray)
        product_attribute = api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PRODUCT)
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product = api_constants.PRODUCTS.VRAY
        else:
            product = api_constants.PRODUCTS.BLENDER
        product_attribute.set_value(product)

        # set and get product version
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.VRAY_VERSION)
            product_version_attribute.set_value(api_client.get_product_versions(api_constants.PRODUCTS.VRAY)[0])
        else:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.BLENDER_VERSION)

            # set the product version to the closest matching version of blender supported
            closest_blender_version = utils_blender.get_closest_matching_product_version()
            if closest_blender_version is not None:
                product_version_attribute.set_value(closest_blender_version)
        product_version = product_version_attribute.get_value()

        # set the other attributes to their application inferred value
        app_attribute_source = plugin.get_application_pool_attribute_source()
        app_attribute_source.set_project_attribute_values(project_name, product, product_version)

        attributes = utils_blender.get_project_attributes(force_transition=True)

        # get the job preset
        from gridmarkets_blender_addon.property_groups.main_props import get_selected_job_option
        job_preset = get_selected_job_option(context)

        if job_preset is None:
            self.report_and_log({"ERROR"}, "No Job Preset option selected for submission")

        ################################################################################################################

        method = self._execute_submit_new_project

        args = (
            project_name,
            product,
            product_version,
            attributes,
            job_preset
        )

        kwargs = {}

        running_operation_message = "Submitting project..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)

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
        plugin = self.get_plugin()
        api_schema = plugin.get_api_client().get_api_schema()
        props = context.scene.props

        # set the project name attribute
        project_name_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)

        project_name_attribute.set_value(self.project_name)

        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            return self.submit_new_project(context)
        else:
            return self.submit_to_existing_project(context)

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.prop(self, "project_name")

        if self.project_name in self.root_directories:
            layout.label(text="A remote project already exists with this name. Existing files will be overwritten.", icon=constants.ICON_ERROR)


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

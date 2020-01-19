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
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.blender_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter

from gridmarkets_blender_addon.meta_plugin.errors import *


class GRIDMARKETS_OT_upload_project(BaseOperator):
    bl_idname = constants.OPERATOR_UPLOAD_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PROJECT_LABEL
    bl_description = "Upload the current scene as a new project"
    bl_options = {'REGISTER'}

    def handle_expected_result(self, result: any) -> bool:

        if isinstance(result, RemoteProject):
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
            msg = "Could not upload your current scene. " + result.user_message
            self.report_and_log({'ERROR'}, msg)
            return True

        return False

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.setup_operator()

        plugin = self.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()

        # get project name
        project_name_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)
        project_name = project_name_attribute.get_value()

        root_directories = api_client.get_root_directories(ignore_cache=True)

        if project_name in root_directories:
            return context.window_manager.invoke_props_dialog(self, width=500)

        return self.execute(context)

    def execute(self, context: bpy.types.Context):
        plugin = self.get_plugin()
        user_interface = plugin.get_user_interface()
        api_schema = plugin.get_api_client().get_api_schema()

        # check render engine
        if not user_interface.is_render_engine_supported():
            return {'FINISHED'}

        # get project name
        project_name_attribute = api_schema.get_project_attribute_with_id(
            api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)
        project_name = project_name_attribute.get_value()

        # set and get product (either blender or vray)
        product_attribute = api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PRODUCT)
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product = api_constants.PRODUCTS.VRAY
        else:
            product = api_constants.PRODUCTS.BLENDER
        product_attribute.set_value(product)

        # get product version
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.VRAY_VERSION)
        else:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.BLENDER_VERSION)
        product_version = product_version_attribute.get_value()

        # set the other attributes to their application inferred value
        app_attribute_source = plugin.get_application_pool_attribute_source()
        app_attribute_source.set_project_attribute_values(project_name, product, product_version)

        attributes = utils_blender.get_project_attributes(force_transition=True)

        ################################################################################################################

        method = self._execute

        args = (
            project_name,
            product,
            product_version,
            attributes
        )

        kwargs = {}

        running_operation_message = "Uploading project..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)

    def _execute(self, project_name: str, product: str, product_version: str, attributes: typing.Dict[str, any]):
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
        return api_client.upload_project(packed_project, True, delete_local_files_after_upload=False)

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.separator()
        layout.label(text="A remote project already exists with this name. Existing files will be overwritten.",
                     icon=constants.ICON_ERROR)
        layout.separator()
        layout.label(text="Press ok to continue.")

classes = (
    GRIDMARKETS_OT_upload_project,
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

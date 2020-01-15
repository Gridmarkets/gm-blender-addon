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

from queue import Queue, Empty
import typing
import traceback

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon import constants, utils, utils_blender
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter


class GRIDMARKETS_OT_upload_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_UPLOAD_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PROJECT_LABEL
    bl_description = "Upload the current scene as a new project"
    bl_options = {'REGISTER'}

    bucket = None
    timer = None
    thread: ExcThread = None
    plugin = None

    def modal(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.errors.plugin_error import PluginError
        from gridmarkets_blender_addon.meta_plugin.errors.not_signed_in_error import NotSignedInError
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
        from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject

        if event.type == 'TIMER':
            self.plugin.get_user_interface().increment_running_operation_spinner()
            utils_blender.force_redraw_addon()

            if not self.thread.isAlive():
                try:
                    result = self.bucket.get(block=False)
                except Empty:
                    raise RuntimeError("bucket is Empty")
                else:
                    if type(result) == NotSignedInError:
                        self.report({'ERROR'}, result.user_message)

                    elif type(result) == AuthenticationError:
                        self.report({'ERROR'}, result.user_message)

                    elif type(result) == InsufficientCreditsError:
                        self.report({'ERROR'}, result.user_message)

                    elif type(result) == InvalidRequestError:
                        self.report({'ERROR'}, result.user_message)

                    elif type(result) == APIError:
                        self.report({'ERROR'}, result.user_message)

                    elif isinstance(result, PluginError):
                        self.report({'ERROR'}, result.user_message)

                    elif isinstance(result, Exception):
                        self.report({'ERROR'}, result)
                        traceback.print_tb(result.__traceback__)

                    else:
                        if type(result) != RemoteProject:
                            raise RuntimeError("Method returned unexpected result:", result)

                self.thread.join()
                self.plugin.get_user_interface().set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    @staticmethod
    def boilerplate_execute(operator, context, method, args, kwargs, running_operation_message: str):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        operator.plugin = plugin

        wm = context.window_manager
        operator.bucket = Queue()
        operator.thread = ExcThread(operator.bucket,
                                    method,
                                    args=args,
                                    kwargs=kwargs)
        operator.thread.start()

        operator.timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(operator)

        user_interface = plugin.get_user_interface()
        user_interface.set_is_running_operation_flag(True)
        user_interface.set_running_operation_message(running_operation_message)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.project_attribute.project_attribute import \
            get_project_attribute_value, set_project_attribute_value
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        user_interface = plugin.get_user_interface()
        api_schema = plugin.get_api_client().get_api_schema()

        # check render engine
        if not user_interface.is_render_engine_supported():
            return {'FINISHED'}

        # get project name
        project_name_attribute = api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PROJECT_NAME)
        project_name = get_project_attribute_value(project_name_attribute)

        # set product (either blender or vray)
        product_attribute = api_schema.get_project_attribute_with_id(api_constants.PROJECT_ATTRIBUTE_IDS.PRODUCT)
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product = api_constants.PRODUCTS.VRAY
        else:
            product = api_constants.PRODUCTS.BLENDER
        set_project_attribute_value(product_attribute, product)

        # get product version
        if context.scene.render.engine == constants.RENDER_ENGINE_VRAY_RT:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.VRAY_VERSION)
        else:
            product_version_attribute = api_schema.get_project_attribute_with_id(
                api_constants.PROJECT_ATTRIBUTE_IDS.BLENDER_VERSION)
        product_version = get_project_attribute_value(product_version_attribute)

        # set the other attributes to their application inferred value
        app_attribute_source = plugin.get_application_pool_attribute_source()
        app_attribute_source.set_project_attribute_values(project_name, product, product_version)

        attributes = utils_blender.get_project_attributes(force_transition=True)

        args = (
            project_name,
            product,
            product_version,
            attributes
        )

        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 GRIDMARKETS_OT_upload_project._execute,
                                                                 args,
                                                                 {},
                                                                 "Uploading project...")

    @staticmethod
    def _execute(project_name: str, product: str, product_version: str, attributes: typing.Dict[str, any]):
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

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        api_client = plugin.get_api_client()
        return api_client.upload_project(packed_project, True, delete_local_files_after_upload=False)


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

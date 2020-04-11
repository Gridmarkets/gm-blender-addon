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
from bpy_extras.io_utils import ImportHelper

import pathlib
from queue import Queue, Empty

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon import api_constants, constants, utils, utils_blender
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts.draw_remote_project_summary import \
    draw_remote_project_summary
from gridmarkets_blender_addon.file_packers.blender_file_packer import BlenderFilePacker
from gridmarkets_blender_addon.project.packed_vray_project import PackedVRayProject


class GRIDMARKETS_OT_upload_file_as_project(bpy.types.Operator, ImportHelper):
    bl_idname = constants.OPERATOR_UPLOAD_FILE_AS_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_FILE_AS_PROJECT_LABEL
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    _filter_glob = '*' + constants.BLEND_FILE_EXTENSION + ';*' + constants.VRAY_SCENE_FILE_EXTENSION

    filter_glob = bpy.props.StringProperty(
        default=_filter_glob,
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    project_name = bpy.props.StringProperty(
        name="Project Name",
        default="",
        maxlen=256
    )

    project_type = bpy.props.EnumProperty(
        name="Project Type",
        items=utils_blender.get_supported_products
    )

    blender_280_engine = bpy.props.EnumProperty(
        name="Blender engine",
        items=utils_blender.get_supported_blender_280_engines
    )

    blender_279_engine = bpy.props.EnumProperty(
        name="Blender engine",
        items=utils_blender.get_supported_blender_279_engines
    )

    blender_version = bpy.props.EnumProperty(
        name="Blender version",
        items=utils_blender.get_supported_blender_versions
    )

    vray_version = bpy.props.EnumProperty(
        name="V-Ray version",
        items=utils_blender.get_supported_vray_versions
    )

    remap_file = bpy.props.StringProperty(
        name="Re-map file",
        default="<Generated during upload>",
        description="The name of the remap file"
    )

    use_file_name = bpy.props.BoolProperty(
        name="Use file name as project name",
        description="Use the name of selected the .blend file as the project name.",
        default=True
    )

    bucket = None
    timer = None
    thread = None
    user_interface = None
    remote_project_container = None

    def modal(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.errors.not_signed_in_error import NotSignedInError
        from gridmarkets.errors import AuthenticationError, InsufficientCreditsError, InvalidRequestError, APIError
        from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject

        if event.type == 'TIMER':
            self.user_interface.increment_running_operation_spinner()
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

                    elif type(result) == RemoteProject:
                        self.remote_project_container.append(result)

                    else:
                        raise RuntimeError("Method returned unexpected result:", result)

                self.thread.join()
                self.user_interface.set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        props = context.scene.props
        self.project_name = utils.create_unique_object_name(props.projects, name_prefix=constants.PROJECT_PREFIX)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        self.remote_project_container = plugin.get_remote_project_container()
        self.user_interface = plugin.get_user_interface()

        wm = context.window_manager
        self.bucket = Queue()
        self.thread = ExcThread(self.bucket, self._execute,
                                args=(self.filepath, self.project_type, self.project_name, self.remap_file), kwargs={})
        self.thread.start()

        self.timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        self.user_interface.set_is_running_operation_flag(True)
        self.user_interface.set_running_operation_message("Uploading project...")
        return {'RUNNING_MODAL'}

    @staticmethod
    def _execute(filepath: str, project_type: str, project_name: str, remap_file):
        main_file = pathlib.Path(filepath)

        if project_type == api_constants.PRODUCTS.BLENDER:
            from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager
            packed_project = BlenderFilePacker().pack(main_file,
                                                      TempDirectoryManager.get_temp_directory_manager().get_temp_directory())
            packed_project.set_name(project_name)
        elif project_type == api_constants.PRODUCTS.VRAY:
            remap_file = pathlib.Path(remap_file)
            packed_project = PackedVRayProject(main_file.parent, main_file)
            packed_project.set_name(project_name)
        else:
            raise RuntimeError("Unknown project type")

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        return api_client.upload_project(packed_project)

    def draw(self, context):
        layout = self.layout

        layout.separator()

        layout.prop(self, "use_file_name")

        sub = layout.row()
        sub.prop(self, "project_name")
        sub.enabled = not self.use_file_name

        layout.prop(self, "project_type")

        if self.project_type == api_constants.PRODUCTS.BLENDER:
            layout.prop(self, "blender_version")

            if self.blender_version == api_constants.BLENDER_VERSIONS.V_2_80:
                layout.prop(self, "blender_280_engine")
            elif self.blender_version == api_constants.BLENDER_VERSIONS.V_2_79:
                layout.prop(self, "blender_279_engine")

        elif self.project_type == api_constants.PRODUCTS.VRAY:
            layout.prop(self, "vray_version")

            sub = layout.row()
            sub.enabled = False
            sub.prop(self, "remap_file")

        layout.separator()

        project_file = pathlib.Path(self.filepath)
        project_file_name = project_file.name
        project_name = project_file.stem
        if self.use_file_name:
            self.project_name = project_name

        draw_remote_project_summary(layout, self.project_name, self.project_type,
                                    self.blender_version, project_file_name, self.blender_280_engine,
                                    self.blender_279_engine,
                                    self.vray_version, self.remap_file)


classes = (
    GRIDMARKETS_OT_upload_file_as_project,
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

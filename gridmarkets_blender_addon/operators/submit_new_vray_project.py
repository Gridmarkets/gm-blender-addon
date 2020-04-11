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
from queue import Queue, Empty

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread

from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter
from gridmarkets_blender_addon.project.packed_vray_project import PackedVRayProject


class GRIDMARKETS_OT_submit_vray_project(bpy.types.Operator):
    bl_idname = "gridmarkets.submit_new_vray_project"
    bl_label = "Submit V-Ray Project"
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    project_name = bpy.props.StringProperty(
        name="Project Name",
        description="The name of the job as it will show in the render manager",
        default="",
        maxlen=256
    )

    job_name = bpy.props.StringProperty(
        name="Job Name",
        description="The name of the job as it will show in the render manager",
        default="V-Ray Job",
        maxlen=256
    )

    frame_ranges = bpy.props.StringProperty(
        name="Frame Ranges",
        description="Defines the frame range in format start [end] [step],[start [end] [step]],...",
        default="1 1 1",
        maxlen=256
    )

    output_width = bpy.props.IntProperty(
        name="Output Width",
        description="Defines the render output width",
        default=0,
    )

    output_height = bpy.props.IntProperty(
        name="Output Height",
        description="Defines the render output height",
        default=0,
    )

    output_prefix = bpy.props.StringProperty(
        name="Output Prefix",
        description="Defines the render output file prefix",
        default="",
        maxlen=256
    )

    output_format = bpy.props.StringProperty(
        name="Output Format",
        description="Defines the render output format",
        default="EXR",
        maxlen=256
    )

    output_path = bpy.props.StringProperty(
        name="Output Path",
        description="Defines the path to download the results to",
        default="",
        maxlen=256
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

                    elif result is None:
                        pass

                    else:
                        raise RuntimeError("Method returned unexpected result:", result)

                self.thread.join()
                self.user_interface.set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        props = context.scene.props
        self.remote_project_container = plugin.get_remote_project_container()
        self.user_interface = plugin.get_user_interface()

        wm = context.window_manager
        self.bucket = Queue()
        self.thread = ExcThread(self.bucket, self._execute,
                                args=(props.project_options, self.project_name, self.job_name, self.frame_ranges,
                                      self.output_height, self.output_width, self.output_prefix, self.output_format,
                                      self.output_path),
                                kwargs={})

        # summary view can not be open when submitting otherwise crash (since submitting blender scenes still accesses
        # the context)
        props.submission_summary_open = False
        self.thread.start()

        self.timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        self.user_interface.set_is_running_operation_flag(True)
        self.user_interface.set_running_operation_message("Submitting V-Ray project...")
        return {'RUNNING_MODAL'}

    @staticmethod
    def _execute(selected_project_option, project_name, job_name, frame_ranges, output_height, output_width,
                 output_prefix, output_format, output_path):

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()

        if selected_project_option == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            EXPORT_PATH = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

            exporter = VRaySceneExporter()
            exporter.export(EXPORT_PATH)

            packed_project = PackedVRayProject(EXPORT_PATH, EXPORT_PATH / "scene_scene.vrscene")
            packed_project.set_name(project_name)

            return api_client.submit_new_vray_project(packed_project,
                                                      job_name,
                                                      frame_ranges,
                                                      output_height,
                                                      output_width,
                                                      output_prefix,
                                                      output_format,
                                                      pathlib.Path(output_path))
        else:
            remote_project_container = plugin.get_remote_project_container()
            remote_project = remote_project_container.get_project_with_id(selected_project_option)

            api_client.submit_existing_vray_project(remote_project,
                                                    job_name,
                                                    frame_ranges,
                                                    output_height,
                                                    output_width,
                                                    output_prefix,
                                                    output_format,
                                                    pathlib.Path(output_path))
            return None


classes = (
    GRIDMARKETS_OT_submit_vray_project,
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

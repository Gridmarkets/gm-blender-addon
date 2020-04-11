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

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon import constants, utils, utils_blender


class GRIDMARKETS_OT_Submit(bpy.types.Operator):
    """Class to represent the 'Submit' operation."""

    bl_idname = constants.OPERATOR_SUBMIT_ID_NAME
    bl_label = constants.OPERATOR_SUBMIT_LABEL

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name = bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
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

    def invoke(self, context, event):
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

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        props = context.scene.props
        self.remote_project_container = plugin.get_remote_project_container()
        self.user_interface = plugin.get_user_interface()

        wm = context.window_manager
        self.bucket = Queue()
        self.thread = ExcThread(self.bucket, self._execute,
                                args=(props.project_options, self.project_name), kwargs={})

        # summary view can not be open when submitting otherwise crash (since submitting blender scenes still accesses
        # the context)
        props.submission_summary_open = False
        self.thread.start()

        self.timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        self.user_interface.set_is_running_operation_flag(True)
        self.user_interface.set_running_operation_message("Submitting project...")
        return {'RUNNING_MODAL'}

    @staticmethod
    def _execute(selected_project_option, project_name: str):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager
        from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter

        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()

        if selected_project_option == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            temp_dir = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

            packed_project = BlenderSceneExporter().export(temp_dir)
            packed_project.set_name(project_name)
            return api_client.submit_new_blender_project(packed_project)
        else:
            remote_project_container = plugin.get_remote_project_container()
            remote_project = remote_project_container.get_project_with_id(selected_project_option)
            api_client.submit_existing_blender_project(remote_project)
            return None



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

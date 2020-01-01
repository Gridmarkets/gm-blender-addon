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
from queue import Empty

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_project import \
    GRIDMARKETS_OT_upload_project


class GRIDMARKETS_OT_upload_packed_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_UPLOAD_PACKED_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PACKED_PROJECT_LABEL
    bl_description = constants.OPERATOR_UPLOAD_PACKED_PROJECT_DESCRIPTION
    bl_options = {'REGISTER'}

    bucket = None
    timer = None
    thread: ExcThread = None
    plugin = None

    def modal(self, context, event):

        if event.type == 'TIMER':
            self.plugin.get_user_interface().increment_running_operation_spinner()
            utils_blender.force_redraw_addon()

            if not self.thread.isAlive():
                try:
                    result = self.bucket.get(block=False)
                except Empty:
                    raise RuntimeError("bucket is Empty")
                else:
                    if type(result) != RemoteProject:
                        raise RuntimeError("Method returned unexpected result:", result)

                self.thread.join()
                self.plugin.get_user_interface().set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import \
            RejectedTransitionInputError
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        log = plugin.get_logging_coordinator().get_logger(self.bl_idname)

        user_interface = plugin.get_user_interface()

        # validate the project attribute make up a valid project
        try:
            attributes = utils_blender.get_project_attributes()
        except RejectedTransitionInputError as e:
            # if a transition failed then one of the attributes is invalid
            self.report({'ERROR'}, e.user_message)
            return {"FINISHED"}

        root_dir = pathlib.Path(user_interface.get_root_directory())

        if not root_dir.exists():
            self.report({'ERROR_INVALID_INPUT'}, "Root Directory does not exist.")
            return {"FINISHED"}

        packed_project = PackedProject(attributes[api_constants.API_KEYS.PROJECT_NAME],
                                       root_dir,
                                       set(utils_blender.get_project_files([])),
                                       attributes)

        args = (
            packed_project,
            user_interface.get_upload_all_files_in_root()
        )

        log.info("Uploading packed project...")
        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 GRIDMARKETS_OT_upload_packed_project._execute,
                                                                 args,
                                                                 {},
                                                                 "Uploading packed project...")

    @staticmethod
    def _execute(packed_project: PackedProject, upload_root_dir: bool):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        return api_client.upload_project(packed_project, upload_root_dir, delete_local_files_after_upload=False)


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

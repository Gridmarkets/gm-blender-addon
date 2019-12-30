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

    def invoke(self, context, event):
        return GRIDMARKETS_OT_upload_project.boilerplate_invoke(self, context, event)

    def execute(self, context):
        from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import \
            RejectedTransitionInputError
        
        # validate the project attribute make up a valid project
        try:
            attributes = utils_blender.get_project_attributes()
            print(attributes)
        except RejectedTransitionInputError as e:
            # if a transition failed then one of the attributes is invalid
            self.report({'ERROR'}, e.user_message)
            return {"FINISHED"}

        args = (
            attributes,
        )

        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 GRIDMARKETS_OT_upload_packed_project._execute,
                                                                 args,
                                                                 {},
                                                                 "Uploading packed project...")

    @staticmethod
    def _execute(attributes):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        packed_project = PackedProject("", pathlib.Path("bob"), set(), attributes)
        remote_project = RemoteProject.convert_packed_project(packed_project)

        plugin.get_remote_project_container().append(remote_project)
        utils_blender.force_redraw_addon()
        return remote_project

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.add_remote_project import \
            GRIDMARKETS_OT_add_remote_project
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        root = plugin.get_api_client().get_api_schema().get_root_project_attribute()

        GRIDMARKETS_OT_add_remote_project.draw_project_attributes(self.layout, context, root)


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

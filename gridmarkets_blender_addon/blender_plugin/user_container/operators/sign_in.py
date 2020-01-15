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

import traceback
from queue import Queue, Empty

from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_project import \
    GRIDMARKETS_OT_upload_project
from gridmarkets_blender_addon.meta_plugin.user import User
from gridmarkets_blender_addon.meta_plugin.errors.invalid_email_error import InvalidEmailError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_access_key_error import InvalidAccessKeyError
from gridmarkets_blender_addon.meta_plugin.errors.invalid_user_error import InvalidUserError
from gridmarkets_blender_addon.meta_plugin.errors.api_error import APIError
from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread


class GRIDMARKETS_OT_sign_in_new_user(bpy.types.Operator):
    bl_idname = "gridmarkets.sign_in_new_user"
    bl_label = "Sign-in new user"
    bl_options = {"REGISTER"}
    bl_description = "Sign in " + constants.COMPANY_NAME

    bucket = None
    timer = None
    thread: ExcThread = None
    plugin = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            user_interface = self.plugin.get_user_interface()
            user_interface.increment_running_operation_spinner()
            utils_blender.force_redraw_addon()

            if not self.thread.isAlive():
                try:
                    result = self.bucket.get(block=False)
                except Empty:
                    raise RuntimeError("bucket is Empty")
                else:
                    if type(result) == InvalidEmailError:
                        user_interface.set_auth_email_validity_flag(False)
                        user_interface.set_auth_access_key_validity_flag(True)
                        user_interface.set_auth_email_validity_message(result.user_message)
                        user_interface.set_auth_access_key_validity_message("")

                    elif type(result) == InvalidAccessKeyError:
                        user_interface.set_auth_email_validity_flag(True)
                        user_interface.set_auth_access_key_validity_flag(False)
                        user_interface.set_auth_email_validity_message("")
                        user_interface.set_auth_access_key_validity_message(result.user_message)

                    elif type(result) == InvalidUserError:
                        user_interface.set_auth_email_validity_flag(True)
                        user_interface.set_auth_access_key_validity_flag(True)
                        user_interface.set_user_validity_flag(False)
                        user_interface.set_user_validity_message(result.user_message)

                    elif type(result) == APIError:
                        user_interface.set_auth_email_validity_flag(True)
                        user_interface.set_auth_access_key_validity_flag(True)
                        user_interface.set_user_validity_flag(False)
                        user_interface.set_user_validity_message(result.user_message)

                    elif result is None:
                        user_interface.set_auth_email_validity_flag(True)
                        user_interface.set_auth_access_key_validity_flag(True)
                        user_interface.set_auth_email_validity_message("")
                        user_interface.set_auth_access_key_validity_message("")
                        user_interface.set_user_validity_flag(True)
                        user_interface.set_user_validity_message("")

                    else:
                        # todo move this into a super class method
                        logging_coordinator = self.plugin.get_logging_coordinator()
                        logger = logging_coordinator.get_logger(self.bl_label)

                        error_message = "Sign-in method returned unexpected result of type \"" + str(type(result)) + \
                                        "\". Return value is: " + str(result) + "."

                        if isinstance(result, Exception) and hasattr(result, "__traceback__"):
                            stack_trace = traceback.format_tb(result.__traceback__)
                            for line in stack_trace:
                                error_message = error_message + str(line)

                        logger.error(error_message)
                        self.report({"ERROR"}, error_message)

                self.thread.join()
                user_interface.set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()

        user_interface = plugin.get_user_interface()
        auth_email = user_interface.get_auth_email()
        auth_access_key = user_interface.get_auth_access_key()
        user = User(auth_email, auth_access_key)

        args = (
            user,
        )

        kwargs = {
            "skip_validation": False,
        }

        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 api_client.sign_in,
                                                                 args,
                                                                 kwargs,
                                                                 "Signing in...")


classes = (
    GRIDMARKETS_OT_sign_in_new_user,
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

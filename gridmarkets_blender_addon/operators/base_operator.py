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
import traceback
import typing

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon.meta_plugin.logger import Logger
from gridmarkets_blender_addon import utils_blender


class BaseOperator(bpy.types.Operator):
    """
    This class is inherited by operators which need to run an operation in a separate thread.

    It provides boilerplate code for executing the operation, polling the response from the thread in
    a modal fashion and handling errors.
    """

    _bucket = None
    _timer = None
    _thread: ExcThread = None
    _plugin = None
    _logger = None

    def setup_operator(self):
        """
        Should be called at beginning of execution
        """

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        self._plugin = plugin
        self._logger = plugin.get_logging_coordinator().get_logger(self.bl_idname)

    def boilerplate_execute(self: 'BaseOperator',
                            context: bpy.types.Context,
                            method: typing.Callable,
                            args: typing.Tuple,
                            kwargs: typing.Dict[str, any],
                            running_operation_message: str):
        """
        Should be called from operator.execute
        """

        # add a lock on logging
        plugin = self.get_plugin()
        plugin.get_logging_coordinator().add_thread_safe_logging_lock()

        wm = context.window_manager
        self._bucket = Queue()
        self._thread = ExcThread(self._bucket,
                                 method,
                                 args=args,
                                 kwargs=kwargs)
        self._thread.start()

        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        user_interface = self._plugin.get_user_interface()
        user_interface.set_is_running_operation_flag(True)
        user_interface.set_running_operation_message(running_operation_message)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'TIMER':
            plugin = self.get_plugin()
            user_interface = plugin.get_user_interface()
            user_interface.increment_running_operation_spinner()

            logging_coordinator = plugin.get_logging_coordinator()
            logging_coordinator.flush()

            utils_blender.force_redraw_addon()

            # if the thread has completed
            if not self.get_thread().isAlive():

                # attempt to get the result from worker
                try:
                    result = self.get_result_bucket().get(block=False)
                except Empty as e:
                    # if there is no result something has gone wrong
                    result = e

                # if the result is not an expected result
                # (e.g. it is of the expected return type or is of an expected error type)
                if not self.handle_expected_result(result):
                    # then handle it as an unexpected result
                    self.handle_unexpected_result(result)

                # clean up logic
                self.get_thread().join()
                user_interface.set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.get_timer())

                logging_coordinator.remove_thread_safe_logging_lock()
                logging_coordinator.flush()

                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def handle_expected_result(self, result) -> bool:
        raise NotImplementedError

    def handle_unexpected_result(self, result: any):

        error_message = "Unexpected result returned by thread of type \"" + str(type(result)) + \
                        "\". Return value is: " + str(result) + "."

        # if the return value is an exception, add it's stack trace to the error message
        if isinstance(result, Exception) and hasattr(result, "__traceback__"):
            stack_trace = traceback.format_tb(result.__traceback__)
            for line in stack_trace:
                error_message = error_message + str(line)

        self.report_and_log({"ERROR"}, error_message)

    def report_and_log(self, type, message):
        # displays the error message to the user in a pop-up and outputs it to the console
        self.report(type, message)

        logger = self.get_logger()
        if type.intersection({'ERROR', 'ERROR_INVALID_INPUT', 'ERROR_INVALID_CONTEXT', 'ERROR_OUT_OF_MEMORY'}):
            logger.error(message)
        elif type.intersection({'WARNING'}):
            logger.warning(message)
        elif type.intersection({'DEBUG'}):
            logger.debug(message)
        else:
            logger.info(message)

    def get_plugin(self) -> 'Plugin':
        return self._plugin

    def get_result_bucket(self) -> Queue:
        return self._bucket

    def get_thread(self) -> ExcThread:
        return self._thread

    def get_timer(self) -> bpy.types.Timer:
        return self._timer

    def get_logger(self) -> Logger:
        return self._logger

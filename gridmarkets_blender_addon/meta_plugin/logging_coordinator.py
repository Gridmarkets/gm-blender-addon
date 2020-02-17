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

__all__ = 'LoggingCoordinator'

import os
import queue
import typing

from .logger import Logger

if typing.TYPE_CHECKING:
    from . import LogHistoryContainer, LogItem, Plugin


class LoggingCoordinator:
    """
    A class for creating loggers and storing their messages in a list that the ui can draw in a thread safe manner.
    """

    def __init__(self, plugin: 'Plugin', log_history_container: 'LogHistoryContainer'):
        self._log_history_container = log_history_container
        self._multi_thread_counter: int = 0
        self._queue: queue.Queue = queue.Queue()
        self._plugin = plugin

    def get_plugin(self) -> 'Plugin':
        return self._plugin

    def is_thread_safe_mode_enabled(self) -> bool:
        return self._multi_thread_counter > 0

    def set_thread_safe_mode(self, enabled: bool) -> None:
        if enabled:
            self._multi_thread_counter += 1
        else:
            self._multi_thread_counter -= 1

            if self._multi_thread_counter < 0:
                raise ValueError("Muti-thread counter should never be less than 1")

    def add_thread_safe_logging_lock(self):
        self.set_thread_safe_mode(True)

    def remove_thread_safe_logging_lock(self):
        self.set_thread_safe_mode(False)

    def get_logger(self, name: str = None) -> 'Logger':
        return Logger(name, self)

    def get_log_history_container(self) -> 'LogHistoryContainer':
        return self._log_history_container

    def serialize_logs(self) -> str:
        sys_info = self.get_plugin().get_plugin_utils().get_sys_info()

        output = ''

        for log_item in self.get_log_history_container().get_all():
            output += log_item.get_date() + ' ' + \
                      log_item.get_time() + ' ' + \
                      log_item.get_logger_name() + ' ' + \
                      log_item.get_level() + ' ' + \
                      log_item.get_message() + os.linesep

        return sys_info + os.linesep + output

    def copy_logs_to_clipboard(self) -> None:
        plugin_utils = self.get_plugin().get_plugin_utils()
        plugin_utils.copy_to_clipboard(self.serialize_logs())

    def save_logs_to_file(self, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.serialize_logs())
            f.close()

    def queue(self, log_item: 'LogItem') -> None:
        """
        Add the log_item to the queue if operating in multi-threaded mode, otherwise append straight to the log history
        container.
        """

        if self.is_thread_safe_mode_enabled():
            self._queue.put(log_item)
        else:
            self._log_history_container.append(log_item)

    def flush(self) -> None:
        """ Call this in the main thread. """

        while True:
            try:
                logged_item = self._queue.get(block=False)
                self._log_history_container.append(logged_item)
            except queue.Empty:
                return

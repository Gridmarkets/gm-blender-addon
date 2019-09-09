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

import queue

from gridmarkets_blender_addon.meta_plugin.log_item import LogItem
from gridmarkets_blender_addon.meta_plugin.logger import Logger
from gridmarkets_blender_addon.meta_plugin.log_history_container import LogHistoryContainer


class LoggingCoordinator:
    """
    A class for creating loggers and storing their messages in a list that the ui can draw in a thread safe manner.
    """

    def __init__(self, log_history_container: LogHistoryContainer):
        self._log_history_container = log_history_container
        self._thread_safe: bool = False
        self._queue: queue.Queue = queue.Queue()

    def is_thread_safe_mode_enabled(self) -> bool:
        return self._thread_safe

    def set_thread_safe_mode(self, enabled: bool) -> None:
        self._thread_safe = enabled

    def get_logger(self, name: str = None) -> Logger:
        return Logger(name, self)

    def get_log_history_container(self) -> LogHistoryContainer:
        return self._log_history_container

    def queue(self, log_item: LogItem) -> None:
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

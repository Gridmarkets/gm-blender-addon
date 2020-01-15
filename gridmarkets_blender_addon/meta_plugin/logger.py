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

import logging
import datetime

from gridmarkets_blender_addon.meta_plugin.log_item import LogItem


class Logger:
    """
    A class which logs messages using both pythons internal logging implementation and to a logging queue in the logging
    coordinator.
    """

    def __init__(self, name: str, logging_coordinator: 'LoggingCoordinator'):
        self._logger = logging.getLogger(name)
        self._name = name
        self._logging_coordinator = logging_coordinator

    def _log(self, msg: str, level: str) -> None:

        # fail fast if msg is not a string
        if type(msg) is not str:
            raise ValueError("Logging message must be a string type not a " + str(type(msg)) + " type.", msg)

        log_item = LogItem(self._name, level, datetime.datetime.now(), msg)
        self._logging_coordinator.queue(log_item)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._log(msg, "DEBUG")
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self._log(msg, "INFO")
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._log(msg, "WARNING")
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._log(msg, "ERROR")
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args, exc_info=True, **kwargs):
        self._log(msg, "ERROR")
        self._logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._log(msg, "ERROR")
        self._logger.critical(msg, *args, **kwargs)

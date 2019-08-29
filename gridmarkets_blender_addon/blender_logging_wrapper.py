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
import bpy
import os
from time import gmtime, strftime
from gridmarkets_blender_addon.constants import PLUGIN_VERSION
from gridmarkets_blender_addon.utils_blender import force_redraw_addon


class BlenderLoggingWrapper:
    """
    A very simple wrapper class that wrappers a logging.Logger and exposes some basic functions. It is designed to be
    used from blender operators so they can optionally output messages to the user using Operator.report().
    """

    def __init__(self, logger):
        """ Constructor

        :param logger: The logger to wrap
        :type logger: logging.Logger
        """

        self._logger = logger
        self._buffer = []

    def _handel_logging_message(self, props, msg, level):

        lines = msg.splitlines()
        line_count = len(lines)
        time = gmtime()

        # report each line individually because blender has problems with multi-line reports (They display backwards in the
        # info panel)
        for i, line in enumerate(lines):
            # replace tabs since the blender info console can not display them
            line = line.replace('\t', ' ' * 4)

            log_item = props.log_items.add()

            # add the logger name and time stamp to the first line of a log message
            if i == 0:
                log_item.name = self._logger.name
                log_item.date = strftime("%Y-%m-%d", time)
                log_item.time = strftime("%H:%M:%S", time)

            log_item.body = line
            log_item.level = level

        # if the last log item was selected then set the selected log item to the new last item
        if props.selected_log_item == len(props.log_items) - (line_count + 1):
            props.selected_log_item = props.selected_log_item + line_count

        force_redraw_addon()

    def _log(self, msg, level):
        """ Helper function which takes log message and adds it to the log_items list.

        :param level: The logging level of the message
        :type level: enum
        :param msg: The logging message
        :type msg: str
        :rtype: void
        """

        # add the message to the logging buffer
        self._buffer.append((msg, level))

        try:
            props = bpy.context.scene.props
        except AttributeError:
            return

        # handel all messages in the buffer
        while len(self._buffer) > 0:
            log_args = self._buffer.pop(0)
            self._handel_logging_message(props, log_args[0], log_args[1])


    def debug(self, msg, *args, **kwargs):
        """ Log debug message
        :param msg: The debug message
        :type msg: str
        :rtype: void
        """

        self._log(msg, "DEBUG")
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """ Log info message
        :param msg: The info message
        :type msg: str
        :rtype: void
        """

        self._log(msg, "INFO")
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """ Log warning message
        :param msg: The warning message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        self._log(msg, "WARNING")
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """ Log error message
        :param msg: The error message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        self._log(msg, "ERROR")
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """ Log exception message
        :param msg: The exception message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        self._log(msg, "ERROR")
        self._logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """ Log critical message
        :param msg: The critical message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        self._log(msg, "ERROR")
        self._logger.critical(msg, *args, **kwargs)

    def clear_logs(self):
        props = bpy.context.scene.props
        props.log_items.clear()
        props.selected_log_item = -1


def get_wrapped_logger(name):
    """ Alternate definition of logging.getLogger() only it returns a wrapped Logger instead. Useful for cutting down on
        the number of imports necessary when creating a wrapped logger.

    :param name: The name of the logger
    :type name: str
    :return: The wrapped Logger
    :rtype: BlenderLoggingWrapper
    """

    return BlenderLoggingWrapper(logging.getLogger(name))

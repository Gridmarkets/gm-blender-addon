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

import datetime
import time


class LogItem:
    """
    A class representing a single logged message plus all the relevant accompanying information
    """

    def __init__(self, logger_name: str, level: str, date_time: datetime.datetime, message: str):
        self._logger_name = logger_name
        self._level = level
        self._date_time = date_time
        self._message = message

    def get_logger_name(self) -> str:
        return self._logger_name

    def get_level(self) -> str:
        return self._level

    def get_date_time(self) -> datetime.datetime:
        return self._date_time

    def get_date(self) -> str:
        return time.strftime("%Y-%m-%d", self._date_time.date())

    def get_time(self) -> str:
        return time.strftime("%H:%M:%S", self._date_time.date())

    def get_message(self) -> str:
        return self._message

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

__all__ = 'PluginError'

import sys
import traceback
import typing


class PluginError(Exception):

    def __init__(self, message: typing.Optional[str] = None):
        Exception.__init__(self, message)

        self._message = message

        try:
            self.traceback = traceback.extract_tb(sys.exc_info()[2])

        except AttributeError:
            self.traceback = None
            pass

    def __str__(self):
        msg = self._message or '<empty message>'
        return msg

    @property
    def user_message(self):
        return self._message

    def __repr__(self):

        class_name = self.__class__.__name__
        msg = self._message or '<empty message>'

        return "%s(message=%r)" % (class_name, msg)

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

__all__ = 'ExcThread'

import typing
import threading
from queue import Queue


class ExcThread(threading.Thread):
    """
    A Threading class which captures exceptions as well as return values and stores them in a queue
    """

    def __init__(self, bucket: Queue, target, args: typing.Tuple = None, kwargs: typing.Dict = None):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self._target = target
        self._args = args if args else ()
        self._kwargs = kwargs if kwargs else {}

    def run(self):
        try:
            result = self._target(*self._args, **self._kwargs)
            self.bucket.put(result)
        except Exception as e:
            self.bucket.put(e)

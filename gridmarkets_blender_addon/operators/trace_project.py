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
from bpy_extras.io_utils import ImportHelper
import os
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.bat_progress_callback import BatProgressCallback

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_trace_project(bpy.types.Operator, ImportHelper):
    bl_idname = constants.OPERATOR_TRACE_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_TRACE_PROJECT_LABEL
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    _all_blend_file = '*.blend'

    # filters the files the user is able to select
    filter_glob = bpy.props.StringProperty(
        default = _all_blend_file,
        options={'HIDDEN'}
    )

    def execute(self, context):
        """ Run for every file selected by the user """
        filename, extension = os.path.splitext(self.filepath)

        log.info("Tracing %s" % self.filepath)

        # create the progress callback
        progress_cb = BatProgressCallback(log)

        # find all dependencies
        dependencies = utils_blender.trace_blend_file(self.filepath, progress_cb=progress_cb)

        # store the trace output as a single string
        trace_summary = "Trace summary:"

        for key, value in dependencies.items():
            trace_summary = trace_summary + os.linesep + "%s has the following dependencies:" % key

            for asset in value:
                trace_summary = trace_summary + os.linesep + '\t' + str(asset)

        log.info(trace_summary)

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_trace_project,
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

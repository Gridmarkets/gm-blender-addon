import bpy
from bpy_extras.io_utils import ImportHelper
import os
import constants
import utils_blender

import logging
log = logging.getLogger(__name__)

class GRIDMARKETS_OT_trace_project(bpy.types.Operator, ImportHelper):
    bl_idname = constants.OPERATOR_TRACE_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_TRACE_PROJECT_LABEL
    bl_icon = 'BLEND_FILE'
    bl_options = {'UNDO'}

    _all_blend_file = '*.blend'

    # filters the files the user is able to select
    filter_glob: bpy.props.StringProperty(
        default = _all_blend_file,
        options={'HIDDEN'}
    )

    def execute(self, context):
        """ Run for every file selected by the user """
        filename, extension = os.path.splitext(self.filepath)

        self.report({"INFO"}, "Tracing %s" % self.filepath)
        log.info("Tracing %s" % self.filepath)

        # find all dependencies
        dependencies = utils_blender.trace_blend_file(self.filepath)


        for key, value in dependencies.items():
            self.report({"INFO"}, key + " has the following dependencies:")

            for asset in value:
                self.report({"INFO"}, '\t' + str(asset))

        #self.log.warning(trace_report)

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

import bpy

import constants
import properties
import utils
import utils_blender


from temp_directory_manager import TempDirectoryManager
from icon_loader import IconLoader
from invalid_input_error import InvalidInputError

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *

# ------------------------------------------------------------------------
#    Lists
# ------------------------------------------------------------------------


class GRIDMARKETS_UL_frame_range(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """ A function which defines how each list item is drawn """

        row = layout.row()
        row.active = item.enabled

        # users should be familiar with the restrict render icon and understand what it denotes
        enabled_icon = ("RESTRICT_RENDER_OFF" if item.enabled else "RESTRICT_RENDER_ON")

        row.prop(item, "enabled", icon=enabled_icon, text="", emboss=item.enabled)
        row.label(text = item.name)
        row.prop(item, "frame_start", text="Start")
        row.prop(item, "frame_end", text="End")
        row.prop(item, "frame_step", text="Step")

    def invoke(self, context, event):
        pass


class GRIDMARKETS_UL_project(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon=constants.PROJECT_ICON)


class GRIDMARKETS_UL_job(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", icon=constants.JOB_ICON, emboss=False)


class GRIDMARKETS_UL_log(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        props = context.scene.props

        row = layout.row(align=True)
        row.alignment = 'LEFT'

        # line text
        row.alert = item.level == 'ERROR' # if the message is an error then colour red

        text = ''

        if item.date and props.show_log_dates:
            text = text + item.date + ' '

        if item.time and props.show_log_times:
            text = text + item.time + ' '

        if item.name and props.show_log_modules:
            text = text + item.name + ' '

        text = text + item.body

        row.label(text=text)


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


classes = (
    GRIDMARKETS_UL_frame_range,
    GRIDMARKETS_UL_project,
    GRIDMARKETS_UL_job,
    GRIDMARKETS_UL_log
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

import bpy

import constants
import properties
import utils
import utils_blender


from temp_directory_manager import TempDirectoryManager
from icon_loader import IconLoader
from property_sanitizer import PropertySanitizer
from invalid_input_error import InvalidInputError

from gridmarkets.envoy_client import EnvoyClient
from gridmarkets.project import Project
from gridmarkets.job import Job
from gridmarkets.watch_file import WatchFile
from gridmarkets.errors import *


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------


class GRIDMARKETS_OT_frame_range_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the frame range list menu """

    bl_idname = constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_LABEL

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('EDIT', "Edit", "")
        )
    )

    def invoke(self, context, event):
        props = context.scene.props
        selected_job = props.jobs[props.selected_job]
        index = selected_job.selected_frame_range

        # do not perform any action if disabled
        if not selected_job.use_custom_frame_ranges:
            return {"FINISHED"}

        # if the currently selected frame_range does not exist then the only allowed action is 'ADD'
        try:
            item = selected_job.frame_ranges[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(selected_job.frame_ranges) - 1:
                selected_job.selected_frame_range += 1

            elif self.action == 'UP' and index >= 1:
                selected_job.selected_frame_range -= 1

            elif self.action == 'REMOVE':
                # never remove the last frame range
                if len(selected_job.frame_ranges) < 2:
                    return {"FINISHED"}

                selected_job.frame_ranges.remove(index)

                if selected_job.selected_frame_range > 0:
                    selected_job.selected_frame_range -= 1

            elif self.action == 'EDIT':
                bpy.ops.gridmarkets.edit_frame_range('INVOKE_DEFAULT')

        if self.action == 'ADD':

            # add a frame range to the list
            frame_range = selected_job.frame_ranges.add()

            frame_range.name = utils.create_unique_object_name(selected_job.frame_ranges, name_prefix=constants.FRAME_RANGE_PREFIX)
            frame_range.enabled = True
            frame_range.frame_start = constants.DEFAULT_FRAME_RANGE_START_VALUE
            frame_range.frame_end = constants.DEFAULT_FRAME_RANGE_END_VALUE
            frame_range.frame_step = constants.DEFAULT_FRAME_RANGE_STEP_VALUE

            selected_job.selected_frame_range = len(selected_job.frame_ranges) - 1

        return {"FINISHED"}


class GRIDMARKETS_OT_edit_frame_range(bpy.types.Operator):
    bl_idname = constants.OPERATOR_EDIT_FRAME_RANGE_ID_NAME
    bl_label = constants.OPERATOR_EDIT_FRAME_RANGE_LABEL
    bl_options = {'UNDO'}

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    name: bpy.props.StringProperty(
        name="Range Name",
        description="Adding a name to your frame ranges makes them searchable",
        default="",
        maxlen=256
    )

    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="If disabled the frame range will be ignored by Gridmarekts",
        default=True
    )

    frame_start: bpy.props.IntProperty(
        name="Frame Start",
        description="First frame of the rendering range",
        default=1,
        min=0,
        get=properties.FrameRangeProps.get_frame_start,
        set=properties.FrameRangeProps.set_frame_start
    )

    frame_end: bpy.props.IntProperty(
        name="Frame End",
        description="Final frame of the rendering range",
        default=255,
        min=0,
        get=properties.FrameRangeProps.get_frame_end,
        set=properties.FrameRangeProps.set_frame_end
    )

    frame_step: bpy.props.IntProperty(
        name="Step Size",
        description="Number of frames to skip forward while rendering back each frame",
        default=1,
        min=1
    )

    def invoke(self, context, event):

        props = context.scene.props
        selected_job = props.jobs[props.selected_job]

        # don't create popup if custom frame ranges are not enabled
        if not selected_job.use_custom_frame_ranges:
            return {"FINISHED"}

        # Select the selected frame range for the selected job
        frame_range = selected_job.frame_ranges[selected_job.selected_frame_range]

        # set values for popup field inputs to default to
        self.name = frame_range.name
        self.enabled = frame_range.enabled
        self.frame_start = frame_range.frame_start
        self.frame_end = frame_range.frame_end
        self.frame_step = frame_range.frame_step

        # create popup
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """ Called after the user clicks the 'ok' button on the popup """

        props = context.scene.props
        selected_job = props.jobs[props.selected_job]

        # add a frame range to the list
        frame_range = selected_job.frame_ranges[selected_job.selected_frame_range]

        frame_range.name = self.name
        frame_range.enabled = True
        frame_range.frame_start = self.frame_start
        frame_range.frame_end = self.frame_end
        frame_range.frame_step = self.frame_step

        # force region to redraw otherwise the list wont update until next event (mouse over, etc)
        for area in bpy.context.screen.areas:
            if area.type == constants.PANEL_SPACE_TYPE:
                for region in area.regions:
                    if region.type == constants.PANEL_REGION_TYPE:
                        region.tag_redraw()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()

        # frame_range name
        row = box.row()
        row.label(text="Name")
        row.prop(self, "name", text="")

        # is frame_range enabled
        row = box.row()
        row.label(text="Enabled")
        row.prop(self, "enabled", text="")

        # Create two columns, by using a split layout.
        split = box.split()

        # First column
        col = split.column()
        col.label(text="Frame Start")
        col.label(text="Frame End")
        col.label(text="Step Size")

        # Second column, aligned
        col = split.column(align=True)
        col.prop(self, "frame_start")
        col.prop(self, "frame_end")
        col.prop(self, "frame_step")


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


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------


classes = (
    GRIDMARKETS_OT_frame_range_list_actions,
    GRIDMARKETS_OT_edit_frame_range,
    GRIDMARKETS_UL_frame_range,
    GRIDMARKETS_UL_project,
    GRIDMARKETS_UL_job
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

import bpy
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps


class GRIDMARKETS_OT_edit_frame_range(bpy.types.Operator):
    bl_idname = constants.OPERATOR_EDIT_FRAME_RANGE_ID_NAME
    bl_label = constants.OPERATOR_EDIT_FRAME_RANGE_LABEL
    bl_options = {'UNDO'}

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    name = bpy.props.StringProperty(
        name="Range Name",
        description="Adding a name to your frame ranges makes them searchable",
        default="",
        maxlen=256
    )

    enabled = bpy.props.BoolProperty(
        name="Enabled",
        description="If disabled the frame range will be ignored by Gridmarekts",
        default=True
    )

    frame_start = bpy.props.IntProperty(
        name="Frame Start",
        description="First frame of the rendering range",
        default=1,
        min=0,
        get=FrameRangeProps.get_frame_start,
        set=FrameRangeProps.set_frame_start
    )

    frame_end = bpy.props.IntProperty(
        name="Frame End",
        description="Final frame of the rendering range",
        default=255,
        min=0,
        get=FrameRangeProps.get_frame_end,
        set=FrameRangeProps.set_frame_end
    )

    frame_step = bpy.props.IntProperty(
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
        utils_blender.force_redraw_addon()

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


classes = (
    GRIDMARKETS_OT_edit_frame_range,
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

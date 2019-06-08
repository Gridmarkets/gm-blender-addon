import bpy
import constants


class GRIDMARKETS_PT_frame_ranges(bpy.types.Panel):
    """Create a Panel containing the frame ranges for a job """

    bl_idname = constants.PANEL_FRAME_RANGES_ID_NAME
    bl_label = constants.PANEL_FRAME_RANGES_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_JOBS_ID_NAME

    @classmethod
    def poll(self, context):
        job_count = len(context.scene.props.jobs)
        return job_count > 0

    def draw(self, context):
        layout = self.layout
        props = bpy.context.scene.props
        selected_job = props.jobs[props.selected_job]

        active = selected_job.use_custom_frame_ranges

        layout.prop(selected_job, "use_custom_frame_ranges")

        row = layout.row()
        row.active = active
        row.template_list("GRIDMARKETS_UL_frame_range", "", selected_job, "frame_ranges", selected_job, "selected_frame_range", rows=5)

        col = row.column()
        col.active = active

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME, icon='MODIFIER', text="").action = 'EDIT'

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME, icon='ADD', text="").action = 'ADD'
        sub.operator(constants.OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME, icon='REMOVE', text="").action = 'REMOVE'

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME, icon='TRIA_UP', text="").action = 'UP'
        sub.operator(constants.OPERATOR_FRAME_RANGE_ACTIONS_ID_NAME, icon='TRIA_DOWN', text="").action = 'DOWN'


classes = (
    GRIDMARKETS_PT_frame_ranges,
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

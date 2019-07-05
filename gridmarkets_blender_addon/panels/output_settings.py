import bpy
import constants
from types import SimpleNamespace


def _draw_frame_ranges_view(self, context):
    layout = self.layout
    props = bpy.context.scene.props
    selected_job = props.jobs[props.selected_job]
    frame_range_count = len(selected_job.frame_ranges)

    enabled = selected_job.use_custom_frame_ranges

    row = layout.row()
    row.active = enabled
    row.template_list("GRIDMARKETS_UL_frame_range", "", selected_job, "frame_ranges", selected_job,
                      "selected_frame_range", rows=5)

    col = row.column()
    col.active = enabled

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon='MODIFIER', text="").action = 'EDIT'

    sub = col.column(align=True)
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon='ADD', text="").action = 'ADD'

    remove = sub.row()
    # prevent the user removing the last frame range for a job
    if frame_range_count < 2:
        remove.enabled = False
    remove.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon='REMOVE', text="").action = 'REMOVE'

    sub = col.column(align=True)

    # disable up / down buttons if only one frame range
    if frame_range_count < 2:
        sub.enabled = False

    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon='TRIA_UP', text="").action = 'UP'
    sub.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon='TRIA_DOWN', text="").action = 'DOWN'


def _draw_output_path_view(self, context):
    layout = self.layout
    job = context.scene.props.jobs[context.scene.props.selected_job]

    # col.label(text="Relative output paths will only work if you have saved your scene", icon="QUESTION")
    layout.prop(job, "output_path")


def _draw_view(self, context, operator_id, view_name, draw_handler):
    views = context.scene.props.custom_settings_views
    job = context.scene.props.jobs[context.scene.props.selected_job]

    box = self.layout.box()
    col = box.column()
    row = col.row(align=True)
    row.alignment = 'LEFT'

    view = getattr(views, view_name + '_view')

    row.operator(
        operator_id,
        text="",
        icon='DISCLOSURE_TRI_DOWN' if view else 'DISCLOSURE_TRI_RIGHT',
        emboss=False,
    )

    row.prop(job, "use_custom_" + view_name)

    if view:
        draw_handler(SimpleNamespace(layout=col), context)


class GRIDMARKETS_PT_Output_Settings(bpy.types.Panel):
    """The plugin's output settings sub panel."""

    bl_idname = constants.PANEL_OUTPUT_SETTINGS_ID_NAME
    bl_label = constants.PANEL_OUTPUT_SETTINGS_LABEL
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
        scene = context.scene
        props = scene.props

        _draw_view(self, context, constants.OPERATOR_TOGGLE_FRAME_RANGES_VIEW_ID_NAME, "frame_ranges", _draw_frame_ranges_view)
        _draw_view(self, context, constants.OPERATOR_TOGGLE_OUTPUT_PATH_VIEW_ID_NAME, "output_path", _draw_output_path_view)

        #col.prop(job, "output_prefix")


classes = (
    GRIDMARKETS_PT_Output_Settings,
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

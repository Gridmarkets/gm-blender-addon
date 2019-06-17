import bpy
import constants


class GRIDMARKETS_PT_Jobs(bpy.types.Panel):
    """ Create a Panel which lists all user defined jobs """

    bl_idname = constants.PANEL_JOBS_ID_NAME
    bl_label = constants.PANEL_JOBS_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout
        props = bpy.context.scene.props
        job_count = len(props.jobs)

        layout.label(text='Preset Jobs')

        row = layout.row()
        row.template_list("GRIDMARKETS_UL_job", "", props, "jobs", props, "selected_job", rows=3)

        col = row.column()

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_JOB_ACTIONS_ID_NAME, icon='ADD', text="").action = 'ADD'
        sub2 = sub.row()

        # disable remove button if there are no projects to remove
        if job_count <= 0:
            sub2.enabled = False

        sub2.operator(constants.OPERATOR_JOB_ACTIONS_ID_NAME, icon='REMOVE', text="").action = 'REMOVE'

        sub = col.column(align=True)

        # disable up and down buttons if there are less than 2 projects
        if job_count < 2:
            sub.enabled = False

        sub.operator(constants.OPERATOR_JOB_ACTIONS_ID_NAME, icon='TRIA_UP', text="").action = 'UP'
        sub.operator(constants.OPERATOR_JOB_ACTIONS_ID_NAME, icon='TRIA_DOWN', text="").action = 'DOWN'


classes = (
    GRIDMARKETS_PT_Jobs,
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

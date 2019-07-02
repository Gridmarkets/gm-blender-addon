import bpy
import constants


class GRIDMARKETS_PT_Projects(bpy.types.Panel):
    """ Create a Panel which lists all uploaded projects """

    bl_idname = constants.PANEL_PROJECTS_ID_NAME
    bl_label = constants.PANEL_PROJECTS_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout
        props = bpy.context.scene.props
        project_count = len(props.projects)

        row = layout.row()
        row.template_list("GRIDMARKETS_UL_project", "", props, "projects", props, "selected_project", rows=2)

        col = row.column()

        sub = col.column(align=True)

        # disable up and down buttons if there are less than 2 projects
        if project_count < 2:
            sub.enabled = False

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon='TRIA_UP', text="").action = 'UP'
        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row(align=True)
        sub = row.column()

        # disable upload project button if already submitting or uploading
        if props.uploading_project or props.submitting_project:
            sub.enabled = False

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon='ADD',
                     text="Upload Project").action = 'UPLOAD'

        sub = row.column()

        # disable remove button if there are no projects to remove
        if project_count <= 0:
            sub.enabled = False

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon='REMOVE',
                     text="Remove Project").action = 'REMOVE'

        # upload status
        if props.uploading_project:
            layout.prop(props, "uploading_project_progress", text=props.uploading_project_status)


classes = (
    GRIDMARKETS_PT_Projects,
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

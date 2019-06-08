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

        if project_count <= 0:
            layout.label(text='You must upload a project before you can submit a job', icon='INFO')

        row = layout.row()
        row.template_list("GRIDMARKETS_UL_project", "", props, "projects", props, "selected_project", rows=2)

        col = row.column()

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_PROJECT_ACTIONS_ID_NAME, icon='MODIFIER', text="").action = 'EDIT'

        sub = col.column(align=True)
        sub.operator(constants.OPERATOR_PROJECT_ACTIONS_ID_NAME, icon='TRIA_UP', text="").action = 'UP'
        sub.operator(constants.OPERATOR_PROJECT_ACTIONS_ID_NAME, icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row(align=True)
        row.operator(constants.OPERATOR_PROJECT_ACTIONS_ID_NAME, icon='ADD', text="Upload Project").action = 'UPLOAD'
        row.operator(constants.OPERATOR_PROJECT_ACTIONS_ID_NAME, icon='REMOVE', text="Remove Project").action = 'REMOVE'


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

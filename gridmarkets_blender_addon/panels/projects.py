import bpy
import constants
from temp_directory_manager import TempDirectoryManager

def _draw_project_info_view(self, context):
    layout = self.layout
    props = bpy.context.scene.props
    project_count = len(props.projects)
    selected_project_index = props.selected_project

    if project_count > 0 and selected_project_index >= 0 and selected_project_index < project_count:
        project = props.projects[selected_project_index]
        temp_directory_manager = TempDirectoryManager.get_temp_directory_manager()
        association = temp_directory_manager.get_association_with_project_name(project.name)

        box = layout.box()
        col = box.column(align=True)

        col.label(text="Project Info", icon=constants.ICON_PROJECT)
        col.separator()

        col.label(text="Project name: %s" % project.name)
        sub = col.row(align=True)
        sub.enabled = False
        sub.label(text="The name of the project as it will appear in Envoy.")

        col.separator()

        sub = col.row()
        sub.label(text="Temporary directory path: %s" % association.get_temp_dir_name())
        op = sub.row()
        op.alignment = 'RIGHT'
        op.operator(constants.OPERATOR_DELETE_TEMPORARY_PROJECT_FILES_ID_NAME, text="Delete")

        sub = col.row(align=True)
        sub.enabled = False
        sub.label(text="The temporary directory project files are packed to before uploading. They are automatically "
                       "deleted when blender closes.")

        col.separator()

        sub = col.row()
        sub.label(text="Project status:")
        op = sub.row()
        op.alignment = 'RIGHT'
        op.operator(constants.OPERATOR_GET_SELECTED_PROJECT_STATUS_ID_NAME, text="Get status")

        if project.status:
            import json
            projecs_status = json.loads(project.status)

            split = col.split(percentage=0.2)

            keys = split.column()
            values = split.column()

            keys.label(text="Code: ")
            values.label(text=str(projecs_status["Code"]))

            keys.label(text="State: ")
            values.label(text=projecs_status["State"])

            keys.label(text="Message: ")
            values.label(text=projecs_status["Message"])

            keys.label(text="BytesDone: ")
            values.label(text=str(projecs_status["BytesDone"]))

            keys.label(text="BytesTotal: ")
            values.label(text=str(projecs_status["BytesTotal"]))

            keys.label(text="Speed: ")
            values.label(text=str(projecs_status["Speed"]))
        else:
            col.label(text="Status not yet fetched")

        sub = col.row(align=True)
        sub.enabled = False
        sub.label(
            text="Press 'Get status' to re-fetch the status of the project.")


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

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_UP, text="").action = 'UP'
        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_DOWN, text="").action = 'DOWN'

        row = layout.row(align=True)
        sub = row.column()

        # disable upload project button if already submitting or uploading
        if props.uploading_project or props.submitting_project:
            sub.enabled = False

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_ADD,
                     text="Upload Project").action = 'UPLOAD'

        sub = row.column()

        # disable remove button if there are no projects to remove
        if project_count <= 0:
            sub.enabled = False

        sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_REMOVE,
                     text="Remove Project").action = 'REMOVE'

        # upload status
        if props.uploading_project:
            layout.prop(props, "uploading_project_progress", text=props.uploading_project_status)

        _draw_project_info_view(self, context)


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

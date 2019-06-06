import bpy
import constants


class GRIDMARKETS_PT_Job_Info(bpy.types.Panel):
    """The plugin's job info sub panel."""

    bl_idname = constants.PANEL_JOB_INFO_ID_NAME
    bl_label = constants.PANEL_JOB_INFO_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Create two columns, by using a split layout.
        split = layout.split(factor=0.5)

        # First column
        col = split.column()
        col.label(text="Project Name:")
        col.label(text="Submission Label:")
        col.label(text="Artist Name:")
        col.label(text="Submission Comment:")
        col.label(text="Blender Version:")
        col.label(text="Render Engine:")

        # Second column, aligned
        col = split.column()
        col.prop(scene.props, "project_name", text="")
        col.prop(scene.props, "submission_label", text="")
        col.prop(scene.props, "artist_name", text="")
        col.prop(scene.props, "submission_comment", text="")

        col.alignment = 'RIGHT'
        col.label(text=bpy.app.version_string)
        col.label(text=bpy.context.scene.render.engine)

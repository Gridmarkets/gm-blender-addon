import bpy
import constants


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
        job = props.jobs[props.selected_job]

        col = layout.column()
        col.prop(job, "output_path")
        col.prop(job, "output_prefix")


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

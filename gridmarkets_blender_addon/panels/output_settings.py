import bpy
import constants


class GRIDMARKETS_PT_Output_Settings(bpy.types.Panel):
    """The plugin's output settings sub panel."""

    bl_idname = constants.PANEL_OUTPUT_SETTINGS_ID_NAME
    bl_label = constants.PANEL_OUTPUT_SETTINGS_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        col.prop(scene.props, "output_path")
        col.prop(scene.props, "output_prefix")

import bpy
import constants


class GRIDMARKETS_PT_Render_settings(bpy.types.Panel):
    """Create a Panel containing render related settings, such as frame range(s)"""

    bl_idname = constants.PANEL_RENDER_SETTINGS_ID_NAME
    bl_label = constants.PANEL_RENDER_SETTINGS_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw(self, context):
        layout = self.layout
        props = bpy.context.scene.props
        active = props.use_custom_frame_ranges

        row = layout.row()

        row.prop(props, "use_custom_frame_ranges")

        row = layout.row()
        row.active = active
        row.template_list("GRIDMARKETS_UL_frame_range", "", props, "frame_ranges", props, "selected_frame_range", rows=5)

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

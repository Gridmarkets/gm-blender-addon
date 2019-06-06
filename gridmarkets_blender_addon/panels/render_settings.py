import bpy


class GRIDMARKETS_PT_Render_settings(bpy.types.Panel):
    """Create a Panel containing render related settings, such as frame range(s)"""

    bl_idname = 'gridmarkets_render_settings_sub_panel'
    bl_label = "Render Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_parent_id = "gridmarkets_main_panel"

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
        sub.operator("gridmarkets.list_action", icon='MODIFIER', text="").action = 'EDIT'

        sub = col.column(align=True)
        sub.operator("gridmarkets.list_action", icon='ADD', text="").action = 'ADD'
        sub.operator("gridmarkets.list_action", icon='REMOVE', text="").action = 'REMOVE'

        sub = col.column(align=True)
        sub.operator("gridmarkets.list_action", icon='TRIA_UP', text="").action = 'UP'
        sub.operator("gridmarkets.list_action", icon='TRIA_DOWN', text="").action = 'DOWN'

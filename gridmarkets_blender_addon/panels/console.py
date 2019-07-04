import bpy
import constants


class GRIDMARKETS_PT_console(bpy.types.Panel):
    """ A Panel which displays the logging output in a simple console. """

    bl_idname = constants.PANEL_CONSOLE_ID_NAME
    bl_label = constants.PANEL_CONSOLE_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT
    bl_parent_id = constants.PANEL_MAIN_ID_NAME

    def draw_header(self, context):
        layout = self.layout

        # display Gridmarkets icon and version
        layout.label(text="", icon='CONSOLE')

    def draw(self, context):
        layout = self.layout
        props = context.scene.props
        box = layout.box()
        box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=6,
                          sort_lock=True)
        box.operator(constants.OPERATOR_COPY_LOGS_TO_CLIPBOARD_ID_NAME)


classes = (
    GRIDMARKETS_PT_console,
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

import bpy
import constants
import utils_blender
from icon_loader import IconLoader


class GRIDMARKETS_PT_Main(bpy.types.Panel):
    """Class to represent the plugins main panel. Contains all sub panels as well as 'Render' and 'Open Manager Portal'
    buttons.
    """

    bl_idname = constants.PANEL_MAIN_ID_NAME
    bl_label = constants.PANEL_MAIN_ID_LABEL
    bl_space_type = constants.PANEL_SPACE_TYPE
    bl_region_type = constants.PANEL_REGION_TYPE
    bl_context = constants.PANEL_CONTEXT

    @classmethod
    def poll(self, context):
        return context.window.screen.name == constants.INJECTED_SCREEN_NAME

    def draw_header(self, context):
        layout = self.layout

        # get the Gridmarkets icon
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

        # display Gridmarkets icon and version
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=constants.ADDON_NAME, icon_value=iconGM.icon_id)

        # get the plugin version as a string
        version_str = utils_blender.get_version_string()

        # version label
        sub = row.row(align=True)
        sub.enabled = False
        sub.label(text=version_str)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animating of properties

        props = context.scene.props

        # submit box
        box = layout.box()
        box.use_property_split = False
        row = box.row()

        # project options
        col = row.column(align=True)
        col.label(text="Project")
        sub = col.row()
        sub.enabled = False
        sub.label(text="The project to run the selected job against.")
        col.separator()
        col.prop(props, "project_options", text="")


        # job options
        col = row.column(align=True)
        col.label(text="Job")
        sub = col.row()
        sub.enabled = False
        sub.label(text="The render settings and output settings to use.")
        col.separator()
        col.prop(props, "job_options", text="")

        # submit button / progress indicator
        row = box.row(align=True)
        row.scale_y = 2.5
        if props.submitting_project:
            row.prop(props, "submitting_project_progress", text=props.submitting_project_status)
        else:
            # disable submit button when uploading project
            if props.uploading_project:
                row.enabled = False

            row.operator(constants.OPERATOR_SUBMIT_ID_NAME, text='Submit')


classes = (
    GRIDMARKETS_PT_Main,
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

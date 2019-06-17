import bpy
import constants
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
        return True  # context.object is not None

    def draw_header(self, context):
        layout = self.layout

        # get the Gridmarkets icon
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

        # display Gridmarkets icon and version
        layout.label(text="", icon_value=iconGM.icon_id)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animating of properties

        props = context.scene.props

        # get the plugin version as a string
        version_str = 'GM Blender Add-on v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(
            constants.PLUGIN_VERSION['minor']) + '.' + str(constants.PLUGIN_VERSION['build'])

        # version label
        row = layout.row(align=True)
        row.enabled = False
        row.label(text=version_str)

        layout.prop(props, "project_options")
        layout.prop(props, "job_options")

        # submit button
        row = layout.row(align=True)
        row.scale_y = 2.5
        row.operator(constants.OPERATOR_SUBMIT_ID_NAME, text='Submit')

        layout.separator_spacer()

        # Portal manager link
        row = layout.row(align=True)
        row.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME, icon='URL')

        # Cost calculator
        row = layout.row()
        row.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME, icon='URL')
        row.operator(constants.OPERATOR_OPEN_HELP_URL_ID_NAME, icon='HELP')


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

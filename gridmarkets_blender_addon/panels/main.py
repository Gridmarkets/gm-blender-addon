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
        props = context.scene.props
        project_count = len(props.projects)
        job_count = len(props.jobs)

        # get the plugin version as a string
        versionStr = 'Gridmarkets v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(
            constants.PLUGIN_VERSION['minor']) + '.' + str(constants.PLUGIN_VERSION['build'])

        # display help message
        if project_count < 1:
            layout.label(text='You must upload a project before you can submit', icon='INFO')

        elif job_count < 1:
            layout.label(text='You must create a job before you can submit', icon='INFO')

        # submit button
        row = layout.row(align=True)
        if project_count < 1 or job_count < 1:
            row.active=False
        row.operator(constants.OPERATOR_SUBMIT_ID_NAME)

        # Portal manager link
        row = layout.row(align=True)
        row.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME)

        # Cost calculator
        row = layout.row(align=True)
        row.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME)

        row = layout.row(align=True)
        row.enabled = False
        row.label(text=versionStr)


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

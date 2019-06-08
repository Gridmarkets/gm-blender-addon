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

    def draw(self, context):
        layout = self.layout

        # get the Gridmarkets icon
        preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
        iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

        # get the plugin version as a string
        versionStr = 'Gridmarkets v' + str(constants.PLUGIN_VERSION['major']) + '.' + str(
            constants.PLUGIN_VERSION['minor']) + '.' + str(constants.PLUGIN_VERSION['build'])

        # display Gridmarkets icon and version
        layout.label(text=versionStr, icon_value=iconGM.icon_id)

        # 'Submit' button
        row = layout.row(align=True)
        row.operator(constants.OPERATOR_SUBMIT_ID_NAME)

        # Portal manager link
        row = layout.row(align=True)
        row.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME)


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

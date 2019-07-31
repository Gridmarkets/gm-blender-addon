from gridmarkets_blender_addon.icon_loader import IconLoader
from gridmarkets_blender_addon import constants, utils_blender


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

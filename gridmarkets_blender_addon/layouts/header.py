# ##### BEGIN GPL LICENSE BLOCK #####
#
# GridMarkets Blender Add-on - A Blender Add-on for rendering scenes / files on the Grid Computing network GridMarkets
# Copyright (C) 2019  GridMarkets
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

from gridmarkets_blender_addon.icon_loader import IconLoader
from gridmarkets_blender_addon import constants, utils_blender


def draw_header(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()
    layout = self.layout
    user_interface = plugin.get_user_interface()
    signed_in_user = plugin.get_api_client().get_signed_in_user()

    # get the company icon
    preview_collection = IconLoader.get_preview_collections()[constants.MAIN_COLLECTION_ID]
    iconGM = preview_collection[constants.GRIDMARKETS_LOGO_ID]

    # display company icon and version
    row = layout.row()
    row.alignment = "CENTER"
    row.label(text=constants.ADDON_NAME, icon_value=iconGM.icon_id)

    # signed in indicator
    sub = row.row(align=True)

    if user_interface.is_running_operation():
        sub.label(text=user_interface.get_running_operation_message(),
                  icon_value=utils_blender.get_spinner(user_interface.get_running_operation_spinner()).icon_id)

    else:
        if signed_in_user:
            sub.label(text="Signed in as: " + signed_in_user.get_auth_email())
        else:
            sub.label(text="Not signed in", icon=constants.ICON_ERROR)

    # version label
    sub = row.row(align=True)
    sub.enabled = False
    sub.label(text='GM Blender Add-on Version ' + plugin.get_version().to_string())



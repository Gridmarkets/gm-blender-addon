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

from gridmarkets_blender_addon import constants


def draw_preferences(self, context):
    layout = self.layout
    layout.use_property_decorate = False  # No animating of properties

    col_box = layout.column()

    # draw add-on preferences
    addon_preferences = context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences
    if addon_preferences is not None:
        draw = getattr(addon_preferences, "draw", None)
        if draw is not None:
            addon_preferences_class = type(addon_preferences)
            box_prefs = col_box.box()
            box_prefs.label(text="Preferences:")
            addon_preferences_class.layout = box_prefs
            try:
                draw(context)
            except:
                import traceback
                traceback.print_exc()
                box_prefs.label(text="Error (see console)", icon=constants.ICON_ERROR)
            del addon_preferences_class.layout

    row = layout.row()
    row.operator_context = 'EXEC_AREA'

    row.scale_x = 1.3
    row.scale_y = 1.3

    row.operator("wm.save_userpref", text="Save Credentials")
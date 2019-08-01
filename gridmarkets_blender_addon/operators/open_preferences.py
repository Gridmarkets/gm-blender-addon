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

import bpy
from gridmarkets_blender_addon import constants, utils_blender

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_open_preferences(bpy.types.Operator):
    bl_idname = constants.OPERATOR_OPEN_PREFERENCES_ID_NAME
    bl_label = constants.OPERATOR_OPEN_PREFERENCES_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        log.info("Opening Gridmarkets add-on preferences menu...")

        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = constants.ADDON_NAME

        mod, info = utils_blender.get_addon(constants.ADDON_NAME)

        # expand the preferences box
        info['show_expanded'] = True

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_preferences,
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

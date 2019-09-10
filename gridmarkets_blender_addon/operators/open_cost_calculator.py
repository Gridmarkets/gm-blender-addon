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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_Open_Cost_Calculator(bpy.types.Operator):
    """Class to represent the 'Cost Calculator' operation. Opens the cost calculator page in the user's browser."""

    bl_idname = constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME
    bl_label = constants.OPERATOR_OPEN_COST_CALCULATOR_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        log = PluginFetcher.get_plugin().get_logging_coordinator().get_logger(self.bl_idname)

        log.info("Opening cost calculator...")

        # open the render manager url in the users browser
        bpy.ops.wm.url_open(url=constants.COST_CALCULATOR_URL)
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_Open_Cost_Calculator,
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

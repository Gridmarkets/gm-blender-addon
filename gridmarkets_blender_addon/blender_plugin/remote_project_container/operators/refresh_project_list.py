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

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon.meta_plugin.errors import *

class GRIDMARKETS_OT_refresh_project_list(BaseOperator):
    bl_idname = "gridmarkets.refresh_project_list"
    bl_label = "Refresh Remote Project List"
    bl_options = set()

    def handle_expected_result(self, result: any) -> bool:
        if result is None:
            return True

        elif type(result) == list:
            return True

        elif type(result) == APIClientError:
            return True

        return False

    def execute(self, context: bpy.types.Context):
        self.setup_operator()
        plugin = self.get_plugin()
        logger = self.get_logger()

        logger.info("Refreshing project list...")

        api_client = plugin.get_api_client()

        ################################################################################################################

        method = api_client.get_root_directories

        args = ()

        kwargs = {
            "ignore_cache": True
        }

        running_operation_message = "Refreshing project list..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)


classes = (
    GRIDMARKETS_OT_refresh_project_list,
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

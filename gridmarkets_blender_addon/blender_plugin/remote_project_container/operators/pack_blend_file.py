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

import pathlib

from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.errors import FilePackingError

from gridmarkets_blender_addon.file_packers.blender_file_packer import BlenderFilePacker
from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_pack_blend_file(BaseOperator):
    bl_idname = constants.OPERATOR_PACK_BLEND_FILE_ID_NAME
    bl_label = constants.OPERATOR_PACK_BLEND_FILE_LABEL
    bl_description = constants.OPERATOR_PACK_BLEND_FILE_DESCRIPTION
    bl_options = {'REGISTER'}

    def handle_expected_result(self, result: any) -> bool:

        if type(result) == PackedProject:
            return True

        elif type(result) == FilePackingError:
            msg = "Could not finish packing your project. " + result.user_message
            self.report_and_log({'ERROR'}, msg)
            return True

        return False

    def execute(self, context: bpy.types.Context):
        self.setup_operator()
        plugin = self.get_plugin()
        logger = self.get_logger()

        blend_file = pathlib.Path(plugin.get_user_interface().get_blend_file_path())

        if not blend_file.exists():
            self.report_and_log({'ERROR'}, "File '" + str(blend_file) + "' does not exist")
            return {"FINISHED"}

        if not blend_file.is_file():
            self.report_and_log({'ERROR'}, "Selected .blend file path does not point to a file")
            return {"FINISHED"}

        if blend_file.suffix != constants.BLEND_FILE_EXTENSION:
            self.report_and_log({'ERROR'}, "File does not have a .blend extension")
            return {"FINISHED"}

        export_path = pathlib.Path(plugin.get_user_interface().get_export_path())

        logger.info("Packing blend file '" + str(blend_file) + "' to directory '" + str(export_path) + "'")

        ################################################################################################################

        method = BlenderFilePacker().pack

        args = (
            blend_file,
            export_path
        )

        kwargs = {}

        running_operation_message = "Packing .blend file..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)


classes = (
    GRIDMARKETS_OT_pack_blend_file,
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

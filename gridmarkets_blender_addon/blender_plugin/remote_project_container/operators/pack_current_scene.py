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

from gridmarkets_blender_addon.operators.base_operator import BaseOperator
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_pack_current_scene(BaseOperator):
    bl_idname = constants.OPERATOR_PACK_CURRENT_SCENE_ID_NAME
    bl_label = constants.OPERATOR_PACK_CURRENT_SCENE_LABEL
    bl_description = constants.OPERATOR_PACK_CURRENT_SCENE_DESCRIPTION
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
        user_interface = plugin.get_user_interface()
        logger = self.get_logger()

        if not user_interface.is_render_engine_supported():
            return {'FINISHED'}

        export_path = pathlib.Path(plugin.get_user_interface().get_export_path())

        logger.info("Pack current scene to '" + str(export_path) + "'")

        render_engine = context.scene.render.engine

        ################################################################################################################

        if render_engine == constants.RENDER_ENGINE_CYCLES:
            method = BlenderSceneExporter().export
        else:
            method = VRaySceneExporter().export

        args = (
            export_path,
        )

        kwargs = {}

        running_operation_message = "Packing project..."

        return self.boilerplate_execute(context, method, args, kwargs, running_operation_message)


classes = (
    GRIDMARKETS_OT_pack_current_scene,
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

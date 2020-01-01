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
from queue import Empty

from gridmarkets_blender_addon.meta_plugin.exc_thread import ExcThread
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_project import \
    GRIDMARKETS_OT_upload_project


class GRIDMARKETS_OT_pack_current_scene(bpy.types.Operator):
    bl_idname = constants.OPERATOR_PACK_CURRENT_SCENE_ID_NAME
    bl_label = constants.OPERATOR_PACK_CURRENT_SCENE_LABEL
    bl_description = constants.OPERATOR_PACK_CURRENT_SCENE_DESCRIPTION
    bl_options = {'REGISTER'}

    bucket = None
    timer = None
    thread: ExcThread = None
    plugin = None

    def modal(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject

        if event.type == 'TIMER':
            self.plugin.get_user_interface().increment_running_operation_spinner()
            utils_blender.force_redraw_addon()

            if not self.thread.isAlive():
                try:
                    result = self.bucket.get(block=False)
                except Empty:
                    raise RuntimeError("bucket is Empty")
                else:
                    if type(result) != PackedProject:
                        raise RuntimeError("Method returned unexpected result:", result)

                self.thread.join()
                self.plugin.get_user_interface().set_is_running_operation_flag(False)
                context.window_manager.event_timer_remove(self.timer)
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        user_interface = plugin.get_user_interface()
        log = plugin.get_logging_coordinator().get_logger(self.bl_idname)

        if not user_interface.is_render_engine_supported():
            return {'FINISHED'}

        export_path = pathlib.Path(plugin.get_user_interface().get_export_path())

        args = (
            context.scene.render.engine,
            export_path
        )

        log.info("Pack current scene to '" + str(export_path) + "'")
        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 GRIDMARKETS_OT_pack_current_scene._execute,
                                                                 args,
                                                                 {},
                                                                 "Packing project...")

    @staticmethod
    def _execute(render_engine: str, export_dir: pathlib.Path):
        if render_engine == constants.RENDER_ENGINE_CYCLES:
            packed_project = BlenderSceneExporter().export(export_dir)
        else:
            packed_project = VRaySceneExporter().export(export_dir)

        return packed_project


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

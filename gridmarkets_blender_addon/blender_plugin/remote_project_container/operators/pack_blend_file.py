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
from gridmarkets_blender_addon import constants, utils, utils_blender

from gridmarkets_blender_addon.file_packers.blender_file_packer import BlenderFilePacker

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.upload_project import \
    GRIDMARKETS_OT_upload_project


class GRIDMARKETS_OT_pack_blend_file(bpy.types.Operator):
    bl_idname = constants.OPERATOR_PACK_BLEND_FILE_ID_NAME
    bl_label = constants.OPERATOR_PACK_BLEND_FILE_LABEL
    bl_description = constants.OPERATOR_PACK_BLEND_FILE_DESCRIPTION
    bl_options = {'REGISTER'}

    bucket = None
    timer = None
    thread: ExcThread = None
    plugin = None

    blend_file: bpy.props.StringProperty(
        name="Blend file",
        description="The path to pack your project to",
        subtype='FILE_PATH'
    )

    filepath: bpy.props.StringProperty(
        name="Export Path",
        description="The path to pack your project to",
        subtype='DIR_PATH'
    )

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

    def invoke(self, context, event):
        if self.filepath == None or self.filepath == "":
            self.filepath = utils.get_desktop_path()

        if (self.blend_file == None or self.blend_file == "") and bpy.context.blend_data.is_saved:
            self.blend_file = bpy.context.blend_data.filepath

        return GRIDMARKETS_OT_upload_project.boilerplate_invoke(self, context, event)

    def execute(self, context):

        blend_file = pathlib.Path(self.blend_file)

        if not blend_file.exists():
            self.report({'ERROR'}, "File '" + str(blend_file) + "' does not exist")
            return {"FINISHED"}

        if not blend_file.is_file():
            self.report({'ERROR'}, "Selected .blend file path does not point to a file")
            return {"FINISHED"}

        if blend_file.suffix != constants.BLEND_FILE_EXTENSION:
            self.report({'ERROR'}, "File does not have a .blend extension")
            return {"FINISHED"}

        args = (
            blend_file,
            pathlib.Path(self.filepath)
        )

        return GRIDMARKETS_OT_upload_project.boilerplate_execute(self,
                                                                 context,
                                                                 GRIDMARKETS_OT_pack_blend_file._execute,
                                                                 args,
                                                                 {},
                                                                 "Packing .blend file...")

    @staticmethod
    def _execute(target_file: pathlib.Path, output_dir: pathlib.Path):
        packed_project = BlenderFilePacker().pack(target_file, output_dir)
        return packed_project

    def draw(self, context):
        layout = self.layout

        # blend file
        layout.separator()
        layout.prop(self, 'blend_file')

        row = layout.row()
        row.label(text="The path to to the .blend file you want to pack.")
        row.enabled = False

        # export path
        layout.separator()
        layout.prop(self, 'filepath')

        row = layout.row()
        row.label(text="The path to save your packed scene to.")
        row.enabled = False

        layout.separator()


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

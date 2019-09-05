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
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter
from gridmarkets_blender_addon.project.packed_vray_project import PackedVRayProject
from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

class GRIDMARKETS_OT_submit_vray_project(bpy.types.Operator):
    bl_idname = "gridmarkets.submit_new_vray_project"
    bl_label = "Submit V-Ray Project"
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    def execute(self, context):


        EXPORT_PATH = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

        exporter = VRaySceneExporter()
        exporter.export(EXPORT_PATH)

        packed_project = PackedVRayProject(EXPORT_PATH, EXPORT_PATH / "scene_scene.vrscene")

        utils_blender.submit_new_vray_project(packed_project)

        return {'FINISHED'}


classes = (
    GRIDMARKETS_OT_submit_vray_project,
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

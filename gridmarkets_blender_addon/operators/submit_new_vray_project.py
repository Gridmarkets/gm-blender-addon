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
from gridmarkets_blender_addon import constants, utils_blender, utils
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter
from gridmarkets_blender_addon.project.packed_vray_project import PackedVRayProject

class GRIDMARKETS_OT_submit_vray_project(bpy.types.Operator):
    bl_idname = "gridmarkets.submit_new_vray_project"
    bl_label = "Submit V-Ray Project"
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    project_name : bpy.props.StringProperty(
        name="Project Name",
        description="The name of the job as it will show in the render manager",
        default="",
        maxlen=256
    )

    job_name : bpy.props.StringProperty(
        name="Job Name",
        description="The name of the job as it will show in the render manager",
        default="V-Ray Job",
        maxlen=256
    )

    frame_ranges : bpy.props.StringProperty(
        name="Frame Ranges",
        description="Defines the frame range in format start [end] [step],[start [end] [step]],...",
        default="1 1 1",
        maxlen=256
    )

    output_width : bpy.props.IntProperty(
        name="Output Width",
        description="Defines the render output width",
        default=0,
    )

    output_height : bpy.props.IntProperty(
        name="Output Height",
        description="Defines the render output height",
        default=0,
    )

    output_prefix : bpy.props.StringProperty(
        name="Output Prefix",
        description="Defines the render output file prefix",
        default="",
        maxlen=256
    )

    output_format : bpy.props.StringProperty(
        name="Output Format",
        description="Defines the render output format",
        default="EXR",
        maxlen=256
    )

    output_path : bpy.props.StringProperty(
        name="Output Path",
        description="Defines the path to download the results to",
        default="",
        maxlen=256
    )

    def execute(self, context):

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

        props = context.scene.props
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()

        selected_project = props.project_options

        if selected_project == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            EXPORT_PATH = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

            exporter = VRaySceneExporter()
            exporter.export(EXPORT_PATH)

            packed_project = PackedVRayProject(EXPORT_PATH, EXPORT_PATH / "scene_scene.vrscene")
            packed_project.set_name(self.project_name)

            api_client.submit_new_vray_project(packed_project,
                                               self.job_name,
                                               self.frame_ranges,
                                               self.output_height,
                                               self.output_width,
                                               self.output_prefix,
                                               self.output_format,
                                               pathlib.Path(self.output_path))
        else:
            remote_project = utils_blender.get_selected_project_options(context.scene, context, selected_project)

            api_client.submit_existing_vray_project(remote_project,
                                                    self.job_name,
                                                    self.frame_ranges,
                                                    self.output_height,
                                                    self.output_width,
                                                    self.output_prefix,
                                                    self.output_format,
                                                    pathlib.Path(self.output_path))

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

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

from gridmarkets_blender_addon import api_constants, constants, utils, utils_blender
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts.draw_remote_project_summary import \
    draw_remote_project_summary
from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter
from gridmarkets_blender_addon.scene_exporters.vray_scene_exporter import VRaySceneExporter


class GRIDMARKETS_OT_upload_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_UPLOAD_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PROJECT_LABEL
    bl_icon = constants.ICON_BLEND_FILE
    bl_description = "Upload the current scene as a new project."
    bl_options = {'UNDO'}

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
        default="",
        maxlen=256
    )

    project_type: bpy.props.EnumProperty(
        name="Project Type",
        items=utils_blender.get_supported_products
    )

    blender_280_engine: bpy.props.EnumProperty(
        name="Blender engine",
        items=utils_blender.get_supported_blender_280_engines
    )

    blender_279_engine: bpy.props.EnumProperty(
        name="Blender engine",
        items=utils_blender.get_supported_blender_279_engines
    )

    blender_version: bpy.props.EnumProperty(
        name="Blender version",
        items=utils_blender.get_supported_blender_versions
    )

    vray_version: bpy.props.EnumProperty(
        name="V-Ray version",
        items=utils_blender.get_supported_vray_versions
    )

    project_file: bpy.props.StringProperty(
        name="Project file",
        subtype="FILE_PATH",
        default="<Generated during upload>",
    )

    remap_file: bpy.props.StringProperty(
        name="Re-map file",
        subtype="FILE_PATH",
        default="<Generated during upload>",
        description="The name of the remap file",
    )

    _timer = None
    _thread = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            # repaint add-on on timer event
            utils_blender.force_redraw_addon()

            if not self._thread.isAlive():
                self._thread.join()
                utils_blender.force_redraw_addon()
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        scene = context.scene
        props = scene.props

        # if the file has been saved use the name of the file as the prefix
        if bpy.context.blend_data.is_saved:
            blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)

            if blend_file_name.endswith(constants.BLEND_FILE_EXTENSION):
                blend_file_name = blend_file_name[:-len(constants.BLEND_FILE_EXTENSION)] + "_"

            self.project_name = utils.create_unique_object_name(props.projects, name_prefix=blend_file_name)
        else:
            self.project_name = utils.create_unique_object_name(props.projects, name_prefix=constants.PROJECT_PREFIX)

        if scene.render.engine == "VRAY_RENDER_RT":
            self.project_type = api_constants.PRODUCTS.VRAY
        else:
            self.project_type = api_constants.PRODUCTS.BLENDER

            try:
                self.blender_280_engine = scene.render.engine
            except TypeError:
                self.report({"WARNING"}, scene.render.engine + " is not supported with this product type")
                return {"FINISHED"}
            self.blender_version = api_constants.BLENDER_VERSIONS.V_2_80

        # create popup
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

        temp_dir = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

        if self.project_type == api_constants.PRODUCTS.BLENDER:
            packed_project = BlenderSceneExporter().export(temp_dir)
            packed_project.set_name(self.project_name)

        elif self.project_type == api_constants.PRODUCTS.VRAY:
            packed_project = VRaySceneExporter().export(temp_dir)
            packed_project.set_name(self.project_name)
        else:
            raise RuntimeError("Unknown project type")

        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_client.upload_project(packed_project)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.separator()

        layout.prop(self, "project_name")

        sub = layout.row()
        sub.enabled = False
        sub.prop(self, "project_type")

        if self.project_type == api_constants.PRODUCTS.BLENDER:
            sub = layout.row()
            sub.enabled = False
            sub.prop(self, "blender_version")

            sub = layout.row()
            sub.enabled = False
            sub.prop(self, "project_file")

            sub1 = layout.row()
            sub1.enabled = False

            if self.blender_version == api_constants.BLENDER_VERSIONS.V_2_80:
                sub1.prop(self, "blender_280_engine")
            elif self.blender_version == api_constants.BLENDER_VERSIONS.V_2_79:
                sub1.prop(self, "blender_279_engine")

        elif self.project_type == api_constants.PRODUCTS.VRAY:
            layout.prop(self, "vray_version")

            sub = layout.row()
            sub.enabled = False
            sub.prop(self, "project_file")

            sub = layout.row()
            sub.enabled = False
            sub.prop(self, "remap_file")

        layout.separator()

        draw_remote_project_summary(layout, self.project_name, self.project_type,
                                    self.blender_version, self.project_file, self.blender_280_engine,
                                    self.blender_279_engine,
                                    self.vray_version, self.remap_file)


classes = (
    GRIDMARKETS_OT_upload_project,
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
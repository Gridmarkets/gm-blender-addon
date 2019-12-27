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
from gridmarkets_blender_addon import api_constants, constants, utils, utils_blender
from gridmarkets_blender_addon.project.remote.remote_blender_project import RemoteBlenderProject
from gridmarkets_blender_addon.project.remote.remote_vray_project import RemoteVRayProject
from gridmarkets_blender_addon.blender_plugin.remote_project_container.layouts.draw_remote_project_summary import \
    draw_remote_project_summary


class GRIDMARKETS_OT_add_remote_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_ADD_REMOTE_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_ADD_REMOTE_PROJECT_LABEL
    bl_options = set()

    project_name: bpy.props.StringProperty(
        name="Project Name",
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
        description="The name of your project",
    )

    remap_file: bpy.props.StringProperty(
        name="Re-map file",
        description="The name of the remap file",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        dir = pathlib.Path(self.project_name)

        if self.project_type == api_constants.PRODUCTS.BLENDER:
            main_file = pathlib.Path(self.project_file + constants.BLEND_FILE_EXTENSION)
            remote_project = RemoteBlenderProject(dir, main_file)

        elif self.project_type == api_constants.PRODUCTS.VRAY:
            main_file = pathlib.Path(self.project_file + constants.VRAY_SCENE_FILE_EXTENSION)
            remap_file = dir / pathlib.Path(self.remap_file)
            remote_project = RemoteVRayProject(dir, main_file, remap_file)

        plugin = PluginFetcher.get_plugin()
        plugin.get_remote_project_container().append(remote_project)

        # reset string inputs, enum inputs don't really need to reset to default values
        self.project_name = ""
        self.project_file = ""
        self.remap_file = ""

        utils_blender.force_redraw_addon()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.separator()

        layout.prop(self, "project_name")
        layout.prop(self, "project_type")

        if self.project_type == api_constants.PRODUCTS.BLENDER:
            layout.prop(self, "blender_version")
            layout.prop(self, "project_file")
            project_file = self.project_file + constants.BLEND_FILE_EXTENSION

            if self.blender_version == api_constants.BLENDER_VERSIONS.V_2_80 or self.blender_version == api_constants.BLENDER_VERSIONS.V_2_81A:
                layout.prop(self, "blender_280_engine")
            elif self.blender_version == api_constants.BLENDER_VERSIONS.V_2_79B:
                layout.prop(self, "blender_279_engine")

        elif self.project_type == api_constants.PRODUCTS.VRAY:
            layout.prop(self, "vray_version")
            layout.prop(self, "project_file")
            project_file = self.project_file + constants.VRAY_SCENE_FILE_EXTENSION
            layout.prop(self, "remap_file")

        layout.separator()

        draw_remote_project_summary(layout, self.project_name, self.project_type,
                                    self.blender_version, project_file, self.blender_280_engine,
                                    self.blender_279_engine,
                                    self.vray_version, self.remap_file)


classes = (
    GRIDMARKETS_OT_add_remote_project,
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

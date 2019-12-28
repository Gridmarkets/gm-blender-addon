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


class GRIDMARKETS_MT_project_upload_options(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_project_upload_options"
    bl_label = "Project upload options"

    def draw(self, context):
        from gridmarkets_blender_addon import constants
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.set_project_upload_method import \
            GRIDMARKETS_OT_set_project_upload_method

        layout = self.layout
        plugin = PluginFetcher.get_plugin()
        user_interface = plugin.get_user_interface()

        upload_method = user_interface.get_project_upload_method()

        layout.label(text="Upload Actions:")
        layout.separator()

        def draw_operator_option(layout, upload_method_tuple):
            row = layout.row()
            icon = constants.ICON_RADIOBUT_ON if upload_method == upload_method_tuple[0] else constants.ICON_RADIOBUT_OFF
            row.operator(GRIDMARKETS_OT_set_project_upload_method.bl_idname, text=upload_method_tuple[1],
                         icon=icon).method = upload_method_tuple[0]

            description = layout.row()
            description.label(text=upload_method_tuple[2])
            description.enabled = False

            layout.separator()

        draw_operator_option(layout, constants.UPLOAD_CURRENT_SCENE_TUPLE)
        draw_operator_option(layout, constants.UPLOAD_PROJECT_FILES_TUPLE)

        layout.label(text="Misc Actions:")
        layout.separator()
        draw_operator_option(layout, constants.PACK_CURRENT_SCENE_TUPLE)
        draw_operator_option(layout, constants.UPLOAD_BY_MANUALLY_SPECIFYING_DETAILS_TUPLE)


classes = (
    GRIDMARKETS_MT_project_upload_options,
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

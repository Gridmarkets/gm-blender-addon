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
from gridmarkets_blender_addon import constants


class GRIDMARKETS_OT_toggle_render_engine_view(bpy.types.Operator):

    bl_idname = constants.OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_ID_NAME
    bl_label = constants.OPERATOR_TOGGLE_RENDER_ENGINE_VIEW_LABEL
    bl_options = {'INTERNAL'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        log = PluginFetcher.get_plugin().get_logging_coordinator().get_logger(self.bl_idname)

        props = context.scene.props
        log.info("%s render engine view" % ("Closing" if props.custom_settings_views.render_engine_view else "Opening"))
        props.custom_settings_views.render_engine_view = not props.custom_settings_views.render_engine_view
        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_toggle_render_engine_view,
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

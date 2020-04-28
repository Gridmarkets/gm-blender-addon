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

import typing

from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute


def get_blender_props_for_project_attributes(project_attribute: ProjectAttribute,
                                             properties: typing.Dict[str, bpy.types.Property],
                                             indent: int):

    utils_blender.get_blender_props_for_attribute(project_attribute.get_attribute(),
                                                  properties,
                                                  project_attribute.get_id())

    for child_attribute in project_attribute.get_children():
        get_blender_props_for_project_attributes(child_attribute, properties, indent + 4)


def register_schema(api_client):
    # register Project Attribute props
    api_schema = api_client.get_cached_api_schema()
    root_project_attribute = api_schema.get_root_project_attribute()

    properties = {}
    get_blender_props_for_project_attributes(root_project_attribute, properties, 0)

    # register property group
    GRIDMARKETS_PROPS_project_attributes = type("GRIDMARKETS_PROPS_project_attributes", (bpy.types.PropertyGroup,),
                                                {"__annotations__": properties})

    bpy.utils.register_class(GRIDMARKETS_PROPS_project_attributes)
    setattr(bpy.types.Scene,
            constants.PROJECT_ATTRIBUTES_POINTER_KEY,
            bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_project_attributes))


def close_render_results_image(context):
    # Iterates through every window, screen, area and space to find any image editor spaces that are open and are
    # viewing the blender's render results
    windows = context.window_manager.windows
    for window in windows:
        screen = window.screen
        for area in screen.areas:
            for space in area.spaces:
                if space.type == "IMAGE_EDITOR":
                    # if the image editor is viewing the render results then close the render results
                    if space.image.name == "Render Result":
                        space.image = None


class GRIDMARKETS_OT_open_preferences(bpy.types.Operator):
    bl_idname = constants.OPERATOR_OPEN_ADDON_ID_NAME
    bl_label = constants.OPERATOR_OPEN_ADDON_LABEL
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        log = plugin.get_logging_coordinator().get_logger(self.bl_idname)
        log.info("Opening " + constants.COMPANY_NAME + " add-on preferences menu...")

        for window in context.window_manager.windows:
            screen = window.screen
            if screen.name == constants.INJECTED_SCREEN_NAME:
                # create a new context for the delete and close operations
                c = {"screen": screen, "window": window}

                # close the existing add-on window so that it can be re-opened with focus
                # (no way in blender that I know of to change window focus so I delete and re-open)
                bpy.ops.wm.window_close(c, 'INVOKE_DEFAULT')

                return {'FINISHED'}

        # get the scenes render settings
        render = bpy.context.scene.render

        # save old settings so that they can be restored later
        old_settings = {'x': render.resolution_x,
                        'y': render.resolution_y,
                        'res_percent': render.resolution_percentage}

        # try finally block so that old settings are guaranteed to be restored
        try:
            pixel_size = context.preferences.system.pixel_size

            # Size multiplier to use when drawing custom user interface elements, so that they are scaled correctly on
            # screens with different DPI. This value is based on operating system DPI settings and Blender display scale
            scale_factor = context.preferences.system.ui_scale * pixel_size

            # set the new window settings
            render.resolution_x = constants.DEFAULT_WINDOW_WIDTH * scale_factor
            render.resolution_y = constants.DEFAULT_WINDOW_HIEGHT * scale_factor
            render.resolution_percentage = 100

            # close any render result images as it messes up the opening process
            close_render_results_image(context)

            # Call image editor window. This window just happens to use the render resolution settings for its
            # dimensions.
            bpy.ops.render.view_show("INVOKE_DEFAULT")

            # duplicate this window to create a new window which we can use to hold the add-on. This is necessary
            # because the previous window is a 'special' blender window which will be re-used by other operators, if
            # we were to modify how it worked it could have unintended consequences.
            bpy.ops.screen.area_dupli("INVOKE_DEFAULT")

            # now close the first new window
            bpy.ops.wm.window_close("INVOKE_DEFAULT")

            # get all other windows
            windows = context.window_manager.windows

            # get screen, area, and regions
            window = windows[-1]
            screen = window.screen
            area = screen.areas[0]

            # Change area type to the Preferences editor
            area.type = constants.WINDOW_SPACE_TYPE

            # switch to the add-ons tab
            context.preferences.active_section = 'ADDONS'

            screen.name = constants.INJECTED_SCREEN_NAME

            # flip the header region to the top if on the bottom
            for region in area.regions:
                if region.alignment == "BOTTOM":
                    override = bpy.context.copy()
                    override['window'] = window
                    override['screen'] = screen
                    override['area'] = area
                    override['region'] = region
                    bpy.ops.screen.region_flip(override)

        finally:
            # reset render settings
            render.resolution_x = old_settings['x']
            render.resolution_y = old_settings['y']
            render.resolution_percentage = old_settings['res_percent']

        api_client = plugin.get_api_client()

        if not api_client.is_user_signed_in():
            user_container = plugin.get_preferences_container().get_user_container()
            default_user = user_container.get_default_user()

            if default_user:
                user_container.focus_item(default_user)
                user_container.load_focused_profile()
                bpy.ops.gridmarkets.sign_in_new_user({"screen": screen, "window": window}, "INVOKE_DEFAULT")

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_open_preferences,
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

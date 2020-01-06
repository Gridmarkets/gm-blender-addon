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

import re

from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants


def register_schema(api_client):
    from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
    from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset
    from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps
    from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType, EnumAttributeType, \
        EnumSubtype, StringAttributeType, StringSubtype
    import bpy

    properties = {}

    def register_project_attribute_props(project_attribute: ProjectAttribute, indent):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        id = project_attribute.get_id()

        attribute = project_attribute.get_attribute()
        display_name = attribute.get_display_name()
        description = attribute.get_description()
        attribute_type = attribute.get_type()
        key = attribute.get_key()
        default = attribute.get_default_value()

        if attribute_type == AttributeType.STRING:
            string_attribute: StringAttributeType = attribute
            subtype = string_attribute.get_subtype()

            max_length = string_attribute.get_max_length()

            if subtype == StringSubtype.NONE.value:
                properties[id] = bpy.props.StringProperty(
                    name=display_name,
                    description=description,
                    default=default,
                    maxlen=0 if max_length is None else max_length,
                    options={'SKIP_SAVE'}
                )
            elif subtype == StringSubtype.FRAME_RANGES.value:
                properties[id + JobPreset.FRAME_RANGE_COLLECTION] = bpy.props.CollectionProperty(
                    type=FrameRangeProps,
                    options={'SKIP_SAVE'}
                )

                properties[id + JobPreset.FRAME_RANGE_FOCUSED] = bpy.props.IntProperty(
                    options={'SKIP_SAVE'}
                )
            elif subtype == StringSubtype.FILE_PATH.value:
                properties[id] = bpy.props.StringProperty(
                    name=display_name,
                    description=description,
                    default=default,
                    subtype='FILE_PATH',
                    maxlen=0 if max_length is None else max_length,
                    options={'SKIP_SAVE'}
                )
            else:
                raise ValueError("Unrecognised String subtype '" + subtype + "'.")

        elif attribute_type == AttributeType.ENUM:
            enum_attribute: EnumAttributeType = attribute
            subtype = enum_attribute.get_subtype()
            items = []

            if subtype == EnumSubtype.PRODUCT_VERSIONS.value:
                product = enum_attribute.get_subtype_kwargs().get(
                    api_constants.SUBTYPE_KEYS.STRING.FILE_PATH.PRODUCT)

                match = enum_attribute.get_subtype_kwargs().get(
                    api_constants.SUBTYPE_KEYS.ENUM.PRODUCT_VERSIONS.MATCH)
                match = p = re.compile(match) if match is not None else None

                def _get_product_versions(self, context):
                    versions = plugin.get_api_client().get_product_versions(product)

                    if match is not None:
                        versions = [s for s in versions if p.match(s)]

                    return list(map(lambda version: (version, version, ''), versions))

                items = _get_product_versions
            else:
                enum_items = enum_attribute.get_items()
                for enum_item in enum_items:
                    items.append((enum_item.get_key(), enum_item.get_display_name(), enum_item.get_description()))

            properties[id] = bpy.props.EnumProperty(
                name=display_name,
                description=description,
                items=items,
                default=default,
                options={'SKIP_SAVE'}
            )

        elif attribute_type == AttributeType.BOOLEAN:
            properties[id] = bpy.props.BoolProperty(
                name=display_name,
                description=description,
                default=default,
                options={'SKIP_SAVE'}
            )

        elif attribute_type == AttributeType.INTEGER:
            properties[id] = bpy.props.IntProperty(
                name=display_name,
                description=description,
                default=default,
                options={'SKIP_SAVE'}
            )

        for child_attribute in project_attribute.get_children():
            register_project_attribute_props(child_attribute, indent + 4)

    # register Project Attribute props
    api_schema = api_client.get_api_schema()
    root_project_attribute = api_schema.get_root_project_attribute()

    register_project_attribute_props(root_project_attribute, 0)

    # register property group
    GRIDMARKETS_PROPS_project_attributes = type("GRIDMARKETS_PROPS_project_attributes", (bpy.types.PropertyGroup,),
                                                {"__annotations__": properties})

    bpy.utils.register_class(GRIDMARKETS_PROPS_project_attributes)
    setattr(bpy.types.Scene,
            constants.PROJECT_ATTRIBUTES_POINTER_KEY,
            bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_project_attributes))


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

        register_schema(api_client)

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

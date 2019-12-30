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
import types
from gridmarkets_blender_addon import constants, utils_blender
from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute_types import StringSubtype
from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import \
    RejectedTransitionInputError
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.blender_plugin.project_attribute.project_attribute import \
    get_project_attribute_value, set_project_attribute_value


def _get_remote_root_directories(self, context):
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    api_client = plugin.get_api_client()
    projects = api_client.get_root_directories()

    return list(map(lambda project: (project, project, ''), projects))


class GRIDMARKETS_OT_add_remote_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_ADD_REMOTE_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_ADD_REMOTE_PROJECT_LABEL
    bl_options = set()

    project_name: bpy.props.EnumProperty(
        name="Project Name",
        items=_get_remote_root_directories
    )

    def invoke(self, context, event):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()

        api_client = plugin.get_api_client()

        # refresh projects list
        projects = api_client.get_root_directories(ignore_cache=True)

        # If the user has no projects display a warning message
        if len(projects) == 0:
            self.report({'ERROR'},
                        "No existing projects detected. You must have already uploaded a project to use this option.")
            return {"FINISHED"}

        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()
        root = api_schema.get_root_project_attribute()

        set_project_attribute_value(root, self.project_name)
        files = api_client.get_remote_project_files(self.project_name)

        # validate project
        def _get_project_attributes(project_attribute, attributes=None):

            if attributes is None:
                raise ValueError

            attribute = project_attribute.get_attribute()

            if attribute.get_type() == AttributeType.NULL:
                return attributes

            value = get_project_attribute_value(project_attribute)

            # check file paths exist
            if attribute.get_type() == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FILE_PATH.value:
                if value not in files:
                    self.report({'ERROR'}, "File path '" + str(value) + "' does not exist.")
                    raise ValueError()

            attributes[attribute.get_key()] = value

            return _get_project_attributes(project_attribute.transition(value), attributes)

        try:
            attributes = _get_project_attributes(root, attributes={})
            remote_project = RemoteProject(attributes.get('PROJECT_NAME'),
                                           attributes.get('PRODUCT'),
                                           [],
                                           attributes)

            plugin.get_remote_project_container().append(remote_project)
            utils_blender.force_redraw_addon()
            return {'FINISHED'}

        except ValueError as e:
            return {'FINISHED'}
        except RejectedTransitionInputError as e:
            return {'FINISHED'}

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.attribute.layouts.draw_attribute_input import draw_attribute_input
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_schema = plugin.get_api_client().get_api_schema()
        root = api_schema.get_root_project_attribute()
        layout = self.layout

        layout.separator()

        split = layout.split(factor=0.25)
        col1 = split.column()
        col1.label(text="Project name:")

        col2 = split.column()
        col2.prop(self, "project_name", text="")

        row = layout.row()
        row.label(text=root.get_attribute().get_description())
        row.enabled = False

        layout.separator()

        def draw_project_attribute(project_attribute):
            attribute = project_attribute.get_attribute()

            # Null attributes represet a base case
            if attribute.get_type() == AttributeType.NULL:
                return

            project_props = getattr(context.scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)
            value = get_project_attribute_value(project_attribute)

            split = layout.split(factor=0.25)
            col1 = split.column()
            col1.label(text=attribute.get_display_name())

            col2 = split.column()

            try:
                project_attribute.transition(value)
            except RejectedTransitionInputError as e:
                col2.alert = True

            draw_attribute_input(types.SimpleNamespace(layout=col2), context, project_props, attribute,
                                 prop_id=project_attribute.get_id())

            if len(attribute.get_description()):
                row = layout.row()
                row.label(text=attribute.get_description())
                row.enabled = False

            layout.separator()

            draw_project_attribute(project_attribute.transition(value))

        try:
            product_project_attribute = root.transition(self.project_name)
            draw_project_attribute(product_project_attribute)

        except RejectedTransitionInputError as e:
            layout.separator()
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            row.label(text="Warning: Project settings are invalid. " + e.user_message)
            layout.separator()


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

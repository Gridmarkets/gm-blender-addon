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
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.blender_plugin.project_attribute.project_attribute import \
    get_project_attribute_value, set_project_attribute_value


class GRIDMARKETS_OT_add_remote_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_ADD_REMOTE_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_ADD_REMOTE_PROJECT_LABEL
    bl_options = set()

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()
        api_schema = api_client.get_api_schema()
        root = api_schema.get_root_project_attribute()

        project_name = context.scene.props.remote_project_container.project_name

        # set project name
        set_project_attribute_value(root, project_name)

        # check the project exists
        if project_name not in api_client.get_root_directories(ignore_cache=True):
            self.report({'ERROR'}, "Project '" + project_name + "' no longer exists.")
            return {'FINISHED'}

        # get the files for this project
        envoy_files = api_client.get_remote_project_files(context.scene.props.remote_project_container.project_name)
        files = list(map(lambda x: x.get_key(), envoy_files))

        def _do_file_paths_exist(project_attribute):

            attribute = project_attribute.get_attribute()

            if attribute.get_type() == AttributeType.NULL:
                return True

            value = get_project_attribute_value(project_attribute)

            # check file paths exist
            if attribute.get_type() == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FILE_PATH.value:
                if value not in files:
                    self.report({'ERROR'}, "File path '" + str(value) + "' does not exist under project '" +
                                project_name + "'.")
                    return False

            return _do_file_paths_exist(project_attribute.transition(value))

        # check files actually exist on the remote project
        if not _do_file_paths_exist(root):
            return {'FINISHED'}

        try:
            attributes = utils_blender.get_project_attributes()
            print(attributes)
            remote_project = RemoteProject(attributes.get(api_constants.API_KEYS.PROJECT_NAME),
                                           attributes.get(api_constants.API_KEYS.APP),
                                           [],
                                           attributes)

            plugin.get_remote_project_container().append(remote_project)

            # switch to the projects layout
            plugin.get_user_interface().set_layout(constants.REMOTE_PROJECTS_LAYOUT_VALUE)

            utils_blender.force_redraw_addon()
            return {'FINISHED'}

        except ValueError as e:
            return {'FINISHED'}
        except RejectedTransitionInputError as e:
            return {'FINISHED'}


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

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
from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager


class GRIDMARKETS_MT_add_new_project(bpy.types.Menu):
    bl_idname = "GRIDMARKETS_MT_add_new_project"
    bl_label = "Add new project"

    def draw(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        plugin = PluginFetcher.get_plugin()
        is_running_operation = plugin.get_user_interface().is_running_operation()

        layout = self.layout
        layout.operator_context = 'INVOKE_AREA'

        # draw upload current scene button
        sub = layout.row()
        if is_running_operation:
            sub.enabled = False
        sub.operator(constants.OPERATOR_UPLOAD_PROJECT_ID_NAME, text="Upload current scene as new Project")

        # draw upload file button
        sub = layout.row()
        if is_running_operation:
            sub.enabled = False
        sub.operator(constants.OPERATOR_UPLOAD_FILE_AS_PROJECT_ID_NAME, text="Upload file as new Project")

        # draw manual entree button
        sub = layout.row()
        sub.operator(constants.OPERATOR_ADD_REMOTE_PROJECT_ID_NAME, text="Manually enter details for existing Project")


def _get_value(project_status, key):
    return str(project_status[key]) if key in project_status else 'Value not found'


def _draw_project_detail(keys, values, detail_status):
    keys.label(text="Name: ")
    values.label(text=_get_value(detail_status, "Name"))

    keys.label(text="State: ")
    values.label(text=_get_value(detail_status, "State"))

    keys.label(text="BytesDone: ")
    values.label(text=_get_value(detail_status, "BytesDone"))

    keys.label(text="BytesTotal: ")
    values.label(text=_get_value(detail_status, "BytesTotal"))

    keys.label(text="Speed: ")
    values.label(text=_get_value(detail_status, "Speed"))

    keys.separator()
    values.separator()


def _draw_project_status(col, project):
    # draw label
    sub = col.row()
    sub.label(text="Project status:")

    # draw the get status operator
    op = sub.row()
    op.alignment = 'RIGHT'
    op.operator(constants.OPERATOR_GET_SELECTED_PROJECT_STATUS_ID_NAME, text="Get status")

    if project.status:
        import json
        projects_status = json.loads(project.status)

        split = col.split(factor=0.2)

        keys = split.column()
        values = split.column()

        # draw over all project status information
        keys.label(text="Name: ")
        values.label(text=project.name if project.name else "Name not provided")

        keys.label(text="Code: ")
        values.label(text=_get_value(projects_status, "Code"))

        keys.label(text="State: ")
        values.label(text=_get_value(projects_status, "State"))

        keys.label(text="BytesDone: ")
        values.label(text=_get_value(projects_status, "BytesDone"))

        keys.label(text="BytesTotal: ")
        values.label(text=_get_value(projects_status, "BytesTotal"))

        keys.label(text="Speed: ")
        values.label(text=_get_value(projects_status, "Speed"))

        keys.separator()
        values.separator()

        keys.label(text="Project Assets:")
        values.label(text="")

        # check the details object exists
        if "Details" in projects_status:
            details = projects_status["Details"]

            if details:
                # iterate through each file that needs uploading and display its status
                for detail_name, detail_status in details.items():

                    # don't show the detail object
                    if detail_name == 'details':
                        continue

                    _draw_project_detail(keys, values, detail_status)

        else:
            values.label(text="No project details found")
    else:
        col.label(text="Status not yet fetched")

    sub = col.row(align=True)
    sub.enabled = False
    sub.label(text="Press 'Get status' to re-fetch the status of the project.")


def _draw_project_info_view(self, context):
    layout = self.layout
    props = context.scene.props
    project_count = len(props.projects)
    selected_project_index = props.selected_project

    if project_count > 0 and selected_project_index >= 0 and selected_project_index < project_count:
        project = props.projects[selected_project_index]
        temp_directory_manager = TempDirectoryManager.get_temp_directory_manager()
        association = temp_directory_manager.get_association_with_project_name(project.name)

        box = layout.box()
        col = box.column(align=True)

        col.label(text="Project Info", icon=constants.ICON_PROJECT)
        col.separator()

        col.label(text="Project name: %s" % project.name)
        sub = col.row(align=True)
        sub.enabled = False
        sub.label(text="The name of the project as it will appear in Envoy.")

        col.separator()

        sub = col.row()
        sub.label(text="Temporary directory path: %s" % association.get_temp_dir_name())
        op = sub.row()
        op.alignment = 'RIGHT'
        op.operator(constants.OPERATOR_COPY_TEMPORARY_FILE_LOCATION_ID_NAME, text="Copy Location")
        if association.get_temp_dir_name() == constants.TEMPORARY_FILES_DELETED:
            op.enabled = False

        sub = col.row(align=True)
        sub.enabled = False
        sub.label(text="The temporary directory project files are packed to before uploading. They are automatically "
                       "deleted when blender closes.")

        # don't show the project status view until gs-utils errors with envoy have been fixed
        if constants.PROJECT_STATUS_POLLING_ENABLED:
            col.separator()
            _draw_project_status(col, project)


def draw_projects(self, context):
    layout = self.layout
    props = context.scene.props
    project_count = len(props.projects)

    row = layout.row()
    row.template_list("GRIDMARKETS_UL_project", "", props, "projects", props, "selected_project", rows=2)

    col = row.column()

    sub = col.column(align=True)

    # disable up and down buttons if there are less than 2 projects
    if project_count < 2:
        sub.enabled = False

    sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_UP, text="").action = 'UP'
    sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_TRIA_DOWN,
                 text="").action = 'DOWN'

    row = layout.row(align=True)
    row.menu_contents(GRIDMARKETS_MT_add_new_project.bl_idname)

    sub = row.column()
    if project_count <= 0:
        # disable remove button if there are no projects to remove
        sub.enabled = False
    sub.operator(constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME, icon=constants.ICON_REMOVE, text="Remove Project").action = 'REMOVE'

    _draw_project_info_view(self, context)


classes = (
    GRIDMARKETS_MT_add_new_project,
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

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
import threading
from gridmarkets_blender_addon import constants, utils, utils_blender
from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager

from gridmarkets_blender_addon.blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_Submit(bpy.types.Operator):
    """Class to represent the 'Submit' operation."""

    bl_idname = constants.OPERATOR_SUBMIT_ID_NAME
    bl_label = constants.OPERATOR_SUBMIT_LABEL

    _timer = None
    _thread = None

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
        default="",
        maxlen=256
    )

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
        props = context.scene.props

        # only show project name pop up dialog if submitting a new project
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            # if the file has been saved use the name of the file as the prefix
            if bpy.context.blend_data.is_saved:
                blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)

                if blend_file_name.endswith(constants.BLEND_FILE_EXTENSION):
                    blend_file_name = blend_file_name[:-len(constants.BLEND_FILE_EXTENSION)] + "_"

                self.project_name = utils.create_unique_object_name(props.projects, name_prefix=blend_file_name)
            else:
                self.project_name = utils.create_unique_object_name(props.projects, name_prefix=constants.PROJECT_PREFIX)

            # create popup
            return context.window_manager.invoke_props_dialog(self, width=400)
        else:
            return self.execute(context)

    def execute(self, context):
        from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
        from gridmarkets_blender_addon.temp_directory_manager import TempDirectoryManager
        from gridmarkets_blender_addon.scene_exporters.blender_scene_exporter import BlenderSceneExporter

        props = context.scene.props
        plugin = PluginFetcher.get_plugin()
        api_client = plugin.get_api_client()

        selected_project = props.project_options

        if selected_project == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            temp_dir = TempDirectoryManager.get_temp_directory_manager().get_temp_directory()

            packed_project = BlenderSceneExporter().export(temp_dir)
            packed_project.set_name(self.project_name)

            api_client.submit_new_blender_project(packed_project)
        else:
            remote_project_container = plugin.get_remote_project_container()
            remote_project = remote_project_container.get_project_with_id(selected_project)
            api_client.submit_existing_blender_project(remote_project)


        return {"FINISHED"}
        """
        wm = context.window_manager

        log.info("Creating separate thread for submission process")

        # run the upload project function in separate thread so that gui is not blocked
        self._thread = threading.Thread(target=utils_blender.submit_job,
                                        args=(context, TempDirectoryManager.get_temp_directory_manager()),
                                        kwargs={'new_project_name': self.project_name, 'operator': self})
        self._thread.start()
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        """


classes = (
    GRIDMARKETS_OT_Submit,
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

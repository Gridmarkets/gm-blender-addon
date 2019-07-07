import bpy
import constants
import threading
import utils
import utils_blender
from temp_directory_manager import TempDirectoryManager

from blender_logging_wrapper import get_wrapped_logger
log = get_wrapped_logger(__name__)


class GRIDMARKETS_OT_upload_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_UPLOAD_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PROJECT_LABEL
    bl_icon = constants.ICON_BLEND_FILE
    bl_options = {'UNDO'}

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
        default="",
        maxlen=256
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
        props = context.scene.props

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

    def execute(self, context):
        """ Called after the user clicks the 'ok' button on the popup """
        wm = context.window_manager

        # run the upload project function in separate thread so that gui is not blocked
        self._thread = threading.Thread(target=utils_blender.upload_project,
                                        args=(context, self.project_name, TempDirectoryManager.get_temp_directory_manager()),
                                        kwargs={'operator': self})
        self._thread.start()
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout

        # project name prop
        layout.prop(self, "project_name")


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

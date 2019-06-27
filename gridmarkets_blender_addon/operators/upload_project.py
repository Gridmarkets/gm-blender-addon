import bpy
import constants
import utils
import utils_blender
from gridmarkets.errors import *
from invalid_input_error import InvalidInputError
from temp_directory_manager import TempDirectoryManager


class GRIDMARKETS_OT_upload_project(bpy.types.Operator):
    bl_idname = constants.OPERATOR_UPLOAD_PROJECT_ID_NAME
    bl_label = constants.OPERATOR_UPLOAD_PROJECT_LABEL
    bl_icon = 'BLEND_FILE'
    bl_options = {'UNDO'}

    # getters, setters and properties are all copied from <properties.FrameRangeProps>
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of your project",
        default="",
        maxlen=256
    )

    def invoke(self, context, event):
        props = context.scene.props

        # if the file has been saved use the name of the file as the prefix
        if bpy.context.blend_data.is_saved:
            blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)

            print("blend_file_name", blend_file_name)

            if blend_file_name.endswith(constants.BLEND_FILE_EXTENSION):
                print("blend_file_name", blend_file_name)
                blend_file_name = blend_file_name[:-len(constants.BLEND_FILE_EXTENSION)] + "_"

            print("blend_file_name", blend_file_name)

            self.project_name = utils.create_unique_object_name(props.projects, name_prefix=blend_file_name)
        else:
            self.project_name = utils.create_unique_object_name(props.projects, name_prefix=constants.PROJECT_PREFIX)

        # create popup
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        """ Called after the user clicks the 'ok' button on the popup """
        scene = context.scene
        props = scene.props

        try:
            utils_blender.upload_project(self.project_name, TempDirectoryManager.get_temp_directory_manager())
            self._add_project_to_list(props)

        except InvalidInputError as e:
            self.report({'ERROR_INVALID_INPUT'}, e.user_message())
        except AuthenticationError as e:
            self.report({'ERROR'}, "Authentication Error: " + e.user_message)
        except InsufficientCreditsError as e:
            self.report({'ERROR'}, "Insufficient Credits Error: " + e.user_message)
        except InvalidRequestError as e:
            self.report({'ERROR'}, "Invalid Request Error: " + e.user_message)
        except APIError as e:
            self.report({'ERROR'}, "API Error: " + str(e.user_message))

        return {'FINISHED'}

    def _add_project_to_list(self, props):

        # add a project to the list
        project = props.projects.add()

        project.id = utils.get_unique_id(props.projects)
        project.name = self.project_name

        # select the new project
        props.selected_project = len(props.projects) - 1

        # force region to redraw otherwise the list wont update until next event (mouse over, etc)
        for area in bpy.context.screen.areas:
            if area.type == constants.PANEL_SPACE_TYPE:
                for region in area.regions:
                    if region.type == constants.PANEL_REGION_TYPE:
                        region.tag_redraw()

    def draw(self, context):
        layout = self.layout

        # project name
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

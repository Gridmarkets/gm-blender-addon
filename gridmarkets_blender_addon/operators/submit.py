import bpy
import constants
import utils_blender
from gridmarkets.errors import *
from invalid_input_error import InvalidInputError
from temp_directory_manager import TempDirectoryManager


class GRIDMARKETS_OT_Submit(bpy.types.Operator):
    """Class to represent the 'Submit' operation."""

    bl_idname = constants.OPERATOR_SUBMIT_ID_NAME
    bl_label = constants.OPERATOR_SUBMIT_LABEL

    def execute(self, context):
        try:
            utils_blender.submit_job(context, TempDirectoryManager.get_temp_directory_manager())
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
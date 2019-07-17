import bpy
import constants

class GRIDMARKETS_OT_project_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the project list menu """

    bl_idname = constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_PROJECT_LIST_ACTIONS_LABEL

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('UPLOAD', "Upload", ""),
            ('UPLOAD_FILE', "Upload File", "")
        )
    )

    def invoke(self, context, event):
        props = context.scene.props
        index = props.selected_project

        # if the currently selected project does not exist then the only allowed action is 'ADD'
        try:
            item = props.projects[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(props.projects) - 1:
                props.selected_project += 1

            elif self.action == 'UP' and index >= 1:
                props.selected_project -= 1

            elif self.action == 'REMOVE':
                # the static default options value's are not necessarily a number
                if props.project_options.isnumeric():
                    selected_project_option = int(props.project_options)

                    # reset the pulldown list if the selected option is going to be deleted
                    if selected_project_option == index + constants.PROJECT_OPTIONS_STATIC_COUNT:
                        props.property_unset("project_options")

                props.projects.remove(index)

                # select the previous project if the selected project isn't already the first in the list
                if props.selected_project > 0:
                    props.selected_project -= 1

        if self.action == 'UPLOAD':
            bpy.ops.gridmarkets.upload_project('INVOKE_DEFAULT')

        if self.action == 'UPLOAD_FILE':
            bpy.ops.gridmarkets.upload_file_as_project('INVOKE_DEFAULT')

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_project_list_actions,
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

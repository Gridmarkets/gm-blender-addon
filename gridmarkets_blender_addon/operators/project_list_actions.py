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

class GRIDMARKETS_OT_project_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the project list menu """

    bl_idname = constants.OPERATOR_PROJECT_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_PROJECT_LIST_ACTIONS_LABEL

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", "")
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

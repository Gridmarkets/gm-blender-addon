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
from gridmarkets_blender_addon import constants, utils


class GRIDMARKETS_OT_frame_range_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the frame range list menu """

    bl_idname = constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_VRAY_FRAME_RANGE_LIST_ACTIONS_LABEL

    action : bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('EDIT', "Edit", "")
        )
    )

    def invoke(self, context, event):
        props = context.scene.props

        vray = props.vray
        index = vray.selected_frame_range

        # if the currently selected frame_range does not exist then the only allowed action is 'ADD'
        try:
            item = vray.frame_ranges[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(vray.frame_ranges) - 1:
                vray.selected_frame_range += 1

            elif self.action == 'UP' and index >= 1:
                vray.selected_frame_range -= 1

            elif self.action == 'REMOVE':
                # never remove the last frame range
                if len(vray.frame_ranges) < 2:
                    return {"FINISHED"}

                vray.frame_ranges.remove(index)

                if vray.selected_frame_range > 0:
                    vray.selected_frame_range -= 1

            elif self.action == 'EDIT':
                bpy.ops.gridmarkets.edit_vray_frame_range('INVOKE_DEFAULT')

        if self.action == 'ADD':

            # add a frame range to the list
            frame_range = vray.frame_ranges.add()

            frame_range.name = utils.create_unique_object_name(vray.frame_ranges, name_prefix=constants.FRAME_RANGE_PREFIX)
            frame_range.enabled = True
            frame_range.frame_start = constants.DEFAULT_FRAME_RANGE_START_VALUE
            frame_range.frame_end = constants.DEFAULT_FRAME_RANGE_END_VALUE
            frame_range.frame_step = constants.DEFAULT_FRAME_RANGE_STEP_VALUE

            vray.selected_frame_range = len(vray.frame_ranges) - 1

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_frame_range_list_actions,
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

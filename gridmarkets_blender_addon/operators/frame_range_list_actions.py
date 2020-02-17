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
from gridmarkets_blender_addon.meta_plugin import utils
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps


class GRIDMARKETS_OT_frame_range_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the frame range list menu """

    bl_idname = constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_LABEL

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", ""),
            ('EDIT', "Edit", "")
        )
    )

    property_group_attribute: bpy.props.StringProperty()
    focused_item_attribute: bpy.props.StringProperty()
    collection_attribute: bpy.props.StringProperty()

    def invoke(self, context, event):
        from gridmarkets_blender_addon.meta_plugin.utils import get_deep_attribute

        property_group = get_deep_attribute(bpy.context.scene, self.property_group_attribute)
        focused_item = getattr(property_group, self.focused_item_attribute)
        collection = getattr(property_group, self.collection_attribute)

        def set_focused_item(value: int):
            setattr(property_group, self.focused_item_attribute, value)

        # if the currently selected frame_range does not exist then the only allowed action is 'ADD'
        try:
            item = collection[focused_item]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and focused_item < len(collection) - 1:
                set_focused_item(focused_item + 1)

            elif self.action == 'UP' and focused_item >= 1:
                set_focused_item(focused_item - 1)

            elif self.action == 'REMOVE':
                # never remove the last frame range
                if len(collection) < 2:
                    return {"FINISHED"}

                collection.remove(focused_item)

                # if the collection only has one item after the removal, make sure that item is enabled
                if len(collection) == 1:
                    collection[0].enabled = True

                if focused_item > 0:
                    set_focused_item(focused_item - 1)

            elif self.action == 'EDIT':
                bpy.ops.gridmarkets.edit_frame_range('INVOKE_DEFAULT',
                                                     property_group_attribute=self.property_group_attribute,
                                                     focused_item_attribute=self.focused_item_attribute,
                                                     collection_attribute=self.collection_attribute)

        if self.action == 'ADD':
            # add a frame range to the list
            frame_range = collection.add()

            frame_range.name = utils.create_unique_object_name(collection, name_prefix=constants.FRAME_RANGE_PREFIX)
            frame_range.enabled = True
            frame_range.frame_start = constants.DEFAULT_FRAME_RANGE_START_VALUE
            frame_range.frame_end = constants.DEFAULT_FRAME_RANGE_END_VALUE
            frame_range.frame_step = constants.DEFAULT_FRAME_RANGE_STEP_VALUE

            set_focused_item(len(collection) - 1)

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

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

__all__ = ['draw_project_attribute']

import bpy
import types

from gridmarkets_blender_addon import constants
from ..project_attribute import get_project_attribute_value
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType
from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import RejectedTransitionInputError
from gridmarkets_blender_addon.blender_plugin.attribute.layouts.draw_attribute_input import draw_attribute_input


def draw_project_attribute(layout: bpy.types.UILayout,
                           context: bpy.types.Context,
                           project_attribute: ProjectAttribute,
                           draw_linked_attributes=True,
                           encountered_transition_error=False) -> bool:
    """
    :return: Returns False if no transition error was encountered otherwise returns True
    :rtype: bool
    """

    attribute = project_attribute.get_attribute()

    # Null attributes represent a base case
    if attribute.get_type() == AttributeType.NULL:
        return encountered_transition_error

    project_props = getattr(context.scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)
    value = get_project_attribute_value(project_attribute)

    split = layout.split(factor=constants.PROJECT_ATTRIBUTE_SPLIT_FACTOR)
    col1 = split.column(align=True)
    col1.label(text=attribute.get_display_name())
    col2 = split.column(align=True)

    try:
        # attempt to get the next project attribute
        next_project_attribute = project_attribute.transition(value)
        transition_error_message = None

    except RejectedTransitionInputError as e:
        # if there is a transition error set alert to True so that blender renders the current input in red
        col2.alert = True
        transition_error_message = e.user_message

        # if it is possible to force the transition, then do so and continue as normal
        try:
            next_project_attribute = project_attribute.transition(value, force_transition=True)
            encountered_transition_error = True
        except RejectedTransitionInputError as e:
            # otherwise it is not possible to know which project attribute to render next so we must raise the error
            return True

    draw_attribute_input(types.SimpleNamespace(layout=col2),
                         context,
                         project_props,
                         attribute,
                         prop_id=project_attribute.get_id())

    # draw attribute description
    if attribute.get_description():
        description_layout = col2.row()
        description_layout.label(text=attribute.get_description())
        description_layout.enabled = False

    # draw transition error message
    if transition_error_message:
        col2.label(text=transition_error_message)

    if next_project_attribute and draw_linked_attributes:
        return draw_project_attribute(layout, context, next_project_attribute,
                                      encountered_transition_error=encountered_transition_error)

    return encountered_transition_error

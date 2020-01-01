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


def draw_project_attribute(layout: bpy.types.UILayout,
                           context: bpy.types.Context,
                           project_attribute: ProjectAttribute):

    from gridmarkets_blender_addon.blender_plugin.attribute.layouts.draw_attribute_input import draw_attribute_input

    attribute = project_attribute.get_attribute()

    # Null attributes represet a base case
    if attribute.get_type() == AttributeType.NULL:
        return

    project_props = getattr(context.scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)
    value = get_project_attribute_value(project_attribute)

    split = layout.split(factor=0.2)

    col1 = split.column(align=True)
    col1.label(text=attribute.get_display_name())

    col2 = split.column(align=True)

    try:
        project_attribute.transition(value)
    except RejectedTransitionInputError as e:
        col2.alert = True

    draw_attribute_input(types.SimpleNamespace(layout=col2), context, project_props, attribute,
                         prop_id=project_attribute.get_id())

    if len(attribute.get_description()):
        row = col2.row()
        row.label(text=attribute.get_description())
        row.enabled = False

    draw_project_attribute(layout, context, project_attribute.transition(value))

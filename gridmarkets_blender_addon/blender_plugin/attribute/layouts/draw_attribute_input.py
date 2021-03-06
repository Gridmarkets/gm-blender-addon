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
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants as api_constants
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute

from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.refresh_project_list import \
    GRIDMARKETS_OT_refresh_project_list
from gridmarkets_blender_addon.blender_plugin.remote_project_container.operators.refresh_project_file_list import \
    GRIDMARKETS_OT_refresh_project_file_list


def draw_attribute_input(self, context, prop_container, attribute: Attribute, prop_id: str = None,
                         remote_source: bool = False):
    from types import SimpleNamespace
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
    from gridmarkets_blender_addon.meta_plugin.attribute_types import StringAttributeType, StringSubtype, IntegerSubtype
    from gridmarkets_blender_addon.layouts.draw_frame_range_container import draw_frame_range_container
    from gridmarkets_blender_addon.blender_plugin.attribute.attribute import get_value
    from gridmarkets_blender_addon.meta_plugin.errors.invalid_attribute_error import InvalidAttributeError

    attribute_type = attribute.get_type()

    # don't draw null attributes
    if attribute_type == AttributeType.NULL:
        return

    layout: bpy.types.UILayout = self.layout
    col = layout.column()

    # use the attribute key as the prop id by default unless one was provided
    prop_id = attribute.get_key() if prop_id is None else prop_id

    # some attributes require a different input if using a remote source
    if remote_source:
        if (attribute_type == AttributeType.STRING and
            attribute.get_subtype() == StringSubtype.PATH.value and
            attribute.get_subtype_kwargs().get(api_constants.SUBTYPE_KEYS.STRING.PATH.FILE_MODE) == api_constants.SUBTYPE_KEYS.STRING.PATH.FILE_PATH) or \
                (attribute.get_key() == api_constants.API_KEYS.PROJECT_NAME and attribute_type == AttributeType.STRING):

            prop_id = prop_id + constants.REMOTE_SOURCE_SUFFIX

    # validate user input
    attribute_value = get_value(prop_container, attribute, prop_id)

    validation_message = None
    try:
        attribute.validate_value(attribute_value)
    except InvalidAttributeError as e:
        validation_message = e.user_message

        # set alert to true if input is invalid
        col.alert = True

    if attribute_type == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FRAME_RANGES.value:
        draw_frame_range_container(SimpleNamespace(layout=col),
                                   context,
                                   prop_container,
                                   prop_id + '_collection',
                                   prop_id + '_focused')

    elif attribute_type == AttributeType.INTEGER and attribute.get_subtype() == IntegerSubtype.INSTANCES.value:
        row = col.row(align=True)

        # only show the value input prop if not using the default value
        use_default_machine_count = getattr(prop_container, prop_id + constants.INSTANCES_SUBTYPE_PROPERTY_USE_DEFAULT)
        if use_default_machine_count:
            row2 = row.row(align=True)
            row2.label(text="Use default machine count")
            row2.enabled = False
            row.prop(prop_container, prop_id + constants.INSTANCES_SUBTYPE_PROPERTY_USE_DEFAULT, text="")
        else:
            row.prop(prop_container, prop_id, text="")
            row.prop(prop_container, prop_id + constants.INSTANCES_SUBTYPE_PROPERTY_USE_DEFAULT, text="")

    elif remote_source and attribute_type == AttributeType.STRING and \
            attribute.get_subtype() == StringSubtype.PATH.value and \
            attribute.get_subtype_kwargs().get(api_constants.SUBTYPE_KEYS.STRING.PATH.FILE_MODE) == api_constants.SUBTYPE_KEYS.STRING.PATH.FILE_PATH:
        row = col.row(align=True)
        row.prop(prop_container, prop_id, text="")
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.operator(GRIDMARKETS_OT_refresh_project_file_list.bl_idname, text="refresh")

    elif remote_source and attribute.get_key() == api_constants.API_KEYS.PROJECT_NAME and attribute_type == AttributeType.STRING:
        row = col.row(align=True)
        row.prop(prop_container, prop_id, text="")
        sub = row.row(align=True)
        sub.alignment = "RIGHT"
        sub.operator(GRIDMARKETS_OT_refresh_project_list.bl_idname, text="refresh")
    else:
        col.prop(prop_container, prop_id, text="")

    # display validation message
    if validation_message:
        col.label(text=validation_message.capitalize())

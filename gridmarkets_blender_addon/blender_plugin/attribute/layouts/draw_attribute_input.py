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

from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute


def draw_attribute_input(self, context, prop_container, attribute: Attribute, prop_id: str = None,
                         remote_source: bool = False):

    from types import SimpleNamespace
    from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
    from gridmarkets_blender_addon.meta_plugin.attribute_types import StringAttributeType, StringSubtype
    from gridmarkets_blender_addon.layouts.draw_frame_range_container import draw_frame_range_container
    from gridmarkets_blender_addon.blender_plugin.attribute.attribute import get_value
    from gridmarkets_blender_addon.meta_plugin.errors.invalid_attribute_error import InvalidAttributeError

    attribute_type = attribute.get_type()

    # don't draw null attributes
    if attribute_type == AttributeType.NULL:
        return

    layout = self.layout
    col = layout.column()

    # use the attribute key as the prop id by default unless one was provided
    prop_id = attribute.get_key() if prop_id is None else prop_id

    # some attributes require a different input if using a remote source
    if remote_source:
        if attribute_type == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FILE_PATH.value:
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
    else:
        col.prop(prop_container, prop_id, text="")

    # display validation message
    if validation_message:
        col.label(text=validation_message.capitalize())

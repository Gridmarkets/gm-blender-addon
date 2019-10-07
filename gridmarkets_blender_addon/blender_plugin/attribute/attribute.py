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

from gridmarkets_blender_addon.meta_plugin.attribute import Attribute


def get_default_value(attribute: Attribute) -> any:
    from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType

    attribute_type: AttributeType = attribute.get_type()

    if attribute_type == AttributeType.ENUM:
        return attribute.get_default_value().get_key()

    if attribute_type == AttributeType.NULL:
        return None

    return attribute.get_default_value()
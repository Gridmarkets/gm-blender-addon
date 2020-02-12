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

import typing
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute
from gridmarkets_blender_addon import constants


def get_value(property_group, attribute: Attribute, prop_id: str = None) -> any:
    from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType, StringSubtype, IntegerSubtype
    from gridmarkets_blender_addon.blender_plugin.job_preset.job_preset import JobPreset
    from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps

    # use the attribute key as the prop id by default unless one was provided
    prop_id = attribute.get_key() if prop_id is None else prop_id

    attribute_type = attribute.get_type()

    if attribute_type == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FRAME_RANGES.value:
        frame_ranges: typing.List[FrameRangeProps] = getattr(property_group,
                                                             prop_id + JobPreset.FRAME_RANGE_COLLECTION)

        def serialise_frame_range(frame_range: FrameRangeProps):
            start = str(frame_range.frame_start)
            end = str(frame_range.frame_end)
            step = str(frame_range.frame_step)

            return start + ' ' + end + ' ' + step

        serialised_ranges = map(serialise_frame_range, frame_ranges)
        return ','.join(serialised_ranges)

    if attribute_type == AttributeType.INTEGER and attribute.get_subtype() == IntegerSubtype.INSTANCES.value:

        use_default_machine_count = getattr(property_group, prop_id + constants.INSTANCES_SUBTYPE_PROPERTY_USE_DEFAULT)
        machine_count_value = getattr(property_group, prop_id)

        if use_default_machine_count:
            return 0
        else:
            return machine_count_value

    return getattr(property_group, prop_id)

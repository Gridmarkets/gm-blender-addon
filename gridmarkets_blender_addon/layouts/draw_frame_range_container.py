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


def draw_frame_range_container(self, context, property_group, collection: str, focused_item_attr: str):
    import bpy
    from gridmarkets_blender_addon.meta_plugin.utils import get_deep_attribute
    from gridmarkets_blender_addon import constants, utils_blender

    layout = self.layout.column()
    props = context.scene.props

    frame_ranges = getattr(property_group, collection)
    focused_item = getattr(property_group, focused_item_attr)
    frame_range_count = len(frame_ranges)

    row = layout.row()
    row.template_list("GRIDMARKETS_UL_frame_range", "", property_group, collection, property_group,
                      focused_item_attr, rows=5)

    col = row.column()

    def draw_operator(element, action, icon):
        op = element.operator(constants.OPERATOR_FRAME_RANGE_LIST_ACTIONS_ID_NAME, icon=icon, text="")
        op.action = action
        op.property_group_attribute = property_group.path_from_id()
        op.focused_item_attribute = focused_item_attr
        op.collection_attribute = collection

    sub = col.column(align=True)
    draw_operator(sub, 'EDIT', constants.ICON_MODIFIER)

    sub = col.column(align=True)
    draw_operator(sub, 'ADD', constants.ICON_ADD)

    remove = sub.row()
    # prevent the user removing the last frame range for a job
    if frame_range_count < 2:
        remove.enabled = False
    draw_operator(remove, 'REMOVE', constants.ICON_REMOVE)

    sub = col.column(align=True)

    # disable up / down buttons if only one frame range
    if frame_range_count < 2:
        sub.enabled = False

    draw_operator(sub, 'UP', constants.ICON_TRIA_UP)
    draw_operator(sub, 'DOWN', constants.ICON_TRIA_DOWN)

    # display warning if overlapping frame ranges
    if utils_blender.do_frame_ranges_overlap(frame_ranges):
        sub = layout.row()
        sub.enabled = False
        sub.label(text="Warning: frame ranges overlap. You may be charged for overlapping frames but will "
                       "receive only one output frame for each conflict.", icon=constants.ICON_ERROR)

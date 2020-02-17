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
import typing

from gridmarkets_blender_addon.meta_plugin import utils
from gridmarkets_blender_addon.meta_plugin.log_history_container import LogHistoryContainer as MetaLogHistoryContainer
from gridmarkets_blender_addon.meta_plugin.log_item import LogItem
from gridmarkets_blender_addon import utils_blender

if typing.TYPE_CHECKING:
    from gridmarkets_blender_addon.blender_plugin.plugin.plugin import Plugin


class LogHistoryContainer(MetaLogHistoryContainer):

    def __init__(self, plugin: 'Plugin'):
        MetaLogHistoryContainer.__init__(self, plugin, [])

    def focus_item(self, log_item: LogItem, clear_selection=True, update_props: bool = True) -> None:

        if update_props:
            try:
                index = self.get_index(log_item)

                if index:
                    bpy.context.scene.props.log_history_container.focused_log_item = index

                utils_blender.force_redraw_addon()
            except AttributeError:
                pass

        MetaLogHistoryContainer.focus_item(self, log_item, clear_selection)

    def append(self, log_item: LogItem, focus_new_item: bool = True, update_props: bool = True) -> None:

        message_lines = log_item.get_message().splitlines()

        # report each line individually because blender has problems with multi-line reports (They display backwards in
        # the info panel)
        for message_line in message_lines:
            # replace tabs since the blender info console can not display them
            message_line = message_line.replace('\t', ' ' * 4)

            sub_item = LogItem(log_item.get_logger_name(),
                               log_item.get_level(),
                               log_item.get_date_time(),
                               message_line)

            if update_props:
                try:
                    log_history_items = bpy.context.scene.props.log_history_container.log_history_items
                    log_history_item_props = log_history_items.add()
                    log_history_item_props.id = utils.get_unique_id(log_history_items)
                    utils_blender.force_redraw_addon()
                except AttributeError:
                    pass


            MetaLogHistoryContainer.append(self, sub_item, focus_new_item=focus_new_item)

    def remove(self, log_item: LogItem, update_props: bool = True) -> None:

        if update_props:
            try:
                index = self._items.index(log_item)
                log_history_items = bpy.context.scene.props.log_history_container.log_history_items
                log_history_items.remove(index)
                utils_blender.force_redraw_addon()
            except AttributeError:
                pass

        MetaLogHistoryContainer.remove(self, log_item)

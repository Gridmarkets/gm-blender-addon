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

from gridmarkets_blender_addon.meta_plugin.job_preset import JobPreset
from gridmarkets_blender_addon.meta_plugin.job_preset_container import JobPresetContainer as MetaJobPresetContainer
from gridmarkets_blender_addon.blender_plugin.decorators.attach_blender_plugin import attach_blender_plugin
from gridmarkets_blender_addon import utils_blender


@attach_blender_plugin
class JobPresetContainer(MetaJobPresetContainer):

    def __init__(self):
        MetaJobPresetContainer.__init__(self, [])

    def focus_item(self, item: JobPreset, clear_selection=True, update_props: bool = True) -> None:

        if update_props:
            index = self.get_index(item)

            if index:
                bpy.context.scene.props.job_preset_container.focused_item = index

            utils_blender.force_redraw_addon()

        MetaJobPresetContainer.focus_item(self, item, clear_selection)

    def append(self, item: JobPreset, focus_new_item: bool = True, update_props: bool = True) -> None:

        if update_props:
            from gridmarkets_blender_addon import utils

            job_preset_items = bpy.context.scene.props.job_preset_container.items
            list_id = utils.get_unique_id(job_preset_items)

            job_preset_item = job_preset_items.add()
            job_preset_item.unique_identifier = item.get_id()
            job_preset_item.id = list_id
            job_preset_item.name = item.get_name()

            utils_blender.force_redraw_addon()

        MetaJobPresetContainer.append(self, item, focus_new_item=focus_new_item)

    def remove(self, item: JobPreset, update_props: bool = True) -> None:

        if update_props:
            index = self._items.index(item)
            job_preset_items = bpy.context.scene.props.job_preset_container.items
            job_preset_items.remove(index)

            utils_blender.force_redraw_addon()

        MetaJobPresetContainer.remove(self, item)

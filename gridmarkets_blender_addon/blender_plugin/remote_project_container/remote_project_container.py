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

from gridmarkets_blender_addon.meta_plugin.remote_project_container import RemoteProjectContainer as \
    MetaRemoteProjectContainer
from gridmarkets_blender_addon.blender_plugin.decorators.attach_blender_plugin import attach_blender_plugin
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject


@attach_blender_plugin
class RemoteProjectContainer(MetaRemoteProjectContainer):

    def __init__(self):
        MetaRemoteProjectContainer.__init__(self, [])

    def focus_item(self, item: RemoteProject, clear_selection=True, update_props: bool = True) -> None:

        if update_props:
            index = self.get_index(item)

            if index:
                bpy.context.scene.props.remote_project_container.focused_remote_project = index

        MetaRemoteProjectContainer.focus_item(self, item, clear_selection)

    def append(self, item: RemoteProject, focus_new_item: bool = True, update_props: bool = True) -> None:

        if update_props:
            from gridmarkets_blender_addon import utils

            remote_projects = bpy.context.scene.props.remote_project_container.remote_projects
            remote_project_props = remote_projects.add()
            remote_project_props.id = utils.get_unique_id(remote_projects)

        MetaRemoteProjectContainer.append(self, item, focus_new_item=focus_new_item)

    def remove(self, item: RemoteProject, update_props: bool = True) -> None:

        if update_props:
            index = self._items.index(item)
            remote_projects = bpy.context.scene.props.remote_project_container.remote_projects
            remote_projects.remove(index)

        MetaRemoteProjectContainer.remove(self, item)

    def get_project_id(self, remote_project: RemoteProject):
        index = self.get_index(remote_project)
        return bpy.context.scene.props.remote_project_container.remote_projects[index].id

    def get_project_with_id(self, id: int):
        remote_projects = bpy.context.scene.props.remote_project_container.remote_projects

        if type(id) == str:
            id = int(id)

        for i, remote_project in enumerate(remote_projects):
            if remote_project.id == id:
                return self.get_at(i)

        raise ValueError("no remote project with id: " + str(id))

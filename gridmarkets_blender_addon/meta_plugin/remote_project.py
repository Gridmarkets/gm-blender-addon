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

__all__ = 'RemoteProject', 'convert_packed_project'

from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute_types import StringSubtype

from gridmarkets_blender_addon.meta_plugin.project import Project
import pathlib
import typing

if typing.TYPE_CHECKING:
    from .plugin import Plugin
    from .packed_project import PackedProject


class RemoteProject(Project):

    def __init__(self,
                 name: str,
                 root_dir: pathlib.Path,
                 files: typing.Set[pathlib.Path],
                 attributes: typing.Dict[str, any]):
        Project.__init__(self,
                         name,
                         root_dir,
                         files,
                         attributes)

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def exists(self) -> bool:
        raise NotImplementedError

    def delete(self) -> None:
        raise NotImplementedError

    def get_size(self) -> int:
        raise NotImplementedError


def convert_packed_project(packed_project: 'PackedProject', plugin: 'Plugin') -> RemoteProject:
    root_dir = pathlib.Path(packed_project.get_name())

    # convert files from absolute local paths to absolute remote paths
    files = set(map(lambda file: pathlib.Path('/') / root_dir / file, packed_project.get_relative_files()))
    attributes = packed_project.get_attributes()

    project_attribute = plugin.get_api_client().get_api_schema(
        plugin.get_factory_collection()).get_root_project_attribute()
    attribute = project_attribute.get_attribute()

    # do the same to all file type project attributes
    while attribute.get_type() != AttributeType.NULL:
        value = packed_project.get_attribute(attribute.get_key())

        if attribute.get_type() == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FILE_PATH.value:
            # update the file path attribute
            value = (pathlib.Path('/') / root_dir / packed_project.get_relative_file_path(
                pathlib.Path(value))).as_posix()
            packed_project.set_attribute(attribute.get_key(), value)

        project_attribute = project_attribute.transition(value)
        attribute = project_attribute.get_attribute()

    return RemoteProject(packed_project.get_name(),
                         root_dir,
                         files,
                         attributes)

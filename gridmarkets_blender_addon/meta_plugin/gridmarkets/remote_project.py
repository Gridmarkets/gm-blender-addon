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
from gridmarkets_blender_addon.meta_plugin.attribute import AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute_types import StringSubtype

__all__ = 'RemoteProject', 'convert_packed_project'

import pathlib
import typing

from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject as MetaRemoteProject, RemoteProject
from gridmarkets_blender_addon.meta_plugin.project import Project
from ..cached_value import CachedValue

if typing.TYPE_CHECKING:
    from ..plugin import Plugin
    from ..packed_project import PackedProject
    from ..api_client import APIClient


class RemoteProject(MetaRemoteProject):

    def __init__(self,
                 name: str,
                 root_dir: pathlib.Path,
                 files: typing.Set[pathlib.Path],
                 attributes: typing.Dict[str, any],
                 api_client: 'APIClient'):

        Project.__init__(self,
                         name,
                         root_dir,
                         files,
                         attributes)

        self._api_client = api_client
        self._cached_size = CachedValue(0)
        self._cached_total_uploaded_bytes_done_uploading = CachedValue(0)
        self.update_project_status()

    def get_api_client(self) -> 'APIClient':
        return self._api_client

    def get_files(self, force_update=False) -> typing.Set[pathlib.Path]:
        if force_update:
            self.get_api_client().update_remote_project_status(self)

        return Project.get_files(self)

    def set_file_list(self, files: typing.Set[pathlib.Path]) -> None:
        self._files = files

    def update_project_status(self):
        self.get_api_client().update_remote_project_status(self)

    def set_name(self, name: str) -> None:
        raise NotImplementedError

    def exists(self) -> bool:
        raise NotImplementedError

    def delete(self) -> None:
        raise NotImplementedError

    def get_size(self, force_update=False) -> int:

        if force_update or not self._cached_size.is_cached():
            self.get_api_client().update_remote_project_status(self)

        return self._cached_size.get_value()

    def set_size(self, size: int) -> None:
        self._cached_size.set_value(size)

    def get_total_bytes_done_uploading(self, force_update: bool = False) -> int:

        if force_update or not self._cached_total_uploaded_bytes_done_uploading.is_cached():
            self.get_api_client().update_remote_project_status(self)

        return self._cached_total_uploaded_bytes_done_uploading.get_value()

    def set_total_bytes_done_uploading(self, bytes: int) -> None:
        self._cached_total_uploaded_bytes_done_uploading.set_value(bytes)

    def get_remaining_bytes_to_upload(self, force_update: bool = False) -> int:

        if force_update or \
                not self._cached_size.is_cached() or \
                not self._cached_total_uploaded_bytes_done_uploading.is_cached():

            self.get_api_client().update_remote_project_status(self)

        return self.get_size() - self.get_total_bytes_done_uploading()


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
                         attributes,
                         plugin.get_api_client())
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

import pathlib

from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject
from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType, StringSubtype


def convert_packed_project(packed_project: PackedProject) -> RemoteProject:
    from gridmarkets_blender_addon.blender_plugin.plugin_fetcher.plugin_fetcher import PluginFetcher
    plugin = PluginFetcher.get_plugin()

    root_dir = pathlib.Path(packed_project.get_name())

    # convert files from absolute local paths to absolute remote paths
    files = set(map(lambda file: pathlib.Path('/') / root_dir / file, packed_project.get_relative_files()))
    attributes = packed_project.get_attributes()

    project_attribute = plugin.get_api_client().get_api_schema().get_root_project_attribute()
    attribute = project_attribute.get_attribute()

    # do the same to all file type project attributes
    while attribute.get_type() != AttributeType.NULL:
        value = packed_project.get_attribute(attribute.get_key())

        if attribute.get_type() == AttributeType.STRING and attribute.get_subtype() == StringSubtype.FILE_PATH.value:
            #update the file path attribute
            value = str(pathlib.Path('/') / root_dir / packed_project.get_relative_file_path(pathlib.Path(value)))
            packed_project.set_attribute(attribute.get_key(), value)

        project_attribute = project_attribute.transition(value)
        attribute = project_attribute.get_attribute()

    return RemoteProject(packed_project.get_name(),
                         root_dir,
                         files,
                         attributes)

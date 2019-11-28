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

import os
import pathlib
import re
import json
from gridmarkets_blender_addon.meta_plugin.packed_project import PackedProject
from gridmarkets_blender_addon import constants

_PATH_MAPPINGS = {'Z:': "/data/input"}


class VRaySceneParser(object):
    anim_start_regex = r'\s+anim_start\=(?P<val>[0-9]+)'
    anim_end_regex = r'\s+anim_end\=(?P<val>[0-9]+)'
    img_width_regex = r'\s+img_width\=(?P<val>[0-9]+)'
    img_height_regex = r'\s+img_height\=(?P<val>[0-9]+)'
    #img_file_regex = r'\s+img_file\=["\']?(?P<val>[a-zA-z0-9._ -]+)["\']?'
    img_file_regex = r'\s+img_file\=["\']?(?P<val>[^"\']+)["\']?'
    file_path_regex = r'\s+file\=["\']?(?P<val>[^"\']+)["\']?'

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        props = dict()
        props['asset_files'] = list()
        props['asset_folders'] = list()
        props['frame_start'] = None
        props['frame_end'] = None
        props['frames'] = ''
        props['output_width'] = None
        props['output_height'] = None
        props['output_file'] = None
        props['output_folder'] = None

        with open(self.file_path) as file_:
            i = 0
            for line in file_:
                i = i + 1

                match = re.match(self.file_path_regex, line)
                if match:
                    asset_file = match.groupdict()["val"].replace('\\', '/')
                    asset_dir = os.path.split(asset_file)[0]

                    if asset_file not in props['asset_files']:
                        props['asset_files'].append(asset_file)

                    if asset_dir not in props['asset_folders']:
                        props['asset_folders'].append(asset_dir)

                match = re.match(self.img_file_regex, line)
                if match:
                    output_file = match.groupdict()["val"].replace('\\', '/')
                    output_dir = os.path.split(output_file)[0]
                    props['output_file'] = os.path.basename(output_file)
                    props['output_folder'] = output_dir

                match = re.match(self.anim_start_regex, line)
                if match:
                    props['frame_start'] = int(match.groupdict()["val"])

                match = re.match(self.anim_end_regex, line)
                if match:
                    props['frame_end'] = int(match.groupdict()["val"])

                if props['frame_start'] and not props['frame_end']:
                    props['frames'] = '{}'.format(props['frame_start'])
                elif props['frame_start'] and props['frame_end']:
                    props['frames'] = '{} {}'.format(props['frame_start'], props['frame_end'])

                match = re.match(self.img_width_regex, line)
                if match:
                    props['output_width'] = int(match.groupdict()["val"])

                match = re.match(self.img_height_regex, line)
                if match:
                    props['output_height'] = int(match.groupdict()["val"])

        props['asset_files'] = sorted(set(props['asset_files']))

        return props


class PackedVRayProject(PackedProject):

    def __init__(self, packed_dir: pathlib.Path, main_file: pathlib.Path):
        from gridmarkets_blender_addon.project.remote.remote_vray_project import RemoteVRayProject

        self._file_last_updated = str(os.path.getmtime(main_file)).replace('.', '-')
        remap_file_path = self.create_remap_file()

        attributes = {
            "PRODUCT": "vray",
            constants.MAIN_PROJECT_FILE: main_file,
            RemoteVRayProject.ATTRIBUTE_REMAP_FILE_KEY: remap_file_path
        }

        PackedProject.__init__(self,
                               packed_dir.stem,
                               packed_dir,
                               {main_file, remap_file_path},
                               attributes)


    def get_remap_file(self) -> pathlib.Path:
        from gridmarkets_blender_addon.project.remote.remote_vray_project import RemoteVRayProject
        return self.get_attribute(RemoteVRayProject.ATTRIBUTE_REMAP_FILE_KEY)

    def create_remap_file(self) -> pathlib.Path:
        from gridmarkets_blender_addon import constants

        remap_file = "{}-{}.xml".format(self.get_attribute(constants.MAIN_PROJECT_FILE).name, self._file_last_updated)
        src_path = os.path.dirname(str(self.get_attribute(constants.MAIN_PROJECT_FILE)))
        remap_file_path = os.path.join(src_path, remap_file)

        if not os.path.exists(remap_file_path):
            PackedVRayProject.create_remap_file_paths_xml(self.parse_scene_file(), remap_file_path)

        return pathlib.Path(remap_file_path)

    def parse_scene_file(self):
        #print("Parsing scene file...")
        from gridmarkets_blender_addon import constants

        scene_file = str(self.get_attribute(constants.MAIN_PROJECT_FILE))

        src_dir_name = os.path.split(scene_file)[0]

        # get the local path of the project directory
        src_path = os.path.abspath(src_dir_name)

        parsed_info = dict()
        parsed_info_file = ''

        parsed_info_file = os.path.join(
            src_path, '.parsed-info' + '-' + self._file_last_updated)

        if os.path.exists(parsed_info_file):
            #print("Cache found, loading scene file info from cache...")
            with open(parsed_info_file) as file_:
                parsed_info = json.load(file_)
                return parsed_info

        scene_parser = VRaySceneParser(scene_file)
        parsed_info = scene_parser.parse()
        #print("Parsing scene file completed.")

        with open(parsed_info_file, 'w') as file_:
            json.dump(parsed_info, file_)

        return parsed_info

    @staticmethod
    def create_remap_file_paths_xml(parsed_info, remap_file):
        import xml.etree.cElementTree as ET

        remapPaths = ET.Element('RemapPaths')

        file_dirs = parsed_info['asset_folders']

        for file_dir in file_dirs:
            for src, target in list(_PATH_MAPPINGS.items()):
                src = src.replace('\\', '/')
                if file_dir.startswith(src):
                    remapItem = ET.SubElement(remapPaths, 'RemapItem')
                    ET.SubElement(
                        remapItem, "From").text = file_dir.replace('/', '\\')
                    ET.SubElement(remapItem, "To").text = file_dir.replace(
                        src, target)

        doc = ET.ElementTree(remapPaths)
        doc.write(remap_file)

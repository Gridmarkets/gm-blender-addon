import pathlib
from typing import List, Set
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject


class RemoteVRayProject(RemoteProject):

    ATTRIBUTE_REMAP_FILE_KEY = "REMAP_FILE"

    def __init__(self, root_dir: pathlib.Path, main_file: pathlib.Path, remap_file: pathlib.Path):
        from gridmarkets_blender_addon import api_constants

        attributes = {
            "PRODUCT": api_constants.PRODUCTS.VRAY,
            self.ATTRIBUTE_REMAP_FILE_KEY : remap_file
        }

        RemoteProject.__init__(self,
                               root_dir.stem,
                               root_dir,
                               main_file,
                               set(),  # empty set for now since they are not used
                               attributes)

    def get_remap_file(self) -> pathlib.Path:
        return self.get_attribute(self.ATTRIBUTE_REMAP_FILE_KEY)

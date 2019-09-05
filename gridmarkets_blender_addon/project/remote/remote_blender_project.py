import pathlib
import typing
from typing import List, Set
from gridmarkets_blender_addon.meta_plugin.remote_project import RemoteProject


class RemoteBlenderProject(RemoteProject):

    def __init__(self, root_dir: pathlib.Path, main_file: pathlib.Path):
        RemoteProject.__init__(self,
                               root_dir.stem,
                               root_dir,
                               main_file,
                               set(),  # empty set for now since they are not used
                               {})

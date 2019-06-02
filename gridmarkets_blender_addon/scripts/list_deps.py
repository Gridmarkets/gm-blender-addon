"""
Calls blender_asset_tracer's tracer.deps() method.

Expects 1 argument
 - The first argument (argv[1]) is expected to be the file path of the .blend file in question

Returns a JSON string containing a list of .blend files and the set of dependencies for each file.
"""

import collections
import json
import pathlib
import os
import sys
import argparse

# the lib path which contains the blender_asset_tracer module
lib_path = None

# the provided .blend file path
blend_file_path = None

called_from_blender = False

# if script is run using blender then args need parsing differently
if '--' in sys.argv:
    parser = argparse.ArgumentParser()

    # get arguments after '--'
    argv = sys.argv[sys.argv.index('--') + 1:]

    parser.add_argument('-p', '--path')
    args = parser.parse_known_args(argv)[0]

    lib_path = os.path.join(os.path.dirname(os.path.dirname(sys.argv[3])),'lib')
    blend_file_path = args.path
    called_from_blender = True

else:
    lib_path = os.path.join(os.path.dirname(sys.path[0]),'lib')
    blend_file_path = sys.argv[1]

# Since blender_asset_tracer is located in the lib folder we must add it to the path.
# Cannot simply import gridmarkets_blender_plugin.lib.blender_asset_tracer as a module since it relies on blender's bpy
# module which is only available in blender.
sys.path.append(lib_path)

# noinspection PyUnresolvedReferences
from blender_asset_tracer import trace

# the dependencies as a mapping from the blend file to its set of dependencies.
dependencies = collections.defaultdict(set)

# Find the dependencies
for usage in trace.deps(pathlib.Path(blend_file_path)):
    filePath = usage.block.bfile.filepath.absolute()
    for assetPath in usage.files():
        assetPath = assetPath.resolve()
        dependencies[str(filePath)].add(assetPath)

if(called_from_blender):
    print()

class JSONSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, pathlib.Path):
            return str(o)
        if isinstance(o, set):
            return sorted(o)
        return super().default(o)


# Output the dependencies as JSON
json.dump(dependencies, sys.stdout, cls=JSONSerializer, indent=0)
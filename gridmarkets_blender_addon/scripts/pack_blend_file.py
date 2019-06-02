"""
Calls blender_asset_tracer's pack method.

Expects 2 arguments
 - The first argument (argv[1]) is expected to be the file path of the .blend file in question
 - The first argument (argv[2]) is expected to be the target path that the packed file should be output to

Returns void.
"""

import pathlib
import os
import sys
import argparse

# the lib path which contains the blender_asset_tracer module
lib_path = None

# the provided .blend file path
blend_file_path = None
project_root_path = None
target_path = None

called_from_blender = False

# if script is run using blender then args need parsing differently
if '--' in sys.argv:
    parser = argparse.ArgumentParser()

    # get arguments after '--'
    argv = sys.argv[sys.argv.index('--') + 1:]

    parser.add_argument('-p', '--path')
    parser.add_argument('-t', '--target')
    args = parser.parse_known_args(argv)[0]

    lib_path = os.path.join(os.path.dirname(os.path.dirname(sys.argv[3])),'lib')

    blend_file_path = pathlib.Path(args.path)
    project_root_path = blend_file_path.parent
    target_path = pathlib.Path(args.target)
    called_from_blender = True

else:
    lib_path = os.path.join(os.path.dirname(sys.path[0]),'lib')

    blend_file_path = pathlib.Path(sys.argv[1])
    project_root_path = blend_file_path.parent
    target_path = pathlib.Path(sys.argv[2])

# Since blender_asset_tracer is located in the lib folder we must add it to the path.
# Cannot simply import gridmarkets_blender_plugin.lib.blender_asset_tracer as a module since it relies on blender's bpy
# module which is only available in blender.
sys.path.append(lib_path)

# noinspection PyUnresolvedReferences
from blender_asset_tracer import pack

# create packer
with pack.Packer(blend_file_path,
                 project_root_path,
                 target_path,
                 noop=False,
                 compress=False,
                 relative_only=False
                 ) as packer:

    # plan the packing operation (must be called before execute)
    packer.strategise()

    # attempt to pack the project
    try:
        packer.execute()
    except pack.transfer.FileTransferError as ex:
        print("%d files couldn't be copied, starting with %s",
                  len(ex.files_remaining), ex.files_remaining[0])
        raise SystemExit(1)

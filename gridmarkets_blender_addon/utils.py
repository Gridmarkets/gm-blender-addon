import bpy
import os
import sys
import json
import pathlib
import subprocess

LIST_DEPS_SCRIPT = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / 'scripts/list_deps.py')
PACK_BLEND_FILE_SCRIPT = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / 'scripts/pack_blend_file.py')


def get_project_dependencies(blend_file):
    """ Creates a new process which searches the provided .blend file for dependencies.

    :param blend_file: the .blend file to inspect
    :type blend_file: str
    :return: A dictionary of .blend files and their sets of dependencies
    :rtype: dictionary
    """

    # Create the subprocess which will get the dependencies.
    # This must be done using a subprocess since there is a bug with the blender_asset_tracer.trace module in that it
    # wont release the file handles for any .blend files it encounters (maybe worth a PR). By using a subprocess all
    # files are automatically released after the script terminates.
    # TODO call using blender not python as user may not have python istalled
    p = subprocess.Popen(['python', str(LIST_DEPS_SCRIPT), blend_file], stdout=subprocess.PIPE)

    # Pipe subprocess output into variables
    stdOutput, stderrOutput = p.communicate()

    # wait for list_deps.py script to finish
    p.wait()

    # parse the results
    dependencies = json.loads(stdOutput)

    return dependencies


def pack_blend_file(blend_file, target):
    """ Packs a Blender .blend file to a target folder using blender_asset_tracer

    :param blend_file: the .blend file to pack
    :type blend_file: str
    :param target: the location to pack the .blend file to
    :type target: str
    """

    blender_exe = str(bpy.app.binary_path)

    # Create the subprocess which will get the dependencies.
    # This must be done using a subprocess since there is a bug with the blender_asset_tracer.trace module in that it
    # wont release the file handles for any .blend files it encounters (maybe worth a PR). By using a subprocess all
    # files are automatically released after the script terminates.
    p = subprocess.Popen([blender_exe,
                          "--background",
                          "--python",
                          PACK_BLEND_FILE_SCRIPT,
                          # "--factory-startup",
                          "--addons",
                          "gridmarkets_blender_addon",
                          "--",
                          "-p", blend_file,
                          "-t", target], stdout=subprocess.PIPE)


    #p = subprocess.Popen(['python', str(PACK_BLEND_FILE_SCRIPT), blend_file, target], stdout=subprocess.PIPE)

    # Pipe subprocess output into variables
    stdOutput, stderrOutput = p.communicate()

    p.wait()


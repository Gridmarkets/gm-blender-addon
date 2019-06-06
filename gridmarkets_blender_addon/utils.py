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


def create_unique_object_name(objects, name_prefix = ""):
    """ Creates a unique name of the form [name_prefix][x] where x is some unique positive integer.

    :param objects: the existing list of objects that this new name must not collide with. Objects in said list may or
                    may not have .name attributes or follow the provided naming scheme
    :type objects: list
    :param name_prefix: a optional prefix to append before the unique number
    :type name_prefix: str
    :return: the unique name
    :rtype: str
    """

    prefix_length = len(name_prefix)

    # compile a list of used numeric integer suffixes
    used_suffixes = []
    for element in objects:
        if hasattr(element, 'name') and isinstance(element.name, str) and element.name.startswith(name_prefix):
            element_suffix = element.name[prefix_length:]
            if element_suffix.isdigit():
                try:
                    element_suffix = int(element_suffix)

                    if element_suffix >= 0:
                        used_suffixes.append(element_suffix)

                except ValueError:
                    pass

    # remove duplicates
    used_suffixes = list(set(used_suffixes))

    # sort
    used_suffixes.sort()

    # find a number which has not been used yet
    i = 0
    while i in used_suffixes:
        i = i+1

    return name_prefix + str(i)


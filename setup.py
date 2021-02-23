#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import glob
import os
import sys
import shutil
import subprocess
import pathlib
import zipfile

from distutils import log
from distutils.core import Command
from distutils.command.install_egg_info import install_egg_info
from setuptools import setup, find_packages


# Global Constants
# import readme text for long description
readme = open('README.md', 'r')
README_TEXT = readme.read()
readme.close()

# Package meta-data.
NAME = 'gridmarkets_blender_addon'
DESCRIPTION = 'Allows users to submit Blender jobs to the GridMarkets render farm from within Blender.'
LONG_DESCRIPTION = README_TEXT
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = 'https://www.gridmarkets.com/'
EMAIL = 'olliedawes@gmail.com'
AUTHOR = 'Ollie Dawes'
VERSION = '0.3.4'

# file paths
HERE = pathlib.Path(__file__).resolve().parent
ADDON_FOLDER = HERE / NAME
DEFAULT_LIB_FOLDER = ADDON_FOLDER / 'lib'
DIST_FOLDER = HERE / 'dist'
DEFAULT_DIST_OUTPUT_LOCATION = (DIST_FOLDER / NAME)
DEFAULT_ZIP_OUTPUT_LOCATION = DEFAULT_DIST_OUTPUT_LOCATION.with_suffix('.zip')

requirements = [
    'blender-asset-tracer',
]


class BuildDependencies(Command):
    """Downloads and builds the dependencies to the add-ons lib folder."""

    description = "Downloads and builds the dependencies to the add-ons lib folder."
    user_options = [
        ('lib-path=', 'd', "the path the dependencies are stored for use by the add-on"),
    ]

    def initialize_options(self):
        self.lib_path = None

    def finalize_options(self):
        # use default lib path unless one is explicitly provided by the user
        if self.lib_path:
            self.lib_path = pathlib.Path(self.path)
        else:
            self.lib_path = DEFAULT_LIB_FOLDER

    def run(self):
        log.info('Installing packages to: %s', self.lib_path)

        for package in requirements:
            self.install_package(package)

    def install_package(self, package):
        """Installs wheel from PyPI to lib folder"""

        log.info('Installing package: %s', package)

        subprocess.call([sys.executable,
                         "-m",
                         "pip",
                         "install",
                         "-t", str(self.lib_path),
                         package])


class CleanCache(Command):
    """ Recursively deletes the __pycache__ directories """

    description = "Recursively deletes the __pycache__ directories."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.info('Cleaning __pycache__ directories')

        path = pathlib.Path(ADDON_FOLDER)
        for p in path.rglob("*"):
            if p.name == '__pycache__':
                shutil.rmtree(p)


class Bzip(Command):
    """ Zips the add-on folder for distribution so that it can be installed by Blender. Overwrites any existing zip file
    of the same name in the output folder.
    """

    description = "Zips the add-on folder for distribution so that it can be installed by Blender. Overwrites any" \
                  "existing zip file of the same name in the output folder"
    user_options = [
        ('path=', 'd', "the path the zip file is output to"),
    ]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        # use default path unless one is explicitly provided by the user
        if self.path:
            self.path = pathlib.Path(self.path)
        else:
            self.path = DEFAULT_DIST_OUTPUT_LOCATION

    def run(self):
        # create the dist folder if it does not exist yet
        DIST_FOLDER.mkdir(parents=True, exist_ok=True)

        self.run_command('clean_cache')

        shutil.make_archive(
            self.path, # zip file name
            'zip',  # the archive format - or tar, bztar, gztar
            root_dir=ADDON_FOLDER.parent,  # root for archive - current working dir if None
            base_dir=ADDON_FOLDER.stem)  # start archiving from here - cwd if None too


class Fdist(Bzip):
    """ Extracts the output of Bzip to either the dist folder or a provided location."""

    description = "Extracts the output of Bzip to either the dist folder or a provided location."
    user_options = [
        ('path=', 'd', 'the path to copy the add-on folder to'),
    ]

    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        # use default path unless one is explicitly provided by the user
        if self.path:
            self.path = pathlib.Path(self.path)
        else:
            self.path = DIST_FOLDER

    def run(self):
        # delete the output folder if it already exists
        if os.path.exists(self.path / NAME):
            log.info('Add-on already exists in directory. Removing old add-on.')
            shutil.rmtree(self.path / NAME, ignore_errors=True)

        # re-generate the zipped add-on
        self.run_command('bzip')

        log.info('Extracting add-on to: %s', self.path)

        # extract add-on to folder
        with zipfile.ZipFile(DEFAULT_ZIP_OUTPUT_LOCATION, 'r') as zip_ref:
            zip_ref.extractall(self.path)


class AvoidEggInfo(install_egg_info):
    """Makes sure the egg-info directory is NOT created.
    If we skip this, the user's addon directory can be polluted by egg-info
    directories, which Blender doesn't use anyway.
    """

    def run(self):
        pass


setup(
    cmdclass={'bzip': Bzip,
              'fdist': Fdist,
              'wheels': BuildDependencies,
              'clean_cache': CleanCache},
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages('.'),
    data_files=[('gridmarkets_blender_addon', ['README.md']),
                ('gridmarkets_blender_addon/icons', glob.glob('gridmarkets_blender_addon/icons/*'))],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Environment :: Plugins',
        'Programming Language :: Python'
    ]
)

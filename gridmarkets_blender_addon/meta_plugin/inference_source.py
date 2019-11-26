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

import typing


class InferenceSource:
    """
    An InferenceSource is the source from which to obtain the value for an attribute. JobPreset Attributes can be
    derived from the JobPreset it self as pre-defined or user-defined constants or from the application or project.
    """

    # InferenceSource id constants
    USER_DEFINED = "USER_DEFINED"
    CONSTANT = "CONSTANT"
    PROJECT = "PROJECT"
    APPLICATION = "APPLICATION"

    # descriptions
    USER_DEFINED_DESCRIPTION = "Use the value specified by the user in the form field"
    CONSTANT_DESCRIPTION = "Use the pre-defined constant value for this attribute"
    PROJECT_DESCRIPTION = "Read the value from the project's attributes when you submit"
    APPLICATION_DESCRIPTION = "Use the value specified by the application"

    _user_defined: 'InferenceSource' = None
    _constant: 'InferenceSource' = None
    _project: 'InferenceSource' = None
    _application: 'InferenceSource' = None

    def __init__(self, inference_source_id: str, display_name: str, description: str):
        self._inference_source_id = inference_source_id
        self._display_name = display_name
        self._description = description

    def get_id(self) -> str:
        return self._inference_source_id

    def get_display_name(self) -> str:
        return self._display_name

    def get_description(self) -> str:
        return self._description

    def __eq__(self, other: 'InferenceSource'):
        return self.get_id() == other.get_id()

    def __ne__(self, other: 'InferenceSource'):
        return self.get_id() != other.get_id()

    @staticmethod
    def is_inference_source_id(value: str):
        return value == InferenceSource.USER_DEFINED or \
               value == InferenceSource.CONSTANT or \
               value == InferenceSource.PROJECT or \
               value == InferenceSource.APPLICATION

    @staticmethod
    def get_inference_source(source_id: str):
        if not InferenceSource.is_inference_source_id(source_id):
            raise ValueError("Unrecognised inference source id.")

        if source_id == InferenceSource.USER_DEFINED:
            return InferenceSource.get_user_defined_inference_source()

        if source_id == InferenceSource.CONSTANT:
            return InferenceSource.get_constant_inference_source()

        if source_id == InferenceSource.PROJECT:
            return InferenceSource.get_project_inference_source()

        if source_id == InferenceSource.APPLICATION:
            return InferenceSource.get_application_inference_source()

    @staticmethod
    def get_all_inference_source_types() -> typing.List['InferenceSource']:
        inference_sources = list()
        inference_sources.append(InferenceSource.get_user_defined_inference_source())
        inference_sources.append(InferenceSource.get_constant_inference_source())
        inference_sources.append(InferenceSource.get_project_inference_source())
        inference_sources.append(InferenceSource.get_application_inference_source())
        return inference_sources

    @staticmethod
    def get_user_defined_inference_source():
        if InferenceSource._user_defined is None:
            InferenceSource._user_defined = InferenceSource(InferenceSource.USER_DEFINED, "User Defined",
                                                            InferenceSource.USER_DEFINED_DESCRIPTION)
        return InferenceSource._user_defined

    @staticmethod
    def get_constant_inference_source():
        if InferenceSource._constant is None:
            InferenceSource._constant = InferenceSource(InferenceSource.CONSTANT, "Constant",
                                                        InferenceSource.CONSTANT_DESCRIPTION)
        return InferenceSource._constant

    @staticmethod
    def get_project_inference_source():
        if InferenceSource._project is None:
            InferenceSource._project = InferenceSource(InferenceSource.PROJECT, "Project",
                                                       InferenceSource.PROJECT_DESCRIPTION)
        return InferenceSource._project

    @staticmethod
    def get_application_inference_source():
        if InferenceSource._application is None:
            InferenceSource._application = InferenceSource(InferenceSource.APPLICATION, "Application",
                                                           InferenceSource.APPLICATION_DESCRIPTION)
        return InferenceSource._application

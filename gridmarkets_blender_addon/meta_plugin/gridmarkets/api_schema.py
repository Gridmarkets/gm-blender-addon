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

from gridmarkets_blender_addon.meta_plugin.api_schema import APISchema
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.attribute_type import AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute import EnumItem, EnumAttribute, StringAttribute
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
from gridmarkets_blender_addon.meta_plugin.attribute_inference_source import AttributeInferenceSource
from gridmarkets_blender_addon.meta_plugin.transition import Transition

import xml.etree.ElementTree as ET
import pathlib
import typing


def get_all_sub_elements(element: ET.Element, tag_name: str, expect_at_least_one: bool = False) -> typing.List[
    ET.Element]:
    elements = element.findall(tag_name)

    if expect_at_least_one and len(elements) < 1:
        raise ValueError("The <" + element.tag + "> element must contain at least one <" + tag_name +
                         "> child element")

    return elements


def get_sub_element(element: ET.Element, tag_name: str, expect_unique_tag: bool = True) -> ET.Element:
    elements = element.findall(tag_name)

    if len(elements) == 0:
        raise ValueError("The <" + element.tag + "> element must contain exactly one <" + tag_name + "> child element")

    if expect_unique_tag and len(elements) != 1:
        raise ValueError("The <" + element.tag + "> element must contain exactly one <" + tag_name + "> child element")

    return elements[0]


def get_attribute(element: ET.Element, attribute_key: str) -> str:
    if attribute_key not in element.attrib:
        raise ValueError("All <" + element.tag + "> tags must contain an '" + attribute_key + "' attribute")

    return element.attrib[attribute_key]


def get_all_sub_elements_text(element: ET.Element, tag_name: str, expect_at_least_one: bool = True) -> typing.List[str]:
    elements = get_all_sub_elements(element, tag_name, expect_at_least_one)
    return list(map(lambda x: x.text, elements))


def get_text(element: ET.Element, tag_name: str, expect_unique_tag: bool = True) -> str:
    element = get_sub_element(element, tag_name, expect_unique_tag)
    return element.text


class GridMarketsAPISchema(APISchema):

    def __init__(self):
        self._job_definitions = []
        self._project_attributes = []
        self._parse_schema()

    def _parse_schema(self):
        SCHEMA_DEFINITION_FILE = pathlib.Path(__file__).parent / "APISchema.xml"

        TAG_API_SCHEMA = "APISchema"
        TAG_JOB_DEFINITIONS = "JobDefinitions"
        TAG_JOB_DEFINITION = "JobDefinition"
        ID_ATTRIBUTE = "id"
        TAG_DISPLAY_NAME = "DisplayName"
        TAG_DESCRIPTION = "Description"
        TAG_OPTIONAL = "Optional"
        TAG_TYPE = "Type"
        TAG_ITEMS = "Items"
        TAG_KEY = "Key"
        TAG_ATTRIBUTE = "Attribute"
        TAG_INFERENCE_SOURCES = "InferenceSources"
        TAG_INFERENCE_SOURCE = "InferenceSource"
        TAG_ATTRIBUTE_KEY_ATTRIBUTE = "key"
        TAG_PROJECT_ATTRIBUTES = "ProjectAttributes"
        TAG_PROJECT_ATTRIBUTE = "ProjectAttribute"
        TAG_VALID_PROJECT = "ValidProject"
        TAG_TRANSITIONS = "Transitions"
        TAG_TRANSITION = "Transition"
        TAG_PROJECT_ATTRIBUTE_ID = "ProjectAttributeId"
        ATRRIBUTE_ID = "id"
        TAG_TRANSITION_FORMULA = "TransitionFormula"
        TAG_COMPATIBLE_JOB_TYPES = "CompatibleJobTypes"
        TAG_JOB_DEFINITION_ID = "JobDefinitionId"

        tree = ET.parse(SCHEMA_DEFINITION_FILE)
        root = tree.getroot()

        if root.tag != TAG_API_SCHEMA:
            raise ValueError("API schema file must have a <" + TAG_API_SCHEMA + "> tag as the root")

        # parse job definitions
        job_definitions_element = get_sub_element(root, TAG_JOB_DEFINITIONS)
        job_definition_elements = get_all_sub_elements(job_definitions_element, TAG_JOB_DEFINITION)

        for job_definition_element in job_definition_elements:

            if ID_ATTRIBUTE not in job_definition_element.attrib:
                raise ValueError("All <" + TAG_JOB_DEFINITION + "> tags must contain an 'id' attribute")

            job_definition_id = get_attribute(job_definition_element, ID_ATTRIBUTE)
            job_definition_display_name = get_text(job_definition_element, TAG_DISPLAY_NAME)

            attribute_elements = get_all_sub_elements(job_definition_element, TAG_ATTRIBUTE, expect_at_least_one=True)

            attributes = []

            for attribute_element in attribute_elements:
                attribute_key = get_attribute(attribute_element, TAG_ATTRIBUTE_KEY_ATTRIBUTE)
                attribute_display_name = get_text(attribute_element, TAG_DISPLAY_NAME)
                attribute_description = get_text(attribute_element, TAG_DESCRIPTION)
                attribute_is_optional = get_text(attribute_element, TAG_OPTIONAL)

                inference_sources_element = get_sub_element(attribute_element, TAG_INFERENCE_SOURCES)
                attribute_inference_sources = get_all_sub_elements_text(inference_sources_element, TAG_INFERENCE_SOURCE)
                attribute_type = get_text(attribute_element, TAG_TYPE)

                if attribute_type == AttributeType.STRING.value:

                    def string_init(self,
                                    key: str,
                                    display_name: str,
                                    description: str,
                                    inference_sources: typing.List[AttributeInferenceSource],
                                    is_optional):

                        StringAttribute.__init__(self)
                        JobAttribute.__init__(self, key, display_name, description, inference_sources, is_optional)

                    job_attribute_string = type("JobAttributeString",
                                                (StringAttribute, JobAttribute),
                                                {
                                                    "key": attribute_key,
                                                    "display_name": attribute_display_name,
                                                    "description": attribute_description,
                                                    "inference_sources": attribute_inference_sources,
                                                    "is_optional": attribute_is_optional,
                                                    "__init__": string_init
                                                })

                    attributes.append(job_attribute_string(attribute_key,
                                                           attribute_display_name,
                                                           attribute_description,
                                                           attribute_inference_sources,
                                                           attribute_is_optional))

                elif attribute_type == AttributeType.ENUM.value:

                    def enum_init(self,
                                  key: str,
                                  display_name: str,
                                  description: str,
                                  inference_sources: typing.List[AttributeInferenceSource],
                                  is_optional: bool,
                                  items: typing.List[EnumItem]):

                        EnumAttribute.__init__(self, items)
                        JobAttribute.__init__(self, key, display_name, description, inference_sources, is_optional)

                    enum_items_element = get_sub_element(attribute_element, TAG_ITEMS)
                    enum_items: typing.List[EnumItem] = []
                    for enum_item_element in enum_items_element:
                        enum_item_key = get_text(enum_item_element, TAG_KEY)
                        enum_item_display_name = get_text(enum_item_element, TAG_DISPLAY_NAME)
                        enum_item_description = get_text(enum_item_element, TAG_DESCRIPTION)
                        enum_items.append(EnumItem(enum_item_key, enum_item_display_name, enum_item_description))

                    job_attribute_enum = type("JobAttributeEnum",
                                              (EnumAttribute, JobAttribute),
                                              {
                                                  "key": attribute_key,
                                                  "display_name": attribute_display_name,
                                                  "description": attribute_description,
                                                  "inference_sources": attribute_inference_sources,
                                                  "is_optional": attribute_is_optional,
                                                  "items": enum_items,
                                                  "__init__": enum_init
                                              })

                    attributes.append(job_attribute_enum(attribute_key,
                                                         attribute_display_name,
                                                         attribute_description,
                                                         attribute_inference_sources,
                                                         attribute_is_optional,
                                                         enum_items))

            self._job_definitions.append(JobDefinition(job_definition_id, job_definition_display_name, attributes))

        # parse project attributes
        project_attributes_element = get_sub_element(root, TAG_PROJECT_ATTRIBUTES)
        project_attribute_elements = get_all_sub_elements(project_attributes_element, TAG_PROJECT_ATTRIBUTE)

        for project_attribute_element in project_attribute_elements:
            project_attribute_id = get_attribute(project_attribute_element, ATRRIBUTE_ID)

            key_element = project_attribute_element.find(TAG_KEY)
            if key_element:
                project_attribute_key = key_element.text
            else:
                project_attribute_key = project_attribute_id

            project_attribute_display_name = get_text(project_attribute_element, TAG_DISPLAY_NAME)
            project_attribute_description = get_text(project_attribute_element, TAG_DESCRIPTION)
            project_attribute_valid_project = (get_text(project_attribute_element, TAG_VALID_PROJECT) == "True")
            project_attribute_type = get_text(project_attribute_element, TAG_TYPE)
            project_attribute_transitions = []

            transitions_element = get_sub_element(project_attribute_element, TAG_TRANSITIONS)
            transition_elements = get_all_sub_elements(transitions_element, TAG_TRANSITION)

            for transition_element in transition_elements:
                transition_project_attribute_id = get_text(transition_element, TAG_PROJECT_ATTRIBUTE_ID)
                transition_project_attribute = self.get_project_attribute_with_id(transition_project_attribute_id)
                transition_formula = get_text(transition_element, TAG_TRANSITION_FORMULA)

                project_attribute_transitions.append(Transition(transition_project_attribute,
                                                                transition_formula))
            project_attribute_compatible_job_definitions = []

            compatible_job_definitions_element = get_sub_element(project_attribute_element, TAG_COMPATIBLE_JOB_TYPES)
            job_definition_ids = get_all_sub_elements_text(compatible_job_definitions_element, TAG_JOB_DEFINITION_ID,
                                                           False)

            for job_definition_id in job_definition_ids:
                project_attribute_compatible_job_definitions.append(self.get_job_definition_with_id(job_definition_id))

            if project_attribute_type == AttributeType.STRING.value:

                def string_init(self,
                                id: str,
                                key: str,
                                display_name: str,
                                description: str,
                                is_valid_project: bool,
                                transitions: typing.List[Transition]):
                    StringAttribute.__init__(self)
                    ProjectAttribute.__init__(self, id, key, display_name, description, is_valid_project, transitions)

                project_attribute_string = type("ProjectAttributeString",
                                                (EnumAttribute, ProjectAttribute),
                                                {
                                                    "id": project_attribute_id,
                                                    "key": project_attribute_key,
                                                    "display_name": project_attribute_display_name,
                                                    "description": project_attribute_description,
                                                    "is_valid_project": project_attribute_valid_project,
                                                    "transitions": project_attribute_transitions,
                                                    "__init__": string_init
                                                })

                self._project_attributes.append(project_attribute_string(project_attribute_id,
                                                                         project_attribute_key,
                                                                         project_attribute_display_name,
                                                                         project_attribute_description,
                                                                         project_attribute_valid_project,
                                                                         project_attribute_transitions))
            elif project_attribute_type == AttributeType.ENUM.value:

                def enum_init(self,
                              id: str,
                              key: str,
                              display_name: str,
                              description: str,
                              is_valid_project: bool,
                              transitions: typing.List[Transition],
                              items: typing.List[EnumItem]):

                    EnumAttribute.__init__(self, items)
                    ProjectAttribute.__init__(self, id, key, display_name, description, is_valid_project, transitions)

                enum_items_element = get_sub_element(project_attribute_element, TAG_ITEMS)
                enum_items: typing.List[EnumItem] = []
                for enum_item_element in enum_items_element:
                    enum_item_key = get_text(enum_item_element, TAG_KEY)
                    enum_item_display_name = get_text(enum_item_element, TAG_DISPLAY_NAME)
                    enum_item_description = get_text(enum_item_element, TAG_DESCRIPTION)
                    enum_items.append(EnumItem(enum_item_key, enum_item_display_name, enum_item_description))

                project_attribute_enum = type("ProjectAttributeEnum",
                                              (EnumAttribute, ProjectAttribute),
                                              {
                                                  "id": project_attribute_id,
                                                  "key": project_attribute_key,
                                                  "display_name": project_attribute_display_name,
                                                  "description": project_attribute_description,
                                                  "is_valid_project": project_attribute_valid_project,
                                                  "transitions": project_attribute_transitions,
                                                  "items": enum_items,
                                                  "__init__": enum_init
                                              })

                self._project_attributes.append(project_attribute_enum(project_attribute_id,
                                                                       project_attribute_key,
                                                                       project_attribute_display_name,
                                                                       project_attribute_description,
                                                                       project_attribute_valid_project,
                                                                       project_attribute_transitions,
                                                                       enum_items))

    def get_job_definitions(self) -> typing.List[JobDefinition]:
        return self._job_definitions

    def get_project_attributes(self) -> typing.List[ProjectAttribute]:
        return self._project_attributes

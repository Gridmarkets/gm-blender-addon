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
from gridmarkets_blender_addon.meta_plugin.attribute_types import AttributeType, EnumItem
from gridmarkets_blender_addon.meta_plugin.job_attribute import *
from gridmarkets_blender_addon.meta_plugin.project_attribute import *
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


def to_bool(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ValueError("Could not convert value: " + value + " to python bool. Expects either 'True' or 'False'.")


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
TAG_DEFAULT_VALUE = "DefaultValue"
TAG_TRANSITIONS = "Transitions"
TAG_TRANSITION = "Transition"
TAG_PROJECT_ATTRIBUTE_ID = "ProjectAttributeId"
ATRRIBUTE_ID = "id"
TAG_TRANSITION_FORMULA = "TransitionFormula"
TAG_COMPATIBLE_JOB_DEFINITIONS = "CompatibleJobDefinitions"
TAG_JOB_DEFINITION_ID = "JobDefinitionId"


class XMLAPISchemaParser:
    """ Reads the xml api schema file and builds a APISchema class instance """

    @staticmethod
    def _parse_enum_items(enum_items_element: ET.Element) -> typing.List[EnumItem]:
        # instantiate the output list
        enum_items: typing.List[EnumItem] = []

        # parse each enum item
        for enum_item_element in enum_items_element:
            enum_item_key = get_text(enum_item_element, TAG_KEY)
            enum_item_display_name = get_text(enum_item_element, TAG_DISPLAY_NAME)
            enum_item_description = get_text(enum_item_element, TAG_DESCRIPTION)
            enum_items.append(EnumItem(enum_item_key, enum_item_display_name, enum_item_description))

        return enum_items

    @staticmethod
    def _parse_job_inference_sources(inference_sources_element: ET.Element) -> typing.List[AttributeInferenceSource]:

        attribute_inference_sources: typing.List[str] = get_all_sub_elements_text(
            inference_sources_element, TAG_INFERENCE_SOURCE)

        recognised_inference_source_values = set(source.value for source in AttributeInferenceSource)

        # check the inference source is a recognised string
        for attribute_inference_source in attribute_inference_sources:
            if attribute_inference_source not in recognised_inference_source_values:
                raise ValueError("Attribute inference source " + attribute_inference_source + " is not recognised.")

        # noinspection PyTypeChecker
        validated_inference_sources: typing.List[AttributeInferenceSource] = attribute_inference_sources

        return validated_inference_sources

    @staticmethod
    def _parse_job_attribute(job_attribute_element: ET.Element) -> JobAttribute:
        attribute_key = get_attribute(job_attribute_element, TAG_ATTRIBUTE_KEY_ATTRIBUTE)
        attribute_display_name = get_text(job_attribute_element, TAG_DISPLAY_NAME)
        attribute_description = get_text(job_attribute_element, TAG_DESCRIPTION)
        attribute_is_optional = to_bool(get_text(job_attribute_element, TAG_OPTIONAL))

        inference_sources_element = get_sub_element(job_attribute_element, TAG_INFERENCE_SOURCES)
        attribute_inference_sources = XMLAPISchemaParser._parse_job_inference_sources(inference_sources_element)

        # get default value (optional)
        job_attribute_default_value_elements = job_attribute_element.findall(TAG_DEFAULT_VALUE)
        if job_attribute_default_value_elements:
            job_attribute_default_value = job_attribute_default_value_elements[0].text
        else:
            job_attribute_default_value = None

        attribute_type = get_text(job_attribute_element, TAG_TYPE)

        if attribute_type == AttributeType.STRING.value:
            return StringJobAttribute(attribute_key,
                                      attribute_display_name,
                                      attribute_description,
                                      attribute_inference_sources,
                                      attribute_is_optional,
                                      default_value=job_attribute_default_value)

        elif attribute_type == AttributeType.ENUM.value:
            enum_items_element = get_sub_element(job_attribute_element, TAG_ITEMS)
            enum_items = XMLAPISchemaParser._parse_enum_items(enum_items_element)

            return EnumJobAttribute(attribute_key,
                                    attribute_display_name,
                                    attribute_description,
                                    attribute_inference_sources,
                                    attribute_is_optional,
                                    enum_items,
                                    default_value=job_attribute_default_value)

        elif attribute_type == AttributeType.NULL.value:
            return NullJobAttribute(attribute_key,
                                    attribute_display_name,
                                    attribute_description,
                                    attribute_inference_sources,
                                    attribute_is_optional)

        elif attribute_type == AttributeType.BOOLEAN.value:
            return BooleanJobAttribute(attribute_key,
                                       attribute_display_name,
                                       attribute_description,
                                       attribute_inference_sources,
                                       attribute_is_optional,
                                       default_value=job_attribute_default_value)

        else:
            raise ValueError("Unrecognised attribute type.")

    @staticmethod
    def _parse_job_definition(job_definition_element: ET.Element) -> JobDefinition:

        if ID_ATTRIBUTE not in job_definition_element.attrib:
            raise ValueError("All <" + TAG_JOB_DEFINITION + "> tags must contain an 'id' attribute")

        job_definition_id = get_attribute(job_definition_element, ID_ATTRIBUTE)
        job_definition_display_name = get_text(job_definition_element, TAG_DISPLAY_NAME)

        attribute_elements = get_all_sub_elements(job_definition_element, TAG_ATTRIBUTE, expect_at_least_one=True)

        attributes = []
        for attribute_element in attribute_elements:
            attributes.append(XMLAPISchemaParser._parse_job_attribute(attribute_element))

        return JobDefinition(job_definition_id, job_definition_display_name, attributes)

    @staticmethod
    def _parse_job_definitions(api_schema_element: ET.Element) -> typing.List[JobDefinition]:

        # instantiate the output list
        job_definitions: typing.List[JobDefinition] = []

        # parse job definitions
        job_definitions_element = get_sub_element(api_schema_element, TAG_JOB_DEFINITIONS)
        job_definition_elements = get_all_sub_elements(job_definitions_element, TAG_JOB_DEFINITION)

        for job_definition_element in job_definition_elements:
            job_definitions.append(XMLAPISchemaParser._parse_job_definition(job_definition_element))

        return job_definitions

    @staticmethod
    def _parse_transition(transition_element: ET.Element,
                          project_attributes: typing.List[ProjectAttribute]) -> Transition:

        transition_project_attribute_id = get_text(transition_element, TAG_PROJECT_ATTRIBUTE_ID)

        for project_attribute in project_attributes:
            if project_attribute.get_id() == transition_project_attribute_id:
                transition_project_attribute = project_attribute
                break
        else:
            raise ValueError("No ProjectAttribute with id '" + transition_project_attribute_id + "' found.")

        transition_formula = get_text(transition_element, TAG_TRANSITION_FORMULA)

        return Transition(transition_formula, transition_project_attribute)

    @staticmethod
    def _parse_transitions(transitions_element: ET.Element,
                           project_attributes: typing.List[ProjectAttribute]) -> typing.List[Transition]:

        # instantiate the output list
        transitions: typing.List[Transition] = []

        transition_elements = get_all_sub_elements(transitions_element, TAG_TRANSITION)
        for transition_element in transition_elements:
            transitions.append(XMLAPISchemaParser._parse_transition(transition_element, project_attributes))

        return transitions

    @staticmethod
    def _parse_compatible_job_definitions(compatible_job_definitions_element: ET.Element,
                                          job_definitions: typing.List[JobDefinition]) -> typing.List[JobDefinition]:
        # instantiate the output list
        compatible_job_definitions = []

        job_definition_ids = get_all_sub_elements_text(compatible_job_definitions_element, TAG_JOB_DEFINITION_ID,
                                                       False)

        for job_definition_id in job_definition_ids:
            for job_definition in job_definitions:
                if job_definition_id == job_definition.get_definition_id():
                    compatible_job_definitions.append(job_definition)

        return compatible_job_definitions

    @staticmethod
    def _parse_project_attribute(project_attribute_element: ET.Element,
                                 project_attributes: typing.List[ProjectAttribute],
                                 job_definitions: typing.List[JobDefinition]) -> ProjectAttribute:

        project_attribute_id = get_attribute(project_attribute_element, ATRRIBUTE_ID)

        # the project key is the same as it's id by default unless an alternative is provided
        key_element = project_attribute_element.find(TAG_KEY)
        project_attribute_key = key_element.text if key_element is not None else project_attribute_id

        project_attribute_display_name = get_text(project_attribute_element, TAG_DISPLAY_NAME)
        project_attribute_description = get_text(project_attribute_element, TAG_DESCRIPTION)
        project_attribute_type = get_text(project_attribute_element, TAG_TYPE)

        # get default value (optional)
        project_attribute_default_value_elements = project_attribute_element.findall(TAG_DEFAULT_VALUE)
        if project_attribute_default_value_elements:
            project_attribute_default_value = project_attribute_default_value_elements[0].text
        else:
            project_attribute_default_value = None

        # parse transitions
        transitions_element = get_sub_element(project_attribute_element, TAG_TRANSITIONS)
        project_attribute_transitions = XMLAPISchemaParser._parse_transitions(transitions_element, project_attributes)

        # parse compatible job definitions
        compatible_job_definitions_element = get_sub_element(project_attribute_element,
                                                             TAG_COMPATIBLE_JOB_DEFINITIONS)
        project_attribute_compatible_job_definitions = XMLAPISchemaParser._parse_compatible_job_definitions(
            compatible_job_definitions_element, job_definitions)

        if project_attribute_type == AttributeType.STRING.value:
            return StringProjectAttribute(project_attribute_id,
                                          project_attribute_key,
                                          project_attribute_display_name,
                                          project_attribute_description,
                                          project_attribute_transitions,
                                          project_attribute_compatible_job_definitions,
                                          default_value=project_attribute_default_value)

        elif project_attribute_type == AttributeType.ENUM.value:

            enum_items_element = get_sub_element(project_attribute_element, TAG_ITEMS)
            enum_items = XMLAPISchemaParser._parse_enum_items(enum_items_element)

            return EnumProjectAttribute(project_attribute_id,
                                        project_attribute_key,
                                        project_attribute_display_name,
                                        project_attribute_description,
                                        project_attribute_transitions,
                                        project_attribute_compatible_job_definitions,
                                        enum_items,
                                        default_value=project_attribute_default_value)

        elif project_attribute_type == AttributeType.NULL.value:
            return NullProjectAttribute(project_attribute_id,
                                        project_attribute_key,
                                        project_attribute_display_name,
                                        project_attribute_description,
                                        project_attribute_transitions,
                                        project_attribute_compatible_job_definitions)

        elif project_attribute_type == AttributeType.BOOLEAN.value:
            return BooleanProjectAttribute(project_attribute_id,
                                           project_attribute_key,
                                           project_attribute_display_name,
                                           project_attribute_description,
                                           project_attribute_transitions,
                                           project_attribute_compatible_job_definitions,
                                           default_value=project_attribute_default_value)
        else:
            raise ValueError("Unrecognised attribute type.")

    @staticmethod
    def _parse_project_attributes(api_schema_element: ET.Element,
                                  job_definitions: typing.List[JobDefinition]) -> typing.List[ProjectAttribute]:

        # instantiate the output list
        project_attributes: typing.List[ProjectAttribute] = []

        # parse project attributes
        project_attributes_element = get_sub_element(api_schema_element, TAG_PROJECT_ATTRIBUTES)
        project_attribute_elements = get_all_sub_elements(project_attributes_element, TAG_PROJECT_ATTRIBUTE)

        for project_attribute_element in project_attribute_elements:
            project_attributes.append(XMLAPISchemaParser._parse_project_attribute(project_attribute_element,
                                                                                  project_attributes,
                                                                                  job_definitions))

        return project_attributes

    @staticmethod
    def parse() -> APISchema:

        # parse the xml file using xml.etree.ElementTree
        tree = ET.parse(SCHEMA_DEFINITION_FILE)
        api_schema_element = tree.getroot()

        if api_schema_element.tag != TAG_API_SCHEMA:
            raise ValueError("API schema file must have a <" + TAG_API_SCHEMA + "> tag as the root")

        job_definitions = XMLAPISchemaParser._parse_job_definitions(api_schema_element)
        project_attributes = XMLAPISchemaParser._parse_project_attributes(api_schema_element, job_definitions)

        return APISchema(job_definitions, project_attributes)

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

from gridmarkets_blender_addon.meta_plugin.gridmarkets.api_schema import APISchema
from gridmarkets_blender_addon.meta_plugin.gridmarkets import constants
from gridmarkets_blender_addon.meta_plugin.job_definition import JobDefinition
from gridmarkets_blender_addon.meta_plugin.attribute import Attribute, AttributeType
from gridmarkets_blender_addon.meta_plugin.attribute_types import *
from gridmarkets_blender_addon.meta_plugin.job_attribute import JobAttribute
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute
from gridmarkets_blender_addon.meta_plugin.inference_source import InferenceSource
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


def get_sub_element(element: ET.Element,
                    tag_name: str,
                    expect_unique_tag: bool = True) -> typing.Optional[ET.Element]:

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

    if element.text is None:
        return ""

    return element.text


def get_text_optional(element: ET.Element, tag_name: str) -> typing.Optional[str]:
    elements = element.findall(tag_name)

    if len(elements) <= 0:
        return None

    if len(elements) > 1:
        raise ValueError("More than one optional '" + tag_name + "' tag.")

    return elements[0].text


def get_optional_number(element: ET.Element, tag_name: str) -> typing.Optional[int]:
    text = get_text_optional(element, tag_name)

    if text is None:
        return None

    return int(text)


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
TAG_SUBTYPE = "Subtype"
TAG_ITEMS = "Items"
TAG_KEY = "Key"
TAG_VALUE = "Value"
TAG_ATTRIBUTE = "Attribute"
TAG_JOB_ATTRIBUTE = "JobAttribute"
TAG_INFERENCE_SOURCES = "InferenceSources"
TAG_INFERENCE_SOURCE = "InferenceSource"
TAG_ATTRIBUTE_KEY_ATTRIBUTE = "key"
TAG_PROJECT_ATTRIBUTES = "ProjectAttributes"
TAG_PROJECT_ATTRIBUTE = "ProjectAttribute"
TAG_DEFAULT_VALUE = "DefaultValue"
TAG_TRANSITIONS = "Transitions"
TAG_TRANSITION = "Transition"
TAG_PROJECT_ATTRIBUTE_ID = "ProjectAttributeId"
ATTRIBUTE_ID = "id"
TAG_TRANSITION_FORMULA = "TransitionFormula"
TAG_COMPATIBLE_JOB_DEFINITIONS = "CompatibleJobDefinitions"
TAG_COMPATIBLE_JOB_DEFINITION = "CompatibleJobDefinition"
TAG_JOB_DEFINITION_ID = "JobDefinitionId"
TAG_MAX_LENGTH = "MaxLength"
TAG_MIN_LENGTH = "MinLength"
TAG_SUBTYPE_KWARGS = "SubtypeKwargs"
TAG_SUBTYPE_KWARG = "SubtypeKwarg"


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
    def _parse_subtype_kwargs(attribute_element: ET.Element):
        subtype_kwargs_attributes = get_all_sub_elements(attribute_element, TAG_SUBTYPE_KWARGS)

        if len(subtype_kwargs_attributes) > 1:
            raise ValueError("The <" + attribute_element.tag +
                             "> element must contain at most one <" + TAG_SUBTYPE_KWARGS + "> child element")

        subtype_kwargs = {}

        if len(subtype_kwargs_attributes):
            subtype_kwargs_attribute = subtype_kwargs_attributes[0]
            subtype_kwarg_attributes = get_all_sub_elements(subtype_kwargs_attribute, TAG_SUBTYPE_KWARG)
            for subtype_kwarg_attribute in subtype_kwarg_attributes:
                key = get_text(subtype_kwarg_attribute, TAG_KEY)
                value = get_text(subtype_kwarg_attribute, TAG_VALUE)
                subtype_kwargs[key] = value

        return subtype_kwargs


    @staticmethod
    def _parse_attribute(attribute_element: ET.Element) -> Attribute:
        attribute_key = get_text(attribute_element, TAG_KEY, expect_unique_tag=True)
        attribute_display_name = get_text(attribute_element, TAG_DISPLAY_NAME, expect_unique_tag=True)
        attribute_description = get_text(attribute_element, TAG_DESCRIPTION, expect_unique_tag=True)
        attribute_type = get_text(attribute_element, TAG_TYPE, expect_unique_tag=True)
        attribute_default_value = get_text_optional(attribute_element, TAG_DEFAULT_VALUE)
        attribute_subtype = get_text_optional(attribute_element, TAG_SUBTYPE)
        attribute_subtype_kwargs = XMLAPISchemaParser._parse_subtype_kwargs(attribute_element)

        if attribute_type == AttributeType.STRING.value:

            max_length = get_optional_number(attribute_element, TAG_MAX_LENGTH)
            min_length = get_optional_number(attribute_element, TAG_MIN_LENGTH)

            return StringAttributeType(attribute_key,
                                       attribute_display_name,
                                       attribute_description,
                                       attribute_subtype_kwargs,
                                       default_value=attribute_default_value,
                                       subtype=attribute_subtype,
                                       max_length=max_length,
                                       min_length=min_length)

        elif attribute_type == AttributeType.ENUM.value:

            if attribute_subtype == constants.ENUM_SUBTYPE_PRODUCT_VERSIONS:
                enum_items = []
            else:
                enum_items_element = get_sub_element(attribute_element, TAG_ITEMS)
                enum_items = XMLAPISchemaParser._parse_enum_items(enum_items_element)

            return EnumAttributeType(attribute_key,
                                     attribute_display_name,
                                     attribute_description,
                                     attribute_subtype_kwargs,
                                     enum_items,
                                     default_value=attribute_default_value,
                                     subtype=attribute_subtype)

        elif attribute_type == AttributeType.NULL.value:
            return NullAttributeType(attribute_key,
                                     attribute_display_name,
                                     attribute_description,
                                     attribute_subtype_kwargs)

        elif attribute_type == AttributeType.BOOLEAN.value:
            return BooleanAttributeType(attribute_key,
                                        attribute_display_name,
                                        attribute_description,
                                        attribute_subtype_kwargs,
                                        default_value=to_bool(attribute_default_value))

        elif attribute_type == AttributeType.INTEGER.value:
            return IntegerAttributeType(attribute_key,
                                        attribute_display_name,
                                        attribute_description,
                                        attribute_subtype_kwargs,
                                        default_value=int(attribute_default_value))

        else:
            raise ValueError("Unrecognised attribute type.")

    @staticmethod
    def _parse_job_inference_sources(inference_sources_element: ET.Element) -> typing.List[InferenceSource]:

        attribute_inference_sources: typing.List[str] = get_all_sub_elements_text(
            inference_sources_element, TAG_INFERENCE_SOURCE)

        return list(map(lambda x: InferenceSource.get_inference_source(x), attribute_inference_sources))

    @staticmethod
    def _parse_job_attribute(job_attribute_element: ET.Element) -> JobAttribute:
        attribute_element = get_sub_element(job_attribute_element, TAG_ATTRIBUTE, expect_unique_tag=True)
        attribute = XMLAPISchemaParser._parse_attribute(attribute_element)
        attribute_is_optional = to_bool(get_text(job_attribute_element, TAG_OPTIONAL))
        inference_sources_element = get_sub_element(job_attribute_element, TAG_INFERENCE_SOURCES)
        attribute_inference_sources = XMLAPISchemaParser._parse_job_inference_sources(inference_sources_element)

        return JobAttribute(attribute, attribute_inference_sources, attribute_is_optional)

    @staticmethod
    def _parse_job_definition(job_definition_element: ET.Element) -> JobDefinition:

        if ID_ATTRIBUTE not in job_definition_element.attrib:
            raise ValueError("All <" + TAG_JOB_DEFINITION + "> tags must contain an 'id' attribute")

        job_definition_id = get_attribute(job_definition_element, ID_ATTRIBUTE)
        job_definition_display_name = get_text(job_definition_element, TAG_DISPLAY_NAME)

        attribute_elements = get_all_sub_elements(job_definition_element, TAG_JOB_ATTRIBUTE, expect_at_least_one=True)

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

        job_definition_ids = get_all_sub_elements_text(compatible_job_definitions_element, TAG_COMPATIBLE_JOB_DEFINITION,
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

        project_attribute_id = get_attribute(project_attribute_element, ATTRIBUTE_ID)

        attribute_element = get_sub_element(project_attribute_element, TAG_ATTRIBUTE, expect_unique_tag=True)
        attribute = XMLAPISchemaParser._parse_attribute(attribute_element)

        # parse transitions
        transitions_element = get_sub_element(project_attribute_element, TAG_TRANSITIONS)
        project_attribute_transitions = XMLAPISchemaParser._parse_transitions(transitions_element, project_attributes)

        # parse compatible job definitions
        compatible_job_definitions_element = get_sub_element(project_attribute_element,
                                                             TAG_COMPATIBLE_JOB_DEFINITIONS)
        compatible_job_definitions = XMLAPISchemaParser._parse_compatible_job_definitions(
            compatible_job_definitions_element, job_definitions)

        return ProjectAttribute(project_attribute_id, attribute, project_attribute_transitions,
                                compatible_job_definitions)

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

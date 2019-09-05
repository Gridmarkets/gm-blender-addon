from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import RejectedTransitionInputError
from enum import Enum
import typing


class TransitionType(Enum):
    PROJECT_ATTRIBUTE = "PROJECT_ATTRIBUTE"
    JOB_DEFINITION = "JOB_DEFINITION"


class Transition:

    def __init__(self, transition_formula: str, project_attribute: 'ProjectAttribute' = None,
                 job_definitions: typing.List['JobDefinition'] = None):

        self._project_attribute = project_attribute
        self._job_definitions = job_definitions
        self._transition_formula = transition_formula

        if project_attribute is not None:
            self._type = TransitionType.PROJECT_ATTRIBUTE
        elif job_definitions is not None:
            self._type = TransitionType.JOB_DEFINITION
        else:
            raise ValueError("Unknown transition type")


def get_transition_type(self) -> TransitionType:
    return self._type


def get_transition_formula(self) -> str:
    return self._transition_formula


def get_project_attribute(self) -> 'ProjectAttribute':
    return self._project_attribute


def get_job_definitions(self) -> 'ProjectAttribute':
    return self._job_definitions


def transition(self, input: any):
    if self._transition_formula == '*':
        return self._node

    if type(input) == str:
        if self._transition_formula == input:
            return self._node

    if type(input) == int:
        if int(self._transition_formula) == input:
            return self._node

    raise RejectedTransitionInputError

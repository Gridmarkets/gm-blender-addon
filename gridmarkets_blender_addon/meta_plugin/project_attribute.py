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

__all__ = 'ProjectAttribute'

from abc import ABC, abstractmethod
import typing

from .errors import RejectedTransitionInputError

if typing.TYPE_CHECKING:
    from . import Attribute, JobDefinition, Transition


class ProjectAttribute(ABC):

    def __init__(self, id: str, attribute: 'Attribute', transitions: typing.List['Transition'],
                 compatible_job_definitions: typing.List['JobDefinition']):
        self._id = id
        self._attribute = attribute
        self._transitions = transitions
        self._compatible_job_definitions = compatible_job_definitions

    def get_id(self) -> str:
        return self._id

    def get_attribute(self) -> 'Attribute':
        return self._attribute

    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: any) -> None:
        raise NotImplementedError

    def has_transitions(self) -> bool:
        return len(self._transitions) > 0

    def get_transitions(self) -> typing.List['Transition']:
        return self._transitions

    def has_compatible_job_definitions(self) -> bool:
        return len(self._compatible_job_definitions) > 0

    def get_compatible_job_definitions(self) -> typing.List['JobDefinition']:
        return self._compatible_job_definitions

    def transition(self, input: any, force_transition: bool = False) -> 'ProjectAttribute':
        for transition in self._transitions:
            try:
                project_attribute = transition.transition(input)
                return project_attribute
            except RejectedTransitionInputError:
                pass

        # if there is only one possible transition then we can either
        if len(self.get_transitions()) == 1:
            transition = self.get_transitions()[0]
            # force the transition
            if force_transition:
                return transition.get_project_attribute()

            # or return a more specific error message if one exists
            message = transition.get_rejection_message()
        else:
            message = "Project attribute '" + self.get_attribute().get_display_name() + " (" + self.get_id() + ")" +\
                      "' does not have a transition that accepts the input value '" + str(input) + "'"

        raise RejectedTransitionInputError(message)

    def get_children(self) -> typing.List['ProjectAttribute']:
        return list(map(lambda x: x.get_project_attribute(), self.get_transitions()))

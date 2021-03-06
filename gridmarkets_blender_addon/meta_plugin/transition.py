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

__all__ = 'Transition'

import typing

from .errors import RejectedTransitionInputError

if typing.TYPE_CHECKING:
    from . import ProjectAttribute


class Transition:

    def __init__(self, transition_formula: str,
                 project_attribute: 'ProjectAttribute',
                 rejection_message: typing.Optional[str] = None):

        self._project_attribute = project_attribute
        self._transition_formula = transition_formula

        if rejection_message is None:
            self._rejection_message = "Transition input must satisfy " + self._transition_formula
        else:
            self._rejection_message = rejection_message

    def get_transition_formula(self) -> str:
        return self._transition_formula

    def get_project_attribute(self) -> 'ProjectAttribute':
        return self._project_attribute

    def get_rejection_message(self) -> str:
        return self._rejection_message

    def transition(self, input: any) -> 'ProjectAttribute':
        import re

        if re.match(self.get_transition_formula(), str(input)):
            return self.get_project_attribute()

        raise RejectedTransitionInputError

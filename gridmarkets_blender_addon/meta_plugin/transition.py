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

from gridmarkets_blender_addon.meta_plugin.errors.rejected_transition_input_error import RejectedTransitionInputError


class Transition:

    def __init__(self, transition_formula: str, project_attribute: 'ProjectAttribute'):

        self._project_attribute = project_attribute
        self._transition_formula = transition_formula

    def get_transition_formula(self) -> str:
        return self._transition_formula

    def get_project_attribute(self) -> 'ProjectAttribute':
        return self._project_attribute

    def transition(self, input: any) -> 'ProjectAttribute':
        import re

        if re.match(self.get_transition_formula(), str(input)):
            return self.get_project_attribute()

        raise RejectedTransitionInputError

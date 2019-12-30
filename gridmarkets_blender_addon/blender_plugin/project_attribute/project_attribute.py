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

import bpy
from gridmarkets_blender_addon import constants
from gridmarkets_blender_addon.meta_plugin.project_attribute import ProjectAttribute as MetaProjectAttribute


def get_project_attribute_value(project_attribute: MetaProjectAttribute) -> any:
    project_props = getattr(bpy.context.scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)
    return getattr(project_props, project_attribute.get_id())


def set_project_attribute_value(project_attribute: MetaProjectAttribute, value: any) -> None:
    project_props = getattr(bpy.context.scene, constants.PROJECT_ATTRIBUTES_POINTER_KEY)
    setattr(project_props, project_attribute.get_id(), value)

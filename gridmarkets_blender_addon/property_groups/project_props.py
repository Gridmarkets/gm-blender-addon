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


class ProjectProps(bpy.types.PropertyGroup):

    id: bpy.props.IntProperty(
        name="ID",
        description="A integer that is unique across all existing projects",
        min=0
    )

    name: bpy.props.StringProperty(
        name="Name",
        description="The name of your project as it will appear in envoy",
        default="",
        maxlen=256
    )

    status: bpy.props.StringProperty(
        name="Satus",
        description="The HTTP response of client.get_project_status for this project",
    )

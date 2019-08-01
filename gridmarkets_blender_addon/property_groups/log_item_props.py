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


class LogItemProps(bpy.types.PropertyGroup):

    body = bpy.props.StringProperty(
        name="Body",
        description="The body of the log message",
        default=""
    )

    level = bpy.props.EnumProperty(
        name="Level",
        description="The logging level of the item",
        items=[
            ('DEBUG', 'DEBUG', ''),
            ('INFO', 'INFO', ''),
            ('WARNING', 'WARNING', ''),
            ('ERROR', 'ERROR', '')
        ]
    )

    name = bpy.props.StringProperty(
        name="Name",
        description="Name of the logger which generated this item",
        default=""
    )

    date = bpy.props.StringProperty(
        name="Date",
        description="The date when this message was generated",
        default=""
    )

    time = bpy.props.StringProperty(
        name="Time",
        description="The time when this message was generated",
        default=""
    )

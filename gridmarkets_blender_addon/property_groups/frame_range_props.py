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


class FrameRangeProps(bpy.types.PropertyGroup):

    def get_frame_start(self):
        return self['frame_start']

    def get_frame_end(self):
        return self['frame_end']

    def set_frame_start(self, value):
        if 'frame_end' in self and value > self['frame_end']:
            self.frame_end = value

        self['frame_start'] = value

    def set_frame_end(self, value):
        if 'frame_start' in self and value < self['frame_start']:
            self.frame_start = value

        self['frame_end'] = value

    name: bpy.props.StringProperty(
        name="Range Name",
        description="Adding a name to your frame ranges makes them searchable",
        default="",
        maxlen=256,
        options={'SKIP_SAVE'}
    )

    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="If disabled the frame range will be ignored by Gridmarekts",
        default=True,
        options={'SKIP_SAVE'}
    )

    frame_start: bpy.props.IntProperty(
        name="Frame Start",
        description="First frame of the rendering range",
        default=1,
        min=0,
        get=get_frame_start,
        set=set_frame_start,
        options={'SKIP_SAVE'}
    )

    frame_end: bpy.props.IntProperty(
        name="Frame End",
        description="Final frame of the rendering range",
        default=255,
        min=0,
        get=get_frame_end,
        set=set_frame_end,
        options={'SKIP_SAVE'}
    )

    frame_step: bpy.props.IntProperty(
        name="Step Size",
        description="Number of frames to skip forward while rendering back each frame",
        default=1,
        min=1,
        options={'SKIP_SAVE'}
    )

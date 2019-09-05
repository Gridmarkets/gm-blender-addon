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
from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps


class VRayProps(bpy.types.PropertyGroup):
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of the job as it will show in the render manager",
        default="",
        maxlen=256
    )

    job_name: bpy.props.StringProperty(
        name="Job Name",
        description="The name of the job as it will show in the render manager",
        default="V-Ray Job",
        maxlen=256
    )

    frame_ranges: bpy.props.StringProperty(
        name="Frame Ranges",
        description="Defines the frame range in format start [end] [step],[start [end] [step]],...",
        default="1 1 1",
        maxlen=256
    )

    selected_frame_range: bpy.props.IntProperty()

    frame_ranges: bpy.props.CollectionProperty(
        type=FrameRangeProps
    )

    output_width: bpy.props.IntProperty(
        name="Output Width",
        description="Defines the render output width",
        default=1920,
        min=1
    )

    output_height: bpy.props.IntProperty(
        name="Output Height",
        description="Defines the render output height",
        default=1080,
        min=1
    )

    output_prefix: bpy.props.StringProperty(
        name="Output Prefix",
        description="Defines the render output file prefix",
        default="",
        maxlen=256
    )

    output_format: bpy.props.EnumProperty(
        name="Output Format",
        description="Defines the render output format",
        default="PNG",
        items={
            ("VRST", "VRayImage", ""),
            ("EXR", "OpenEXR", ""),
            ("SGI", "SGI", ""),
            ("TGA", "TGA", ""),
            ("TIFF", "TIFF", ""),
            ("JPEG", "JPEG", ""),
            ("PNG", "PNG", ""),
        }
    )

    output_path: bpy.props.StringProperty(
        name="Output Path",
        subtype="DIR_PATH",
        description="Defines the path to download the results to",
        default="",
        maxlen=256
    )

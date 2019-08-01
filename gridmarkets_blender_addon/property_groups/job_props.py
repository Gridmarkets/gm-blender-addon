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
from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps


class JobProps(bpy.types.PropertyGroup):

    id = bpy.props.IntProperty(
        name="ID",
        description="A integer that is unique across all existing jobs",
        min= 0
    )

    name = bpy.props.StringProperty(
        name="Name",
        description="The name of the job",
        default="",
        maxlen=256
    )

    # use project settings or overrided settings
    use_custom_frame_ranges = bpy.props.BoolProperty(
        name="Use custom frame range(s)",
        description="Choose between rendering custom frame ranges or using blenders standard animation frame range "
                    "settings",
        default=False,
    )

    # frame range collection
    frame_ranges = bpy.props.CollectionProperty(
        type=FrameRangeProps
    )

    selected_frame_range = bpy.props.IntProperty()

    use_custom_output_path = bpy.props.BoolProperty(
        name="Use custom output path",
        description="If this is option is selected this job will use the provided output path to output render results "
                    "to instead of Blender's output path",
        default=False
    )

    # output path
    output_path = bpy.props.StringProperty(
        name="Output Path",
        description="",
        default=constants.DEFAULT_OUTPUT_PATH,
        subtype='DIR_PATH'
    )

    use_custom_output_prefix = bpy.props.BoolProperty(
        name="Use custom output prefix",
        description="If this is option is selected this job will use the provided output prefix when naming ouput "
                    "files. The # characters are replaced by the frame number, and used to define zero padding."
                    "When the filename does not contain #, The suffix #### is added to the filename.",
        default=False
    )

    # prefix for output files
    output_prefix = bpy.props.StringProperty(
        name="Output Prefix",
        description="",
        default="GM_",
        maxlen=200,
    )

    use_custom_output_format = bpy.props.BoolProperty(
        name="Use custom output format",
        description="If this is option is selected this job will use the provided output format when outputting results",
        default=False
    )

    output_format = bpy.props.EnumProperty(
        name="Output Format",
        description="The output format to use when rendering the scene",
        items=[
            ("TGA", "TGA", ''),
            ("RAWTGA", "RAWTGA", ''),
            ("JPEG", "JPEG", ''),
            ("JPEG2000", "JPEG 2000", ''),
            ("IRIS", "IRIS", ''),
            ("PNG", "PNG", ''),
            ("TARGA", "Targa", ''),
            ("TARGA_RAW", "Targa Raw", ''),
            ("BMP", "BMP", ''),
            ("CINEON", "Cineon", ''),
            ("DPX", "DPX", ''),
            ("OPEN_EXR_MULTILAYER", "OpenEXR Multilayer", ''),
            ("EXR", "OpenEXR", ''),
            ("HDR", "Radiance HDR", ''),
            ("TIFF", "TIFF", '')
        ]
    )

    use_custom_render_engine = bpy.props.BoolProperty(
        name="Use custom render engine",
        description="If this is option is selected this job will override the scene render engine",
        default=False
    )

    render_engine = bpy.props.EnumProperty(
        name="Render Engine",
        description="The render engine to use when rendering the scene",
        items=[
            ("CYCLES", "Cycles", ''),
            ("BLENDER_RENDER", "Blender Internal", '')
        ]
    )

    render_device = bpy.props.EnumProperty(
        name="Render Device",
        description="The render device to use when rendering the scene",
        items=[
            (constants.RENDER_DEVICE_CPU, constants.RENDER_DEVICE_CPU, ''),
            (constants.RENDER_DEVICE_GPU, constants.RENDER_DEVICE_GPU, ''),
        ]
    )

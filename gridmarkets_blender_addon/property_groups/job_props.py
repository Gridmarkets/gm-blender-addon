import bpy
import constants

from property_groups.frame_range_props import FrameRangeProps


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
            ("IRIS", "IRIS", ''),
            ("PNG", "PNG", ''),
            ("RAWTGA", "RAWTGA", ''),
            ("BMP", "BMP", '')
        ]
    )

    use_custom_render_engine = bpy.props.BoolProperty(
        name="Use custom render engine",
        description="If this is option is selected this job will use the override the scene render engine",
        default=False
    )

    render_engine = bpy.props.EnumProperty(
        name="Render Engine",
        description="The render engine to use when rendering the scene",
        items=[
            ("CYCLES", "CYCLES", ''),
            ("BLENDER_RENDER", "BLENDER_RENDER", '')
        ]
    )

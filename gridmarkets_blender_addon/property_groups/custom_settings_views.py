import bpy


class CustomSettingsViews(bpy.types.PropertyGroup):

    frame_ranges_view = bpy.props.BoolProperty(default=False)

    output_path_view = bpy.props.BoolProperty(default=False)

    output_format_view = bpy.props.BoolProperty(default=False)

    render_engine_view = bpy.props.BoolProperty(default=False)

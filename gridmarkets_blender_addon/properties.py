import bpy
import constants

class GRIDMARKETS_PROPS_Addon_Properties(bpy.types.PropertyGroup):
    """Class to represent the main state of the plugin. Holds all the properties that are accessable via the interface."""
    
    # project name
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="The name of the project is optional, if it's not passed it will be inferred from project's root folder",
        default="",
        maxlen=1024,
        )
    
    # submission label
    submission_label: bpy.props.StringProperty(
        name="Submission Label",
        description="A string identifier for the submission (optional)",
        default="",
        maxlen=1024,
        )
    
    # artist name
    artist_name: bpy.props.StringProperty(
        name="Artist",
        description="The name of the Artist is optional",
        default="",
        maxlen=1024,
        )
        
    # submission comment
    submission_comment: bpy.props.StringProperty(
        name="Comment",
        description="",
        default="",
        maxlen=1024,
        )
    
    # use project settings or overrided settings
    override_project_render_settings: bpy.props.BoolProperty(
        name="Override project render settings",
        description="Determines if the projects default render settings are used to define the render range or if a different range should be used",
        default = False,
        )
    
    # frame start override
    render_frame_start: bpy.props.IntProperty(
        name = "Frame Start",
        description="First frame of the rendering range",
        default = 1,
        min = 0
        )
    
    # frame end override
    render_frame_end: bpy.props.IntProperty(
        name = "Frame End",
        description="Final frame of the rendering range",
        default = 255,
        min = 0
        )
    
    # frame step size override
    render_frame_step: bpy.props.IntProperty(
        name = "Step Size",
        description="Number of frames to skip forward while rendering back each frame",
        default = 1,
        min = 1
        )
    
    # output path
    output_path: bpy.props.StringProperty(
        name="Output Path",
        description="",
        default = constants.DEFAULT_OUTPUT_PATH,
        subtype = 'DIR_PATH'
        )
    
    # prefix for output files
    output_prefix: bpy.props.StringProperty(
        name="Output Prefix",
        description="",
        default = "",
        maxlen=200,
        )


def register():
    from bpy.utils import register_class
    
    # register properties
    register_class(GRIDMARKETS_PROPS_Addon_Properties)
    
    # register addon properties
    bpy.types.Scene.props = bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_Addon_Properties)


def unregister():
    from bpy.utils import unregister_class
    
    # unregister properties
    unregister_class(GRIDMARKETS_PROPS_Addon_Properties)
        
    # delete addon properties
    del bpy.types.Scene.props
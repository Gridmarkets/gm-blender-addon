import bpy
import constants
from utils import create_unique_object_name


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
        maxlen=256
    )

    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="If disabled the frame range will be ignored by Gridmarekts",
        default=True
    )

    frame_start: bpy.props.IntProperty(
        name="Frame Start",
        description="First frame of the rendering range",
        default=1,
        min=0,
        get=get_frame_start,
        set=set_frame_start
    )

    frame_end: bpy.props.IntProperty(
        name="Frame End",
        description="Final frame of the rendering range",
        default=255,
        min=0,
        get=get_frame_end,
        set=set_frame_end
    )

    frame_step: bpy.props.IntProperty(
        name="Step Size",
        description="Number of frames to skip forward while rendering back each frame",
        default=1,
        min=1
    )

class ProjectProps(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="Name",
        description="The name of your project as it will appear in envoy",
        default="",
        maxlen=256
    )


class JobProps(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="Name",
        description="The name of the job",
        default="",
        maxlen=256
    )

    # use project settings or overrided settings
    use_custom_frame_ranges: bpy.props.BoolProperty(
        name="Use custom frame ranges",
        description="Choose between rendering custom frame ranges or using blenders standard animation frame range "
                    "settings",
        default=False,
    )

    # frame range collection
    frame_ranges: bpy.props.CollectionProperty(
        type=FrameRangeProps
    )

    selected_frame_range: bpy.props.IntProperty()

    # output path
    output_path: bpy.props.StringProperty(
        name="Output Path",
        description="",
        default=constants.DEFAULT_OUTPUT_PATH,
        subtype='DIR_PATH'
    )

    # prefix for output files
    output_prefix: bpy.props.StringProperty(
        name="Output Prefix",
        description="",
        default="",
        maxlen=200,
    )



def _get_projects(scene, context):
    """ Returns a list of items representing project options """

    props = context.scene.props

    project_options = [
        # it is always an option to upload as a new project
        ('new project', "New Project", ""),  # (value, label, description)
    ]

    # iterate through uploaded projects and add them as options
    for i, project in enumerate(props.projects):
        project_options.append((i, project.name, ''))

    return project_options


class GRIDMARKETS_PROPS_Addon_Properties(bpy.types.PropertyGroup):
    """ Class to represent the main state of the plugin. Holds all the properties that are accessable via the interface.
    """


    
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

    # project collection
    projects: bpy.props.CollectionProperty(
        type=ProjectProps
    )

    selected_project: bpy.props.IntProperty()

    # projects enum
    project_options: bpy.props.EnumProperty(
        name="Projects",
        description="Apply Data to attribute.",
        items=_get_projects
    )

    # job collection
    jobs: bpy.props.CollectionProperty(
        type=JobProps
    )

    selected_job: bpy.props.IntProperty()


def set_default_job():
    """" Adds a default job to GRIDMARKETS_PROPS_Addon_Properties.jobs """
    jobs = bpy.context.scene.props.jobs

    # set default value if <bpy.context.scene.props.frame_ranges> is empty
    if not jobs:
        job = jobs.add()
        job.name = 'default job'

        job.use_custom_frame_ranges = False

        frame_range = job.frame_ranges.add()
        frame_range.name = create_unique_object_name(job.frame_ranges, name_prefix=constants.FRAME_RANGE_PREFIX)
        frame_range.enabled = True
        frame_range.frame_start = constants.DEFAULT_FRAME_RANGE_START_VALUE
        frame_range.frame_end = constants.DEFAULT_FRAME_RANGE_END_VALUE
        frame_range.frame_step = constants.DEFAULT_FRAME_RANGE_STEP_VALUE


def _on_register(scene):
    """ Called when the add-on is registered """
    set_default_job()

    # remove the handler once it has completed as it is no longer needed
    if _on_register in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_on_register)


@bpy.app.handlers.persistent
def _on_file_loaded(scene):
    """ This handler is needed to set the default value for <bpy.context.scene.props.frame_ranges> after any of the
    following events:
    - opening Blender
    - reloading the start-up file via the keys Ctrl N
    - opening any Blender file
    """

    set_default_job()


classes = (
    FrameRangeProps,
    ProjectProps,
    JobProps,
    GRIDMARKETS_PROPS_Addon_Properties,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    # register add-on properties
    bpy.types.Scene.props = bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_Addon_Properties)

    # add handler
    bpy.app.handlers.depsgraph_update_post.append(_on_register)
    bpy.app.handlers.load_post.append(_on_file_loaded)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

    # remove handler
    if _on_file_loaded in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_file_loaded)

    # delete add-on properties
    del bpy.types.Scene.props


import bpy
import constants


class LogItemProps(bpy.types.PropertyGroup):

    body: bpy.props.StringProperty(
        name="Body",
        description="The body of the log message",
        default=""
    )

    level: bpy.props.EnumProperty(
        name="Level",
        description="The logging level of the item",
        items=[
            ('DEBUG', 'DEBUG', ''),
            ('INFO', 'INFO', ''),
            ('WARNING', 'WARNING', ''),
            ('ERROR', 'ERROR', '')
        ]
    )

    name: bpy.props.StringProperty(
        name="Name",
        description="Name of the logger which generated this item",
        default=""
    )

    date: bpy.props.StringProperty(
        name="Date",
        description="The date when this message was generated",
        default=""
    )

    time: bpy.props.StringProperty(
        name="Time",
        description="The time when this message was generated",
        default=""
    )


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


class JobProps(bpy.types.PropertyGroup):

    id: bpy.props.IntProperty(
        name="ID",
        description="A integer that is unique across all existing jobs",
        min= 0
    )

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

    use_custom_output_path: bpy.props.BoolProperty(
        name="use custom output path",
        description="If this is option is selected this job will use the provided output path to output render results "
                    "to instead of Blender's output path",
        default=False
    )

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


def _get_project_options(scene, context):
    """ Returns a list of items representing project options """

    props = context.scene.props

    project_options = [
        # it is always an option to upload as a new project
        (constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE,
         constants.PROJECT_OPTIONS_NEW_PROJECT_LABEL,
         constants.PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION,
         'FILE_NEW', 0)
    ]

    # iterate through uploaded projects and add them as options
    for i, project in enumerate(props.projects):
        project_options.append((str(i + 1), project.name, '', '', project.id))

    return project_options


def _get_job_options(scene, context):
    """ Returns a list of items representing project options """

    props = context.scene.props

    job_options = [
        (constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE,
         constants.JOB_OPTIONS_BLENDERS_SETTINGS_LABEL,
         constants.JOB_OPTIONS_BLENDERS_SETTINGS_DESCRIPTION,
         'BLENDER', 0)
    ]

    # iterate through uploaded projects and add them as options
    for i, job in enumerate(props.jobs):
        job_options.append((str(i + 1), job.name, '', constants.JOB_ICON, job.id))

    return job_options


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
        name="Project",
        description="The list of possible projects to use on submit",
        items=_get_project_options
    )

    # job collection
    jobs: bpy.props.CollectionProperty(
        type=JobProps
    )

    selected_job: bpy.props.IntProperty()

    # jobs enum
    job_options: bpy.props.EnumProperty(
        name="Job",
        description="The list of possible jobs to use on submit",
        items=_get_job_options
    )

    selected_log_item: bpy.props.IntProperty(
        default=-1 # must be negative one otherwise the logic that selects new log items wont work
    )

    # logging items
    log_items: bpy.props.CollectionProperty(
        type=LogItemProps
    )

    show_log_dates: bpy.props.BoolProperty(
        name="Show Logged Dates",
        description="Toggles the displaying of dates for log items",
        default=False
    )

    show_log_times: bpy.props.BoolProperty(
        name="Show Logged Times",
        description="Toggles the displaying of times for log items",
        default=True
    )

    show_log_modules: bpy.props.BoolProperty(
        name="Show Logged Modules",
        description="Toggles the displaying of module names for log items",
        default=False
    )

    # upload project progress props
    uploading_project: bpy.props.BoolProperty(
        name="Uploading Project",
        description="Indicates that a project is being uploaded",
        default=False
    )

    uploading_project_progress: bpy.props.IntProperty(
        name="Uploading Project Progress",
        description="What percent of the project has been uploaded",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE'
    )

    uploading_project_status: bpy.props.StringProperty(
        name="Uploading Project Status",
        description="A brief description of the current status of the uploading operation",
        default="",
    )

    # submit operation progress props
    submitting_project: bpy.props.BoolProperty(
        name="Submitting Project",
        description="Indicates that a project is being submitted",
        default=False
    )

    submitting_project_progress: bpy.props.IntProperty(
        name="Submitting Project Progress",
        description="The progress made towards submitting this job",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE'
    )

    submitting_project_status: bpy.props.StringProperty(
        name="Submitting Project Status",
        description="A brief description of the current status of the submit operation",
        default="",
    )

    tab_options: bpy.props.EnumProperty(
        name="Tabs",
        description="The tabs that show at the top of the add-on main window",
        items=[
            (constants.TAB_SUBMISSION_SETTINGS, constants.TAB_SUBMISSION_SETTINGS, ''),
            (constants.TAB_PROJECTS, constants.TAB_PROJECTS, ''),
            (constants.TAB_JOB_PRESETS, constants.TAB_JOB_PRESETS, ''),
            (constants.TAB_CREDENTIALS, constants.TAB_CREDENTIALS, ''),
            (constants.TAB_LOGGING, constants.TAB_LOGGING, ''),
        ]
    )

    submission_summary_open: bpy.props.BoolProperty(
        name="Submission Summary Open",
        description="Whether or not the submission summary view is open",
        default=False
    )


classes = (
    LogItemProps,
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


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

    # delete add-on properties
    del bpy.types.Scene.props


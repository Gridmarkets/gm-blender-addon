import bpy
from bpy.app.handlers import persistent
from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.property_groups.frame_range_props import FrameRangeProps
from gridmarkets_blender_addon.property_groups.job_props import JobProps
from gridmarkets_blender_addon.property_groups.project_props import ProjectProps
from gridmarkets_blender_addon.property_groups.log_item_props import LogItemProps
from gridmarkets_blender_addon.property_groups.custom_settings_views import CustomSettingsViews


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
        job_options.append((str(i + 1), job.name, '', constants.ICON_JOB, job.id))

    return job_options


class GRIDMARKETS_PROPS_Addon_Properties(bpy.types.PropertyGroup):
    """ Class to represent the main state of the plugin. Holds all the properties that are accessible via the interface.
    """

    # artist name
    artist_name = bpy.props.StringProperty(
        name="Artist",
        description="The name of the Artist is optional",
        default="",
        maxlen=1024,
        )
        
    # submission comment
    submission_comment = bpy.props.StringProperty(
        name="Comment",
        description="",
        default="",
        maxlen=1024,
        )

    # project collection
    projects = bpy.props.CollectionProperty(
        type=ProjectProps,

    )

    selected_project = bpy.props.IntProperty(
        options=set()
    )

    # projects enum
    project_options = bpy.props.EnumProperty(
        name="Project",
        description="The list of possible projects to use on submit",
        items=_get_project_options,
    )

    # job collection
    jobs = bpy.props.CollectionProperty(
        type=JobProps
    )

    selected_job = bpy.props.IntProperty(
        options=set()
    )

    # jobs enum
    job_options = bpy.props.EnumProperty(
        name="Job",
        description="The list of possible jobs to use on submit",
        items=_get_job_options
    )

    selected_log_item = bpy.props.IntProperty(
        default=-1, # must be negative one otherwise the logic that selects new log items wont work
        options = set()
    )

    # logging items
    log_items = bpy.props.CollectionProperty(
        type=LogItemProps
    )

    show_log_dates = bpy.props.BoolProperty(
        name="Show Logged Dates",
        description="Toggles the displaying of dates for log items",
        default=False
    )

    show_log_times = bpy.props.BoolProperty(
        name="Show Logged Times",
        description="Toggles the displaying of times for log items",
        default=True
    )

    show_log_modules = bpy.props.BoolProperty(
        name="Show Logged Modules",
        description="Toggles the displaying of module names for log items",
        default=False
    )

    # upload project progress props
    uploading_project = bpy.props.BoolProperty(
        name="Uploading Project",
        description="Indicates that a project is being uploaded",
        default=False,
        options={'SKIP_SAVE'}
    )

    uploading_project_progress = bpy.props.IntProperty(
        name="Uploading Project Progress",
        description="What percent of the project has been uploaded",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE',
        options={'SKIP_SAVE'}
    )

    uploading_project_status = bpy.props.StringProperty(
        name="Uploading Project Status",
        description="A brief description of the current status of the uploading operation",
        default="",
    )

    # submit operation progress props
    submitting_project = bpy.props.BoolProperty(
        name="Submitting Project",
        description="Indicates that a project is being submitted",
        default=False,
        options={'SKIP_SAVE'}
    )

    submitting_project_progress = bpy.props.IntProperty(
        name="Submitting Project Progress",
        description="The progress made towards submitting this job",
        default=0,
        min=0,
        max=100,
        step=1,
        subtype='PERCENTAGE',
        options={'SKIP_SAVE'}
    )

    submitting_project_status = bpy.props.StringProperty(
        name="Submitting Project Status",
        description="A brief description of the current status of the submit operation",
        default="",
        options={'SKIP_SAVE'}
    )

    tab_options = bpy.props.EnumProperty(
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

    submission_summary_open = bpy.props.BoolProperty(
        name="Submission Summary Open",
        description="Whether or not the submission summary view is open",
        default=False
    )

    custom_settings_views = bpy.props.PointerProperty(type=CustomSettingsViews)



classes = (
    CustomSettingsViews,
    FrameRangeProps,
    JobProps,
    ProjectProps,
    LogItemProps,
    GRIDMARKETS_PROPS_Addon_Properties,
)


@persistent
def reset_to_defaults(pos):
    # options={'SKIP_SAVE'} doesnt work for global properties so we must reset manually
    bpy.context.scene.props.uploading_project = False
    bpy.context.scene.props.uploading_project_progress = 0
    bpy.context.scene.props.submitting_project = False
    bpy.context.scene.props.submitting_project_progress = 0
    bpy.context.scene.props.submitting_project_status = ""


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)

    # register add-on properties
    bpy.types.Scene.props = bpy.props.PointerProperty(type=GRIDMARKETS_PROPS_Addon_Properties)

    # add event handler
    bpy.app.handlers.load_post.append(reset_to_defaults)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

    # delete add-on properties
    del bpy.types.Scene.props

    # remove event handler
    bpy.app.handlers.load_post.remove(reset_to_defaults)


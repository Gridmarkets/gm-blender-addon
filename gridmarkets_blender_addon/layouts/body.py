import constants

from layouts import sidebar
from layouts.preferences import draw_preferences

from types import SimpleNamespace
from panels.console import GRIDMARKETS_PT_console
from panels.main import GRIDMARKETS_PT_Main
from panels.projects import GRIDMARKETS_PT_Projects
import utils_blender

from panels.jobs import GRIDMARKETS_PT_Jobs
from panels.output_settings import GRIDMARKETS_PT_Output_Settings


def _draw_jobs_panels(self, context):
    GRIDMARKETS_PT_Jobs.draw(self, context)
    if len(context.scene.props.jobs) > 0:
        GRIDMARKETS_PT_Output_Settings.draw(self, context)


def _draw_submission_summary(self, context):
    scene = context.scene
    props = scene.props
    open = props.submission_summary_open

    box = self.layout.box()

    col = box.column()
    row = col.row(align=True)
    row.alignment = 'LEFT'

    row.operator(
        constants.OPERATOR_TOGGLE_SUBMISSION_SUMMARY_ID_NAME,
        text="Submission Summary",
        icon=constants.ICON_DISCLOSURE_TRI_DOWN if open else constants.ICON_DISCLOSURE_TRI_RIGHT,
        emboss=False,
    )

    if open:
        split = col.split(percentage=0.2)
        labels = split.column()
        labels.label(text="Project: ")
        labels.separator()
        labels.label(text="Job: ")
        labels.label(text="App: ")
        labels.label(text="App Version: ")
        labels.label(text="GM Operation: ")
        labels.label(text="Path: ")
        labels.label(text="Frame range(s): ")
        labels.label(text="Output prefix: ")
        labels.label(text="Output format: ")
        labels.label(text="Output path: ")
        labels.label(text="Render Engine: ")
        labels.label(text="Resolution X: ")
        labels.label(text="Resolution Y: ")
        labels.label(text="Resolution %: ")
        labels.label(text="Frame Rate: ")


        values = split.column()
        if props.project_options == constants.PROJECT_OPTIONS_NEW_PROJECT_VALUE:
            values.label(text=constants.PROJECT_OPTIONS_NEW_PROJECT_DESCRIPTION)
        else:
            project = props.projects[int(props.project_options) - constants.PROJECT_OPTIONS_STATIC_COUNT]
            values.label(text=project.name)
        values.separator()

        if props.job_options == constants.JOB_OPTIONS_BLENDERS_SETTINGS_VALUE:
            values.label(text=constants.JOB_OPTIONS_BLENDERS_SETTINGS_LABEL)
        else:
            selected_job = props.jobs[int(props.job_options) - constants.JOB_OPTIONS_STATIC_COUNT]
            values.label(text=selected_job.name)

        # get a gridmarkets job. The render file doesnt matter for now
        job = utils_blender.get_job(context, "RENDER FILE")
        values.label(text=job.app)
        values.label(text=job.app_version)
        values.label(text=job.operation)
        values.label(text=job.path)
        values.label(text=job.params['frames'])
        values.label(text='' if job.params['output_prefix'] is None else job.params['output_prefix'] )
        values.label(text=job.params['output_format'])
        values.label(text=utils_blender.get_job_output_path_abs(context))
        values.label(text=job.params['engine'])
        values.label(text=str(scene.render.resolution_x))
        values.label(text=str(scene.render.resolution_y))
        values.label(text=str(scene.render.resolution_percentage) + ' %')
        values.label(text=str(scene.render.fps))


def _draw_compact_console(self, context):
    props = context.scene.props
    box = self.layout.box()
    box.alignment = "RIGHT"
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=4)


def draw_body(self, context):
    layout = self.layout
    props = context.scene.props

    # split to show the side bar
    split = layout.split(percentage=0.2)
    col = SimpleNamespace(layout=split.column())

    # draw the sidebar
    sidebar.draw_sidebar(col, context)

    # draw the main body
    col = split.column()
    box = col.box()
    row = box.row()
    row.prop(props, "tab_options", expand=True)
    col = SimpleNamespace(layout=col)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        GRIDMARKETS_PT_Main.draw(col, context)
        _draw_submission_summary(col, context)
        _draw_compact_console(col, context)
    elif props.tab_options == constants.TAB_PROJECTS:
        GRIDMARKETS_PT_Projects.draw(col, context)
        _draw_compact_console(col, context)
    elif props.tab_options == constants.TAB_JOB_PRESETS:
        _draw_jobs_panels(col, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(col, context)
    elif props.tab_options == constants.TAB_LOGGING:
        GRIDMARKETS_PT_console.draw(col, context)


import bpy
import constants
import utils_blender

from panels.main import GRIDMARKETS_PT_Main
from panels.projects import GRIDMARKETS_PT_Projects
from panels.jobs import GRIDMARKETS_PT_Jobs
from panels.preferences import GRIDMARKETS_PT_preferences
from panels.console import GRIDMARKETS_PT_console
from panels.output_settings import GRIDMARKETS_PT_Output_Settings

_old_USERPREF_PT_addons_draw_function = None
_old_USERPREF_HT_header_draw_function = None
_old_USERPREF_PT_navigation_bar_draw_function = None
_old_USERPREF_PT_save_preferences_draw_function = None


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
        split = col.split(factor=0.2)
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
        values.label(text=job.params['output_prefix'])
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
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=4, sort_lock=True)


def _draw_main_region(self, context):
    if context.screen.name == constants.INJECTED_SCREEN_NAME:
        layout = self.layout
        props = context.scene.props

        box = layout.box()
        row = box.row()
        row.prop_tabs_enum(props, "tab_options", icon_only=True)

        if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
            GRIDMARKETS_PT_Main.draw(self, context)
            _draw_submission_summary(self, context)
            _draw_compact_console(self, context)
        elif props.tab_options == constants.TAB_PROJECTS:
            GRIDMARKETS_PT_Projects.draw(self, context)
            _draw_compact_console(self, context)
        elif props.tab_options == constants.TAB_JOB_PRESETS:
            _draw_jobs_panels(self, context)
        elif props.tab_options == constants.TAB_CREDENTIALS:
            GRIDMARKETS_PT_preferences.draw(self, context)
        elif props.tab_options == constants.TAB_LOGGING:
            GRIDMARKETS_PT_console.draw(self, context)

    else:
        _old_USERPREF_PT_addons_draw_function(self, context)


def _draw_nav_region(self, context):
    if context.screen.name == constants.INJECTED_SCREEN_NAME:
        layout = self.layout
        props = context.scene.props

        layout.label(text="Links")

        col = layout.column()
        col.scale_x = 1
        col.scale_y = 2

        # Portal manager link
        col.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME, icon=constants.ICON_URL)

        # Cost calculator
        col.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME, icon=constants.ICON_URL)
        col.operator(constants.OPERATOR_OPEN_PREFERENCES_ID_NAME, icon=constants.ICON_PREFERENCES, text="Preferences")
        col.operator(constants.OPERATOR_OPEN_HELP_URL_ID_NAME, icon=constants.ICON_HELP)
    else:
        _old_USERPREF_PT_navigation_bar_draw_function(self, context)


def _draw_header_region(self, context):
    if context.screen.name == constants.INJECTED_SCREEN_NAME:
        from panels.main import GRIDMARKETS_PT_Main
        GRIDMARKETS_PT_Main.draw_header(self, context)
    else:
        _old_USERPREF_HT_header_draw_function(self, context)


def _draw_save_preferences_region(self, context):
    if context.screen.name == constants.INJECTED_SCREEN_NAME:
        pass;
    else:
        _old_USERPREF_PT_save_preferences_draw_function(self, context)


def register():

    print("register injections")

    global _old_USERPREF_PT_addons_draw_function
    global _old_USERPREF_HT_header_draw_function
    global _old_USERPREF_PT_navigation_bar_draw_function
    global  _old_USERPREF_PT_save_preferences_draw_function
    
    _old_USERPREF_PT_addons_draw_function = bpy.types.USERPREF_PT_addons.draw
    _old_USERPREF_HT_header_draw_function = bpy.types.USERPREF_HT_header.draw
    _old_USERPREF_PT_navigation_bar_draw_function = bpy.types.USERPREF_PT_navigation_bar.draw
    _old_USERPREF_PT_save_preferences_draw_function = bpy.types.USERPREF_PT_save_preferences.draw

    bpy.types.USERPREF_PT_addons.draw = _draw_main_region
    bpy.types.USERPREF_HT_header.draw = _draw_header_region
    bpy.types.USERPREF_PT_navigation_bar.draw = _draw_nav_region
    bpy.types.USERPREF_PT_save_preferences.draw = _draw_save_preferences_region


def unregister():
    bpy.types.USERPREF_PT_addons.draw = _old_USERPREF_PT_addons_draw_function
    bpy.types.USERPREF_HT_header.draw = _old_USERPREF_HT_header_draw_function
    bpy.types.USERPREF_PT_navigation_bar.draw = nav_bar = _old_USERPREF_PT_navigation_bar_draw_function
    bpy.types.USERPREF_PT_save_preferences.draw = _old_USERPREF_PT_save_preferences_draw_function

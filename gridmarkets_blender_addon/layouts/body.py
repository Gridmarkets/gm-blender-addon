from gridmarkets_blender_addon import constants

from gridmarkets_blender_addon.layouts.submission_settings import draw_submission_settings, draw_submission_summary
from gridmarkets_blender_addon.layouts.preferences import draw_preferences
from gridmarkets_blender_addon.layouts.projects import draw_projects
from gridmarkets_blender_addon.layouts.jobs import draw_jobs
from gridmarkets_blender_addon.layouts.console import draw_console, draw_compact_console


def draw_body(self, context):
    layout = self.layout
    props = context.scene.props

    box = layout.box()
    row = box.row()
    row.prop_tabs_enum(props, "tab_options", icon_only=True)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        draw_submission_settings(self, context)
        draw_submission_summary(self, context)
        draw_compact_console(self, context)
    elif props.tab_options == constants.TAB_PROJECTS:
        draw_projects(self, context)
        draw_compact_console(self, context)
    elif props.tab_options == constants.TAB_JOB_PRESETS:
        draw_jobs(self, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(self, context)
    elif props.tab_options == constants.TAB_LOGGING:
        draw_console(self, context)

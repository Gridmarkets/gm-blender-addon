import constants

from layouts.submission_settings import draw_submission_settings, draw_submission_summary
from layouts.preferences import draw_preferences
from layouts.projects import draw_projects
from layouts.jobs import draw_jobs
from layouts.console import draw_console, draw_compact_console


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

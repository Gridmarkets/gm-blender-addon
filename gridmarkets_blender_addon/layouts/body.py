from types import SimpleNamespace
import constants

from layouts.submission_settings import draw_submission_settings, draw_submission_summary
from layouts.preferences import draw_preferences
from layouts.projects import draw_projects
from layouts.jobs import draw_jobs
from layouts.console import draw_console, draw_compact_console
from layouts.sidebar import draw_sidebar


def draw_body(self, context):
    layout = self.layout
    props = context.scene.props

    # split to show the side bar
    split = layout.split(percentage=0.2)
    col = SimpleNamespace(layout=split.column())

    # draw the sidebar
    draw_sidebar(col, context)

    # draw the main body
    col = split.column()
    box = col.box()
    row = box.row()
    row.prop(props, "tab_options", expand=True)
    col = SimpleNamespace(layout=col)

    if props.tab_options == constants.TAB_SUBMISSION_SETTINGS:
        draw_submission_settings(col, context)
        draw_submission_summary(col, context)
        draw_compact_console(col, context)
    elif props.tab_options == constants.TAB_PROJECTS:
        draw_projects(col, context)
        draw_compact_console(col, context)
    elif props.tab_options == constants.TAB_JOB_PRESETS:
        draw_jobs(col, context)
    elif props.tab_options == constants.TAB_CREDENTIALS:
        draw_preferences(col, context)
    elif props.tab_options == constants.TAB_LOGGING:
        draw_console(col, context)

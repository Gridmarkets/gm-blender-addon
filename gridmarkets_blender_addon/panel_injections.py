import bpy
import constants
from types import SimpleNamespace

from panels.main import GRIDMARKETS_PT_Main
from panels.projects import GRIDMARKETS_PT_Projects
from panels.jobs import GRIDMARKETS_PT_Jobs
from panels.preferences import GRIDMARKETS_PT_preferences
from panels.console import GRIDMARKETS_PT_console
from panels.frame_ranges import GRIDMARKETS_PT_frame_ranges
from panels.output_settings import GRIDMARKETS_PT_Output_Settings

_old_USERPREF_PT_addons_draw_function = None
_old_USERPREF_HT_header_draw_function = None
_old_USERPREF_PT_navigation_bar_draw_function = None


def _draw_jobs_panels(self, context):
    GRIDMARKETS_PT_Jobs.draw(self, context)
    if len(context.scene.props.jobs) > 0:
        GRIDMARKETS_PT_frame_ranges.draw_header(self, context)
        GRIDMARKETS_PT_frame_ranges.draw(self, context)
        GRIDMARKETS_PT_Output_Settings.draw(self, context)

def _draw_submission_summary(self, context):
    box = self.layout.box()
    box.label(text="Submission Summary")

def _draw_compact_console(self, context):
    props = context.scene.props
    box = self.layout.box()
    box.alignment = "RIGHT"
    box.template_list("GRIDMARKETS_UL_log", "", props, "log_items", props, "selected_log_item", rows=4,
                      sort_lock=True)

def register():
    _old_USERPREF_PT_addons_draw_function = bpy.types.USERPREF_PT_addons.draw
    _old_USERPREF_HT_header_draw_function = bpy.types.USERPREF_HT_header.draw
    _old_USERPREF_PT_navigation_bar_draw_function = bpy.types.USERPREF_PT_navigation_bar.draw

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
            # col = layout.row(align=True)
            col.operator(constants.OPERATOR_OPEN_MANAGER_PORTAL_ID_NAME, icon='URL')

            # Cost calculator
            col.operator(constants.OPERATOR_OPEN_COST_CALCULATOR_ID_NAME, icon='URL')
            col.operator(constants.OPERATOR_OPEN_PREFERENCES_ID_NAME, icon='PREFERENCES', text="Preferences")
            col.operator(constants.OPERATOR_OPEN_HELP_URL_ID_NAME, icon='HELP')
        else:
            _old_USERPREF_PT_navigation_bar_draw_function(self, context)

    def _draw_header_region(self, context):
        if context.screen.name == constants.INJECTED_SCREEN_NAME:
            from panels.main import GRIDMARKETS_PT_Main
            GRIDMARKETS_PT_Main.draw_header(self, context)
        else:
            _old_USERPREF_HT_header_draw_function(self, context)

    bpy.types.USERPREF_PT_addons.draw = _draw_main_region
    bpy.types.USERPREF_HT_header.draw = _draw_header_region
    bpy.types.USERPREF_PT_navigation_bar.draw = _draw_nav_region


def unregister():
    bpy.types.USERPREF_PT_addons.draw = _old_USERPREF_PT_addons_draw_function
    bpy.types.USERPREF_HT_header.draw = _old_USERPREF_HT_header_draw_function
    bpy.types.USERPREF_PT_navigation_bar.draw = nav_bar = _old_USERPREF_PT_navigation_bar_draw_function

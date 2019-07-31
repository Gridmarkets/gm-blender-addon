import bpy
from utils_blender import addon_draw_condition
from layouts.sidebar import draw_sidebar
from .panel_overloader import PanelOverloader

_instance = None


class NavigationBarOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_navigation_bar,
                         draw_sidebar,
                         overload_condition=addon_draw_condition)


def register():
    global _instance

    if _instance is None:
        _instance = NavigationBarOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

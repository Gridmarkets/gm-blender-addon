import bpy
from utils_blender import addon_draw_condition
from .panel_overloader import PanelOverloader

_instance = None


class TabsOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_tabs,
                         TabsOverloader._draw_tabs,
                         overload_condition=addon_draw_condition)

    @staticmethod
    def _draw_tabs(self, context):
        pass


def register():
    global _instance

    if _instance is None:
        _instance = TabsOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

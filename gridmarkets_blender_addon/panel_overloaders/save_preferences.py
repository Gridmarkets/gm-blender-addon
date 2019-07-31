import bpy
from utils_blender import addon_draw_condition
from layouts.empty import draw_empty
from .panel_overloader import PanelOverloader

_instance = None


class SavePreferencesOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_save_preferences,
                         draw_empty,
                         overload_condition=addon_draw_condition)


def register():
    global _instance

    if _instance is None:
        _instance = SavePreferencesOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

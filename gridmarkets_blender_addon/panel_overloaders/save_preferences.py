import bpy
from utils_blender import addon_draw_condition
from .panel_overloader import PanelOverloader

_instance = None


class SavePreferencesOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_save_preferences,
                         SavePreferencesOverloader._draw_method,
                         overload_condition=addon_draw_condition)

    @staticmethod
    def _draw_method(self, context):
        pass;


def register():
    global _instance

    if _instance is None:
        _instance = SavePreferencesOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

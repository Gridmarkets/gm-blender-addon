import bpy
from gridmarkets_blender_addon.utils_blender import addon_draw_condition
from gridmarkets_blender_addon.layouts.empty import draw_empty
from gridmarkets_blender_addon.panel_overloaders.panel_overloader import PanelOverloader

_instance = None


class TabsOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_tabs,
                         draw_empty,
                         overload_condition=addon_draw_condition)


def register():
    global _instance

    if _instance is None:
        _instance = TabsOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

import bpy
from gridmarkets_blender_addon.utils_blender import addon_draw_condition
from gridmarkets_blender_addon.layouts.body import draw_body
from gridmarkets_blender_addon.panel_overloaders.panel_overloader import PanelOverloader

_instance = None


class AddonsOverloader(PanelOverloader):

    def __init__(self):
        super().__init__(bpy.types.USERPREF_PT_addons,
                         draw_body,
                         overload_condition=addon_draw_condition)


def register():
    global _instance

    if _instance is None:
        _instance = AddonsOverloader()


def unregister():
    global _instance

    if _instance is not None:
        _instance = _instance.reset_panel()

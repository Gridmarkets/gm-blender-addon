import bpy

class GRIDMARKETS_UL_frame_range(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """ Defines how frame range item is drawn in a template list """

        row = layout.row()
        row.active = item.enabled

        # users should be familiar with the restrict render icon and understand what it denotes
        enabled_icon = ("RESTRICT_RENDER_OFF" if item.enabled else "RESTRICT_RENDER_ON")

        row.prop(item, "enabled", icon=enabled_icon, text="", emboss=item.enabled)
        row.label(text = item.name)
        row.prop(item, "frame_start", text="Start")
        row.prop(item, "frame_end", text="End")
        row.prop(item, "frame_step", text="Step")

    def invoke(self, context, event):
        pass


classes = (
    GRIDMARKETS_UL_frame_range,
)


def register():
    from bpy.utils import register_class

    # register classes
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    # unregister classes
    for cls in reversed(classes):
        unregister_class(cls)

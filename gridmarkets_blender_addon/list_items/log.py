import bpy


class GRIDMARKETS_UL_log(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        props = context.scene.props

        row = layout.row(align=True)
        row.alignment = 'LEFT'

        # line text
        row.alert = item.level == 'ERROR' # if the message is an error then colour red

        text = ''

        if item.date and props.show_log_dates:
            text = text + item.date + ' '

        if item.time and props.show_log_times:
            text = text + item.time + ' '

        if item.name and props.show_log_modules:
            text = text + item.name + ' '

        text = text + item.body

        row.label(text=text)


classes = (
    GRIDMARKETS_UL_log,
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

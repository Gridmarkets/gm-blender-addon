import bpy


class LogItemProps(bpy.types.PropertyGroup):

    body = bpy.props.StringProperty(
        name="Body",
        description="The body of the log message",
        default=""
    )

    level = bpy.props.EnumProperty(
        name="Level",
        description="The logging level of the item",
        items=[
            ('DEBUG', 'DEBUG', ''),
            ('INFO', 'INFO', ''),
            ('WARNING', 'WARNING', ''),
            ('ERROR', 'ERROR', '')
        ]
    )

    name = bpy.props.StringProperty(
        name="Name",
        description="Name of the logger which generated this item",
        default=""
    )

    date = bpy.props.StringProperty(
        name="Date",
        description="The date when this message was generated",
        default=""
    )

    time = bpy.props.StringProperty(
        name="Time",
        description="The time when this message was generated",
        default=""
    )

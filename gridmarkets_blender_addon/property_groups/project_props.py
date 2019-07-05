import bpy


class ProjectProps(bpy.types.PropertyGroup):

    id = bpy.props.IntProperty(
        name="ID",
        description="A integer that is unique across all existing projects",
        min=0
    )

    name = bpy.props.StringProperty(
        name="Name",
        description="The name of your project as it will appear in envoy",
        default="",
        maxlen=256
    )

    status = bpy.props.StringProperty(
        name="Satus",
        description="The HTTP response of client.get_project_status for this project"
    )

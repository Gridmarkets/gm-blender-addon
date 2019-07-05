import bpy


class FrameRangeProps(bpy.types.PropertyGroup):

    def get_frame_start(self):
        return self['frame_start']

    def get_frame_end(self):
        return self['frame_end']

    def set_frame_start(self, value):
        if 'frame_end' in self and value > self['frame_end']:
            self.frame_end = value

        self['frame_start'] = value

    def set_frame_end(self, value):
        if 'frame_start' in self and value < self['frame_start']:
            self.frame_start = value

        self['frame_end'] = value

    name: bpy.props.StringProperty(
        name="Range Name",
        description="Adding a name to your frame ranges makes them searchable",
        default="",
        maxlen=256
    )

    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="If disabled the frame range will be ignored by Gridmarekts",
        default=True
    )

    frame_start: bpy.props.IntProperty(
        name="Frame Start",
        description="First frame of the rendering range",
        default=1,
        min=0,
        get=get_frame_start,
        set=set_frame_start
    )

    frame_end: bpy.props.IntProperty(
        name="Frame End",
        description="Final frame of the rendering range",
        default=255,
        min=0,
        get=get_frame_end,
        set=set_frame_end
    )

    frame_step: bpy.props.IntProperty(
        name="Step Size",
        description="Number of frames to skip forward while rendering back each frame",
        default=1,
        min=1
    )

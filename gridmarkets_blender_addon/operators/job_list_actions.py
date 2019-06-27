import bpy
import constants
import utils


class GRIDMARKETS_OT_job_list_actions(bpy.types.Operator):
    """ Contains actions that can be performed on the project list menu """

    bl_idname = constants.OPERATOR_JOB_LIST_ACTIONS_ID_NAME
    bl_label = constants.OPERATOR_JOB_LIST_ACTIONS_LABEL

    action: bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")
        )
    )

    def invoke(self, context, event):
        props = context.scene.props
        index = props.selected_job

        # if the currently selected project does not exist then the only allowed action is 'ADD'
        try:
            item = props.jobs[index]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and index < len(props.jobs) - 1:
                props.selected_job += 1

            elif self.action == 'UP' and index >= 1:
                props.selected_job -= 1

            elif self.action == 'REMOVE':
                # the static default options value's are not necessarily a number
                if props.job_options.isnumeric():
                    selected_job_option = int(props.job_options)

                    # reset the pulldown list if the selected option is going to be deleted
                    if selected_job_option == index + constants.JOB_OPTIONS_STATIC_COUNT:
                        props.property_unset("job_options")

                props.jobs.remove(index)

                if props.selected_job > 0:
                    props.selected_job -= 1

        if self.action == 'ADD':
            # add a frame range to the list
            job = props.jobs.add()

            job.id = utils.get_unique_id(props.jobs)
            job.name = utils.create_unique_object_name(props.jobs, name_prefix=constants.JOB_PREFIX)
            job.use_custom_frame_ranges = False

            frame_range = job.frame_ranges.add()
            frame_range.name = utils.create_unique_object_name(job.frame_ranges, name_prefix=constants.FRAME_RANGE_PREFIX)
            frame_range.enabled = True
            frame_range.frame_start = constants.DEFAULT_FRAME_RANGE_START_VALUE
            frame_range.frame_end = constants.DEFAULT_FRAME_RANGE_END_VALUE
            frame_range.frame_step = constants.DEFAULT_FRAME_RANGE_STEP_VALUE

            props.selected_job = len(props.jobs) - 1

        return {"FINISHED"}


classes = (
    GRIDMARKETS_OT_job_list_actions,
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

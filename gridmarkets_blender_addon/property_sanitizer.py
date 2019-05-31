import uuid


class PropertySanitizer():
    """ Helper class which provides useful methods for getting and validating the values of user input fields"""

    @staticmethod
    def getJobName(props):

        jobName = props.submission_label

        # check if the job name has been entered
        if not isinstance(jobName, str) or len(jobName) <= 0:
            return 'job-' + uuid.uuid4().hex

        return jobName

    @staticmethod
    def getFrameRange(scene, props):
        """ returns the frame settings in a format suitable for the API (1 255 1)"""

        # use scene frame settings unless the user has overridden them
        if props.override_project_render_settings:
            return str(props.render_frame_start) + ' ' + str(props.render_frame_end) + ' ' + str(
                props.render_frame_step)
        else:
            return str(scene.frame_start) + ' ' + str(scene.frame_end) + ' ' + str(scene.frame_step)

    @staticmethod
    def getOutputPrefix(props):

        outputPrefix = props.output_prefix

        # check if the output prefix has been entered
        if not isinstance(outputPrefix, str) or len(outputPrefix) <= 0:
            # the Blender job submission API requires an output prefix but an if it's an empty string envoy wont auto
            # download the results.
            return "0"

        return outputPrefix

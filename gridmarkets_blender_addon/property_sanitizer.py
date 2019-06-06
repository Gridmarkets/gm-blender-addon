import uuid


class PropertySanitizer():
    """ Helper class which provides useful methods for getting and validating the values of user input fields"""

    @staticmethod
    def get_project_name(props, default_project_name ='Project-' + uuid.uuid4().hex):
        """ returns the project name or the default provided name if the user has not entered a name yet"""

        project_name = props.project_name

        # check if the project name has not been entered
        if not isinstance(project_name, str) or len(project_name) <= 0:
            return default_project_name

        return project_name

    @staticmethod

    def get_job_name(props):

        job_name = props.submission_label

        # check if the job name has been entered
        if not isinstance(job_name, str) or len(job_name) <= 0:
            return 'job-' + uuid.uuid4().hex

        return job_name


    @staticmethod
    def get_frame_ranges(scene, props):
        """ returns the frame settings in a format suitable for the API (1 255 1)"""

        # use scene frame settings unless the user has overridden them
        if props.use_custom_frame_ranges:

            # filter disabled frame ranges
            frame_ranges = filter( lambda frame_range: frame_range.enabled, props.frame_ranges)

            # join the frame_start, frame_end and frame_step properties
            frame_ranges = map( lambda r: ' '.join([str(r.frame_start), str(r.frame_end), str(r.frame_step)]),
                                frame_ranges)

            # join all frame ranges together
            return ','.join(frame_ranges)

        else:
            return str(scene.frame_start) + ' ' + str(scene.frame_end) + ' ' + str(scene.frame_step)

    @staticmethod
    def get_output_prefix(props):

        outputPrefix = props.output_prefix

        # check if the output prefix has been entered
        if not isinstance(outputPrefix, str) or len(outputPrefix) <= 0:
            # the Blender job submission API requires an output prefix but an if it's an empty string envoy wont auto
            # download the results.
            return "0"

        return outputPrefix

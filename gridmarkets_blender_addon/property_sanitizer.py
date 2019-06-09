import bpy
import pathlib
import uuid
import constants


class ValidationResponse():

    def __init__(self, error_message=None):

        self._error_message = error_message

        if error_message == None:
            self._is_valid = True
        else:
            self._is_valid = False

    def is_valid(self):
        """ Did the validation method pass

        :return: is the validation response valid
        :rtype: bool
        """

        return self._is_valid

    def is_invalid(self):
        """ Did the validation method fail

        :return: opposite of is_valid
        :rtype: bool
        """

        return not self.is_valid()

    def get_error_message(self):
        """ Getter

        :return: The error message explaining why validation failed
        :rtype: str
        """
        return self._error_message


class PropertySanitizer():
    """ Helper class which provides useful methods for getting and validating the values of user input fields"""

    @staticmethod
    def validate_credentials():
        """ Validator

        :return: Whether or not the user's authentication credentials are valid
        :rtype: ValidationResponse
        """

        # get the add-on preferences
        addon_prefs = bpy.context.preferences.addons[constants.ADDON_PACKAGE_NAME].preferences

        hasEmail = False
        hasKey = False

        # check an email address has been entered
        if isinstance(addon_prefs.auth_email, str) and len(addon_prefs.auth_email) > 0:
            hasEmail = True

        # check a auth key has been entered
        if isinstance(addon_prefs.auth_accessKey, str) and len(addon_prefs.auth_accessKey) > 0:
            hasKey = True

        # validate
        if (not hasEmail and not hasKey):
            return ValidationResponse("No Gridmarkets email address or access key provided." +
                                      constants.AUTHENTICATION_HELP_MESSAGE)
        elif (not hasEmail):
            return ValidationResponse("No Gridmarketes email address provided." + constants.AUTHENTICATION_HELP_MESSAGE)

        elif (not hasKey):
            return ValidationResponse("No Gridmarketes access key provided." + constants.AUTHENTICATION_HELP_MESSAGE)

        return ValidationResponse()


    @staticmethod
    def get_project_name(props, default_project_name ='Project-' + uuid.uuid4().hex):
        """ returns the project name or the default provided name if the user has not entered a name yet"""

        project_name = props.project_name

        # check if the project name has not been entered
        if not isinstance(project_name, str) or len(project_name) <= 0:
            return default_project_name

        return project_name

    @staticmethod
    def get_output_path(context, props):
        """ Returns the output path provided by the user """

        output_path = props.output_path

        # check if the project name has not been entered
        if not isinstance(output_path, str) or len(output_path) <= 0:
            output_path = constants.DEFAULT_OUTPUT_PATH

        # convert path to absolute format (if not already in it)
        output_path = pathlib.Path(bpy.path.abspath(output_path))

        return output_path

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


def register():
    pass


def unregister():
    pass
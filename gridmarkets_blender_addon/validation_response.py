class ValidationResponse:

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

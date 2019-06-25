import sys
import traceback

class InvalidInputError(Exception):

    def __init__(self, message=None):
        super(InvalidInputError, self).__init__(message)

        self._message = message

        try:
            self.traceback = traceback.extract_tb(sys.exc_info()[2])

        except AttributeError:
            self.traceback = None
            pass

    def __str__(self):
        msg = self._message or '<empty message>'

        return msg

    @property
    def user_message(self):
        return self._message

    def __repr__(self):
        return "%s(message=%r)" % (
            self.__class__.__name__,
            self._message)

import logging


def _report(level, msg, operator):
    """ helper function which takes a messages intended to be logged and converts it into one the blender can display
        properly using Operator.report().

    :param level: The logging level of the message
    :type level: enum
    :param msg: The logging message
    :type msg: str
    :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
    :type operator: bpy.types.Operator
    :rtype: void
    """

    # report each line individually because blender has problems with multi-line reports (They display backwards in the
    # info panel)
    for line in msg.splitlines():

        # replace tabs since the blender info console can not display them
        line = line.replace('\t', '   ')

        operator.report(level, line)


class BlenderLoggingWrapper:
    """
    A very simple wrapper class that wrappers a logging.Logger and exposes some basic functions. It is designed to be
    used from blender operators so they can optionally output messages to the user using Operator.report().
    """

    def __init__(self, logger):
        """ Constructor

        :param logger: The logger to wrap
        :type logger: logging.Logger
        """

        self._logger = logger

    def debug(self, msg, operator=None, *args, **kwargs):
        """
        :param msg: The debug message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            _report({'DEBUG'}, msg, operator)

        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, operator=None, *args, **kwargs):
        """
        :param msg: The info message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            _report({'INFO'}, msg, operator)

        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, operator=None, *args, **kwargs):
        """
        :param msg: The warning message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            _report({'WARNING'}, msg, operator)

        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, operator=None, *args, **kwargs):
        """
        :param msg: The error message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            _report({'ERROR'}, msg, operator)

        #self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, operator=None, *args, exc_info=True, **kwargs):
        """
        :param msg: The exception message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            # blender has no exception enum
            _report({'ERROR'}, msg, operator)

        self._logger.exception(msg, *args, exc_info, **kwargs)

    def critical(self, msg, operator=None, *args, **kwargs):
        """
        :param msg: The critical message
        :type msg: str
        :param operator: An instance of a Blender Operator which can be used to report the message to the blender ui
        :type operator: bpy.types.Operator
        :rtype: void
        """

        if operator:
            # blender has no critical enum
            _report({'ERROR'}, msg, operator)

        self._logger.critical(msg, *args, **kwargs)


def get_wrapped_logger(name):
    """ Alternate definition of logging.getLogger() only it returns a wrapped Logger instead. Useful for cutting down on
        the number of imports necessary when creating a wrapped logger.

    :param name: The name of the logger
    :type name: str
    :return: The wrapped Logger
    :rtype: BlenderLoggingWrapper
    """

    return BlenderLoggingWrapper(logging.getLogger(name))

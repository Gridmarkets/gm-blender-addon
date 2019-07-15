import pathlib
import tempfile
import atexit
import constants

def get_wrapped_logger():
    from blender_logging_wrapper import get_wrapped_logger
    return get_wrapped_logger(__name__)

class _AssociationTuple:
    """ A container class representing the relationship between a temporary directory, a preject and the preject's
        render file"""

    PROJECT_NOT_SET_FLAG = 'project_not_set'
    RENDER_FILE_NOT_SET = "render_file_not_set"

    def __init__(self, temp_directory, project = PROJECT_NOT_SET_FLAG, render_file = RENDER_FILE_NOT_SET):
        """ Constructor

        :param temp_directory: The path to the temporary directory used to hold the temporary files related to a project
        :type temp_directory: tempfile.TemporaryDirectory
        :param project: The actual project instance
        :type project: gridmarkets.Project
        :param render_file: The name of there render file
        :type render_file: str
        """

        self._temp_directory = temp_directory
        self._project = project
        self._render_file = render_file

    def associate(self, project, render_file):
        """ Adds the project and render_file to this Association.

        :param project: The project instance to associate with this temp directory
        :type project: gridmarkets.Project
        :param render_file: The name of the render file for this project
        :type render_file: str
        :rtype: void
        """

        self._project = project
        self._render_file = render_file

    def get_temp_dir_name(self):
        """ Getter

        :return: The path to the temporary directory used to hold the temporary files related to a project
        :rtype: str
        """

        if self._temp_directory is None:
            return constants.TEMPORARY_FILES_DELETED

        return self._temp_directory.name

    def get_project(self):
        """ Getter

        :return: The actual project instance
        :rtype: gridmarkets.Project
        """
        return self._project

    def get_render_file(self):
        """ Getter

        :return: The name of there render file
        :rtype: str
        """
        return self._render_file

    def get_relative_render_file(self):
        """ Getter

        :return: The job file to be run relative to the project name which is also the remote folder name.
        :rtype: str
        """
        return ("{0}/" + self.get_render_file()).format(self.get_project().name)

    def delete_temporary_directory(self):
        if self._temp_directory:
            try:
                self._temp_directory.cleanup()
                self._temp_directory = None

            # If the file cannot be cleaned up because it is being used by another process (it shouldn't be!)
            except OSError as e:
                # then log the problem and fail
                log = get_wrapped_logger()
                log.exception("OSError when attempting to clean up temporary files.")
                raise e


class TempDirectoryManager:
    """ Singleton class used for managing all temporary directories created by the add-on and makes sure they are
    deleted when no longer needed.
    """

    _instance = None

    def __init__(self):
        # prevent more than one instance from ever being created
        if TempDirectoryManager._instance:
            raise Exception("TempDirectoryManager should never be instantiated twice")

        self.associations = []

        # register a clean up function that gets called on exit
        atexit.register(self.clean_up)

        TempDirectoryManager._instance = self

    @staticmethod
    def get_temp_directory_manager():
        if TempDirectoryManager._instance:
            return TempDirectoryManager._instance

        return TempDirectoryManager()

    def get_temp_directory(self):
        """ Creates a new temporary directory

        :return: The path of the temporary directory
        :rtype: pathlib.Path
        """

        # create a new temp directory
        temp_dir = tempfile.TemporaryDirectory(prefix='gm-temp-dir-')

        # store the new temp directory so that it can be released later
        self.associations.append(_AssociationTuple(temp_dir))

        return pathlib.Path(temp_dir.name)

    def get_association_with_project_name(self, project_name):
        """ Gets the association with with the provided project name.

        :param project_name: The name of the project
        :type project_name: str
        :return: The Association containing the project with the same name or None if no such Association exists
        :rtype: _AssociationTuple
        """

        for association_tuple in self.associations:
            project = association_tuple.get_project()

            if project and type(project) is not str and project.name == project_name:
                return association_tuple

        return None

    def associate_with_temp_dir(self, temp_dir_name, project, render_file):
        """ Iterate through self.temp_dir and associate the provided project and render_file with the provided temp
            directory

        :param temp_dir_name: The name of the temporary directory
        :type temp_dir_name: str
        :param project: The project to associate with the temporary directory
        :type project: gridmarkets.Project
        :param render_file: The name of the render file
        :type render_file: str
        :rtype: void
        """

        existing_tuple = None
        for association_tuple in self.associations:
            existing_project = association_tuple.get_project()
            if existing_project and type(existing_project) is not str and existing_project.name == project.name:
                existing_tuple = association_tuple

        # if an association already exists with this project name
        if existing_tuple:
            # delete it's temporary directory
            existing_tuple.delete_temporary_directory()

            # remove it from the list
            self.associations.remove(existing_tuple)

        for association_tuple in self.associations:
            if association_tuple.get_temp_dir_name() == temp_dir_name:
                association_tuple.associate(project, render_file)
                break

    def clean_up(self):
        """ Iterates through all stored temporary directories and cleans them up """

        i = len(self.associations) - 1
        while i >= 0:
            self.associations[i].delete_temporary_directory()
            del self.associations[i]
            i = i - 1

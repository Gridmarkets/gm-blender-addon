import pathlib
import tempfile
import atexit


class _AssociationTuple:
    """ Class representing the relationship between a project and the temporary directory that it has been assigned """

    PROJECT_NOT_SET_FLAG = 'project_not_set'

    def __init__(self, temp_directory, project = PROJECT_NOT_SET_FLAG):
        self._temp_directory = temp_directory
        self._project = project

    def set_project(self, project):
        self._project = project

    def get_temp_dir(self):
        return self._temp_directory

    def get_project(self):
        return self._project


class TempDirectoryManager:
    """ Manages all temporary directories created by the add-on and makes sure they are deleted when no longer needed"""

    def __init__(self):
        self.temp_dirs = []
        atexit.register(self.clean_up)

    def get_temp_directory(self):
        """ Creates a new temporary directory

        :return: The path of the temporary directory
        :rtype: pathlib.Path
        """

        # create a new temp directory
        temp_dir = tempfile.TemporaryDirectory(prefix='gm-temp-dir-')

        # store the new temp directory so that it can be released later
        self.temp_dirs.append(_AssociationTuple(temp_dir))

        return pathlib.Path(temp_dir.name)

    def associate_project(self, temp_dir_name, project):
        """ Iterate through self.temp_dir and associate the provided project with the provided temp directory """

        for association_tuple in self.temp_dirs:
            if association_tuple.get_temp_dir().name == temp_dir_name:
                association_tuple.set_project(project)
                break

    def clean_up(self):
        """ Iterates through all stored temporary directories and cleans them up """

        i = len(self.temp_dirs) - 1
        while i >= 0:
            self.temp_dirs[i].get_temp_dir().cleanup()
            del self.temp_dirs[i]
            i = i - 1

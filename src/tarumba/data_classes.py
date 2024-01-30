# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's data classes"

from gettext import gettext as _

class Base:
    "Base data class"

    def __init__(self):
        """
        Initialize the dictionary.
        """

        self.dictionary = None

    def get(self, key):
        """
        Returns a configuration value.

        :param key: Configuration key
        :return: Configuration value
        """

        assert key in self.dictionary, _('invalid configuration key: %(key)s')
        return self.dictionary.get(key)

    def set(self, key, value):
        """
        Updates a configuration value.

        :param key: Configuration key
        :param value: Configuration value
        """

        assert key in self.dictionary, _('invalid configuration key: %(key)s')
        self.dictionary[key] = value

    def __str__(self):
        """
        Returns a string representation of the data.

        :return: String
        """

        return str(self.dictionary)

class ListArgs(Base):
    "Arguments used when listing files"

    def __init__(self):
        """
        Initialize the dictionary.
        """

        super().__init__()
        self.dictionary = {
            'archive': None,
            'columns': None,
            'files': None,
            'backend': None,
            'occurrence': None,
            'output': None,
            'password': None
        }

class AddArgs(Base):
    "Arguments used when adding files"

    def __init__(self):
        """
        Initialize the dictionary.
        """

        super().__init__()
        self.dictionary = {
            'archive': None,
            'contents': None,
            'files': None,
            'follow_links': None,
            'backend': None,
            'level': None,
            'overwrite': None,
            'owner': None,
            'password': None,
            'path': None,
            'tmp_dirs': None
        }

class ExtractArgs(Base):
    "Arguments used when extracting files"

    def __init__(self):
        """
        Initialize the dictionary.
        """

        super().__init__()
        self.dictionary = {
            'archive': None,
            'contents': None,
            'cwd': None,
            'files': None,
            'backend': None,
            'occurrence': None,
            'overwrite': None,
            'password': None,
            'path': None,
            'tmp_dir': None
        }

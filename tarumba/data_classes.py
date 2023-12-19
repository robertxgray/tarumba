# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's data classes"

from gettext import gettext as _

class Base:
    "Base data class"

    dictionary = {}

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

class AddArgs(Base):
    "Arguments used when adding files"

    dictionary = {
        'archive': None,
        'contents': None,
        'files': None,
        'follow_links': None,
        'form': None,
        'level': None,
        'overwrite': None,
        'path': None,
        'tmp_dirs': []
    }

class ExtractArgs(Base):
    "Arguments used when extracting files"

    dictionary = {
        'archive': None,
        'cwd': None,
        'files': None,
        'form': None,
        'last_file': None,
        'overwrite': None,
        'path': None,
        'tmp_dir': None
    }

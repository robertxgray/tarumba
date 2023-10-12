# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

class Format:
    "Abstract parent class for archive formats."

    def list_commands(self, archive):
        "Commands to list the archive contents."
        pass

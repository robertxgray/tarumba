# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's data classes"

from dataclasses import dataclass

from tarumba.format import format as t_format

@dataclass
class AddArgs:
    "Arguments used when adding files"

    archive: str
    contents: set
    files: list[str]
    follow_links: bool
    form: t_format.Format
    path: str
    tmp_dirs: list[(str, bool)]

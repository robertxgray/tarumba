# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba - The universal archive manager"

from tarumba import config

import gettext
import os

# Init locale
gettext.bindtextdomain('tarumba', os.path.join(config.BASE_PATH, 'locale'))
gettext.textdomain('tarumba')

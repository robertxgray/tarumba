# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba - The universal archive manager"

import gettext
import logging

# Init locale
gettext.bindtextdomain('tarumba', 'tarumba/locale')
gettext.textdomain('tarumba')

# Init logging
logging.basicConfig(format='tarumba: %(message)s')

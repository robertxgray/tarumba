# Copyright: (c) 2024, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"Tarumba's custom errors"


class BackendUnavailableError(Exception):
    "The backend is not available"


class InvalidOperationError(Exception):
    "The user requested an invalid operation"


class UpdateTarCompressedError(Exception):
    "Compressed tar archives cannot be updated"

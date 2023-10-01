# Copyright: (c) 2023, Félix Medrano
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from tarumba import parser

def main():
    """
    Main function.
    """

    args = parser.get_arguments()
    print(str(args))

if __name__ == '__main__':
    main()

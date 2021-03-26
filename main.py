import getopt
import sys
from integration import IntegrationProcessor


def argument_error_print():
    print(
        '\033[91m[!] Please specify the root path by using -i <root_folder_path> flag.')
    print(
        '\033[91m[!] Please specify the output file by using -o <path_to_output_file> flag.')


def main(argv):
    root_path = ''
    output_path = ''

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["path=", "output="])
    except getopt.GetoptError:
        argument_error_print()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            argument_error_print()
            sys.exit()
        elif opt in ("-i", "--path"):
            root_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg

    if root_path != '':
        IntegrationProcessor(root_path, output_path).integrate()
    else:
        argument_error_print()


if __name__ == "__main__":
    main(sys.argv[1:])

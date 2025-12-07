'''
Docstring for op_miniprojects.mini3.project2_task1_a
'''
import re
import sys
import argparse
import os

def main():
    '''
    Docstring for main
    '''
    parser = argparse.ArgumentParser(
        description="Remove lines from a file that match a given regex pattern."
    )

    parser.add_argument(
        "pattern",
        type=str,
        help="Regex pattern of file to find"
    )
    parser.add_argument(
        "dirpath",
        type=str,
        help="Directory where to start search"
    )

    args = parser.parse_args()
    dirpath = args.dirpath
    pattern = args.pattern

    if not os.path.exists(dirpath):
        print(f"\033[91mError: Path '{dirpath}' not found.\033[0m")
        sys.exit()
    if not os.path.isdir(dirpath):
        print(f"\033[91mError: '{dirpath}' is not a directory.\033[0m")
        sys.exit()


    try:
        regex = re.compile(pattern)
    except re.error:
        print("\033[91mError: Invalid regex pattern provided.\033[0m")
        sys.exit()

    matches_found = False
    try:
        for root, _, files in os.walk(dirpath):
            for file in files:
                if regex.search(file):
                    full_path = os.path.join(root, file)
                    print(full_path)
                    matches_found = True
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        print("\033[91m+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("FILE NOT FOUND ERROR")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")
        sys.exit()

    if not matches_found:
        print("\033[91mNo files found\033[0m")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()

'''
Docstring for op_miniprojects.mini3.project2_task1_a
'''
import re
import sys
import argparse

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
        help="Regex pattern of lines to remove."
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file to process."
    )
    parser.add_argument(
        '-i', "--inplace",
        action="store_true",
        help="Modify the file in place instead of printing the result."
    )

    args = parser.parse_args()
    filepath = args.filepath
    pattern = args.pattern
    if not isinstance(filepath, str) or not isinstance(pattern, str):
        print("\033[91m+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("INVALID INPUT")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")
        sys.exit()
    try:
        with open(args.filepath, 'r', encoding='utf-8') as file:
            text = file.readlines()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        print("\033[91m+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("FILE NOT FOUND ERROR")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")
        sys.exit()

    try:
        filtered = ''.join([line for line in text if not re.findall(rf'{pattern}', line)])
    except re.error:
        print("\033[91m+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("INVALID PATTERN")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")
        sys.exit()

    if args.inplace:
        with open(args.filepath, 'w', encoding='utf-8') as file:
            file.write(filtered)
    else:
        print(filtered)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()

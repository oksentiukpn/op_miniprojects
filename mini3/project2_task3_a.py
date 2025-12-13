'''
Docstring for op_miniprojects.mini3.project2_task1_a
'''
import argparse
import os
import re
from sys import exit as system32_termination
import zipfile


def pro_cleaning(path: str):
    '''
    Pro cleaning of all temp files

    :param path: Description
    :type path: str
    '''
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir_ in dirs:
            os.rmdir(os.path.join(root, dir_))
    if os.path.exists(path):
        os.rmdir(path)


def main():
    '''
    Docstring for main
    '''
    parser = argparse.ArgumentParser(
        description="Extract mathcing files from zip and zip them in archive"
    )

    parser.add_argument(
        "pattern",
        type=str,
        help="Match pattern"
    )
    parser.add_argument(
        "src",
        type=str,
        help="Source archive path"
    )
    parser.add_argument(
        "dst",
        type=str,
        help="Destination archive path"
    )

    args = parser.parse_args()
    pattern = args.pattern
    src = args.src
    dst = args.dst

    if not os.path.exists(src):
        print('\033[91mSource archive not found\033[0m')

    if not os.path.exists(src):
        print(f"\033[91mError: Path '{src}' not found.\033[0m")
        system32_termination()


    temp_dir = 'temp_dir'

    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        with zipfile.ZipFile(src, 'r') as z:
            z.extractall(temp_dir)

        regex = re.compile(pattern)
        to_archive = []

        for root, _, files in os.walk(temp_dir):
            for file in files:
                path = os.path.join(root, file)

                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if regex.search(f.read()):
                            to_archive.append(os.path.relpath(path, temp_dir))
                except (UnicodeDecodeError, PermissionError):
                    continue
        if to_archive:
            with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
                for path in to_archive:
                    z.write(os.path.join(temp_dir, path), arcname=path)
        else:
            print("No matching files found.")
    finally:
        if os.path.exists(temp_dir):
            pro_cleaning(temp_dir)


if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print('Handled \033[91mPermissionError\033[0m, give normal path please!^_^')
        system32_termination()

'''
Docstring for op_miniprojects.mini3.project2_task1_a
'''
import argparse
import os
from sys import exit as system32_termination
import zipfile


def main():
    '''
    Docstring for main
    '''
    parser = argparse.ArgumentParser(
        description="Copy files from src to dst archive"
    )

    parser.add_argument(
        "src",
        type=str,
        help="Source path"
    )
    parser.add_argument(
        "dst",
        type=str,
        help="Destination archive path"
    )

    args = parser.parse_args()
    src = args.src
    dst = args.dst

    if not os.path.exists(src):
        print('\033[91mSource file/dir not found\033[0m')

    if not os.path.exists(src):
        print(f"\033[91mError: Path '{src}' not found.\033[0m")
        system32_termination()
    to_add = []

    if os.path.isfile(src):
        to_add.append(src)
    elif os.path.isdir(src):
        items = os.listdir(src)
        for item in items:
            path = os.path.join(src, item)
            if os.path.isfile(path):
                to_add.append(path)
    else:
        print('Not a file and not a Directory')
        system32_termination()
    if not to_add:
        print('Nothing to add')
        system32_termination()

    try:
        with zipfile.ZipFile(dst, 'a', zipfile.ZIP_DEFLATED) as z:
            for file in to_add:
                z.write(file, arcname=os.path.basename(file))
    except zipfile.error:
        print('\033[91mCritical error when working with archive\033[0m')

if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print('Handled \033[91mPermissionError\033[0m, give normal path please!^_^')
        system32_termination()

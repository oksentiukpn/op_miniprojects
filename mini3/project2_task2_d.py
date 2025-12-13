'''
Docstring for op_miniprojects.mini3.project2_task1_a
'''
import argparse
import os
from sys import exit as system32_termination

def main():
    '''
    Docstring for main
    '''
    parser = argparse.ArgumentParser(
        description="Copytree programm"
    )

    parser.add_argument(
        "source",
        type=str,
        help="Source path"
    )
    parser.add_argument(
        "destination",
        type=str,
        help="Destination part"
    )

    args = parser.parse_args()
    src = args.source
    dst = args.destination

    if not os.path.exists(src):
        print(f"\033[91mError: Path '{src}' not found.\033[0m")
        system32_termination()
    if not os.path.isdir(src):
        print(f"\033[91mError: '{src}' is not a directory.\033[0m")
        system32_termination()
    if not os.path.exists(dst):
        os.makedirs(dst)
    if not os.path.isdir(dst):
        print(f"\033[91mError: '{dst}' Already exists, but is not a directory.\033[0m")
        system32_termination()

    def copy(src: str, dst: str):
        '''
        Recursively copies all files from src to dst
        '''
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            if os.path.isdir(src_item):
                copy(src_item, dst_item)
            else: # Copying by parts
                with open(src_item, 'rb') as f_src:
                    with open(dst_item, 'wb') as f_dst:
                        while True:
                            buf = f_src.read(1024*1024)
                            if not buf:
                                break
                            f_dst.write(buf)
    copy(src, dst)

if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print('Handled \033[91mPermissionError\033[0m, give normal path please!^_^')
        system32_termination()

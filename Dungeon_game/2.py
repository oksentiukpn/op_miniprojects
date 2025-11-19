# with open('map1.txt', 'r+', encoding='utf-8') as file:
#     my_map = file.readlines()
#     my_map = [list(i) for i in my_map]
#     treasures = []
#     for i, k in enumerate(my_map):
#         for j, e in enumerate(k):
#             if e == '¢':
#                 treasures.append(f'{i} {j}')
#     with open('treasures.txt', 'w', encoding='utf-8') as f:
#         f.write("\n".join(treasures))
print(
                "\033[38;2;255;0;0mT\033[38;2;255;127;0mR\033[38;2;255;255;0mU"
                "\033[38;2;0;255;0mE \033[38;2;0;0;255mW\033[38;2;75;0;130mI"
                "\033[38;2;148;0;211mN\033[38;2;255;20;147mN"
                "\033[38;2;0;206;209mE\033[38;2;255;255;255mR\033[0m"
            )

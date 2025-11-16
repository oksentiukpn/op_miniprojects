with open('map1.txt', 'r+', encoding='utf-8') as file:
    my_map = file.readlines()
    my_map = [list(i) for i in my_map]
    treasures = []
    for i, k in enumerate(my_map):
        for j, e in enumerate(k):
            if e == '¢':
                treasures.append(f'{i} {j}')
    with open('treasures.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(treasures))

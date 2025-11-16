'''
Dungeon rpg game
'''
import random
from time import sleep
import sys
import os
import msvcrt

ARROW_KEYS = {
    b'H': 'W',  # up arrow
    b'P': 'S',  # down arrow
    b'K': 'A',  # left arrow
    b'M': 'D',  # right arrow
}
DICE_RULES = """
══════════════════════════════════════════════
🎲 DICE GAME FARKLE ⚔️
══════════════════════════════════════════════

🎯 GOAL:
→ Score more points than your opponent before they do!

══════════════════════════════════════════════
✅ BASICS
──────────────────────────────────────────────
• Both players roll 6 dice 🎲🎲🎲🎲🎲🎲
• Your turn continues as long as you keep scoring ✨
• If your roll has NO scoring dice → ❌ FARKLE → you lose all points for this round!

══════════════════════════════════════════════
💰 SCORING
──────────────────────────────────────────────

🔥 SINGLE DICE
• 1 → ⭐ 100 points
• 5 → ⭐ 50 points

🔥 TRIPLE SETS (3 of a kind)
• 1-1-1 → ⭐ 1000 points
• 2-2-2 → ⭐ 200 points
• 3-3-3 → ⭐ 300 points
• 4-4-4 → ⭐ 400 points
• 5-5-5 → ⭐ 500 points
• 6-6-6 → ⭐ 600 points

🔥 STRAIGHT
• 1-2-3-4-5-6 → 🌈 1500 points

🔥 FOUR / FIVE / SIX OF A KIND
• 4 of a kind → ✨ double triple value (e.g., 4, 4, 4, 4) = 800
• 5 of a kind → ✨ triple triple value (e.g., 4, 4, 4, 4, 4) = 1600
• 6 of a kind → ✨ quadruple triple value (e.g., 4, 4, 4, 4, 4, 4) = 3200

══════════════════════════════════════════════
🎒 CHOOSING DICE
──────────────────────────────────────────────
After each roll:
• Set aside scoring dice ✅
• Re-roll remaining dice 🎲
• Stop ANYTIME to bank your points 💼
• But be careful — GREED brings FARKLE 😈

══════════════════════════════════════════════
⚠️ FARKLE RULE
──────────────────────────────────────────────
If a roll scores NOTHING:
→ ❌ Points from this turn are LOST
→ 🔄 Turn passes to opponent

══════════════════════════════════════════════
🔥 "HOT DICE"
──────────────────────────────────────────────
If ALL 6 dice score:
→ You get ALL dice back and keep rolling! ♾️

══════════════════════════════════════════════
🏆 WINNING
──────────────────────────────────────────────
First player to reach target score (2000) → 🏆 Champion!

══════════════════════════════════════════════

To start game type "start"
To quit type "quit"
⚠️!!!If you quit you will automatically loose
"""
DICES = ['''
+-------+
|       |
|   ●   |
|       |
+-------+
''',
'''
+-------+
| ●     |
|       |
|     ● |
+-------+
''',
'''
+-------+
| ●     |
|   ●   |
|     ● |
+-------+
''',
'''
+-------+
| ●   ● |
|       |
| ●   ● |
+-------+
''',
'''
+-------+
| ●   ● |
|   ●   |
| ●   ● |
+-------+
''',
'''
+-------+
| ●   ● |
| ●   ● |
| ●   ● |
+-------+
''']
with open('combinations.txt', 'r', encoding='utf-8') as file1:
    lines = file1.readlines()
    lines = dict([(line.strip()).split(' ') for line in lines])
    lines = {tuple(DICES[int(i)-1] for i in combo): int(points) for combo, points in lines.items()}
COMBINATIONS = lines

def bot_move() -> int:
    '''
    Automatically perform the bot move by rolling all dice,
    finding the most valuable combo and returning its score.
    '''

    dices = [DICES[random.choice(range(len(DICES)))] for _ in range(6)]
    print('\nBot rolls the dice!')
    printable = [dice.split('\n') for dice in dices]

    for row in range(len(printable[0])):
        print(f'\033[91m{'   '.join(printable[i][row] for i in range(3))}\033[0m')
    print()
    for row in range(len(printable[0])):
        print(f'\033[91m{'   '.join(printable[i][row] for i in range(3, 6))}\033[0m')

    combos = find_combinations('123456', dices)
    if not combos:
        print('Bot got zero combos this turn.')
        return 0
    points = max(combos, key=lambda item: item[1])[1]

    print(f'Bot chooses combo worth \033[92m{points}\033[0m points.')
    print('\033[93m=========================================\033[0m')
    sleep(2)
    return points

def find_combinations(choosen, dices) -> list:
    '''
    Finding combinations

    #>>> find_combinations('123456', [DICES[0], DICES[1], DICES[2], DICES[3], DICES[4], DICES[5]])
    '''

    choosen = [int(e) for e in choosen]
    choosen = [dices[i-1] for i in choosen]
    found = []
    counts = {}

    for d in choosen:
        counts[d] = counts.get(d, 0) + 1
    for combo, points in COMBINATIONS.items():
        need = {}
        for x in combo:
            need[x] = need.get(x, 0) + 1

        ok = True
        for x, y in need.items():
            if counts.get(x, 0) < y:
                ok = False
                break

        if ok:
            found.append((combo, points))

    return found

def check_combo(choosen, num_dices, dices) -> bool:
    '''
    Checking if valid combo given
    '''

    if not choosen or not ("".join(choosen)).isdigit() or len(choosen) > num_dices:
        return False
    if any(choosen.count(i) != 1 for i in choosen):
        return False
    if not find_combinations(choosen, dices):
        return False

    return True

def player_move(num_dices: int, combo_result) -> int:
    '''
    Player move
    '''

    passing = False

    print('Type <roll> to roll dices or <pass> to pass')
    while(input1:=input('\033[95m>>> \033[0m')) !='roll':
        if input1 == 'quit':
            return None
        if input1 == 'pass':
            return combo_result
        print('Wrong input!!!')

    dices = [DICES[random.choice(range(6))] for _ in range(num_dices)]
    zero = False # Check for combos

    for combo in COMBINATIONS:
        combos = {dice: combo.count(dice) for dice in combo}
        for item, value in combos.items():
            if value <= dices.count(item):
                continue
            break
        else:
            zero = False
            break
        zero = True

    print('YOUR DICES!!!')
    print('Dice numbers:')
    labels = [str(i + 1) for i in range(len(dices))]

    for start in range(0, len(labels), 3):
        print(f'\033[94m{'   '.join(labels[start:start+3])}\033[0m')
    printable = [dice.split('\n') for dice in dices]

    for start in range(0, len(printable), 3):
        chunk = printable[start:start+3]
        for row in range(len(chunk[0])):
            print(f'\033[94m{'   '.join(d[row] for d in chunk)}\033[0m')
        print()
    if zero:
        print('\033[91mZero combos, opponent`s turn!\033[0m')
        sleep(2.5)
        return 0

    print('Choose dices')
    print("Input format: dices: 1 2 3 or 4 3 2 or 1 or 1 2 3 4 5\nOr type \
pass to score and pass\nType quit to quit")

    while(input1:=input('\033[95m>>> \033[0m')) != 'quit':

        if input1 == 'pass':
            passing = True
            break
        choosen = [e for e in input1 if e != ' ']
        if not check_combo(choosen, num_dices, dices):
            print('\033[91mWrong input!!!\033[0m')
            continue

        remaining = choosen[:]
        scored_combos = []
        total_removed = 0

        while True:
            found = find_combinations(remaining, dices)
            if not found:
                break
            combo, points = found.pop()
            scored_combos.append((combo, points))
            combo_result += points
            total_removed += len(combo)
            for face in combo:
                for idx, die_idx in enumerate(remaining):
                    if dices[int(die_idx) - 1] == face:
                        remaining.pop(idx)
                        break

        if not scored_combos:
            print('\033[91mWrong input!!!\033[0m')
            continue

        num_dices -= total_removed
        print(f'\033[92mYour turn Balance: {combo_result}!\033[0m')
        break
    else:
        return None
    if num_dices == 0: # if all dices scored, you can make new turn
        num_dices = 6
    if passing:
        return combo_result
    return player_move(num_dices, combo_result)

def game() -> bool:
    '''
    Playing dice game
    '''
    # Creating dices
    player_points = 0
    bot_points = 0

    while player_points < 2000 and bot_points < 2000:
        player_plus = player_move(6, 0)
        if player_plus is None:
            return False
        player_points += player_plus
        bot_points += bot_move()
        print(f'BOT POINTS: \033[91m{bot_points}\033[0m')
        print(f'YOUR POINTS: \033[92m{player_points}\033[0m')
        print('\033[93m=========================================\033[0m')

    if player_points > bot_points:
        print('\033[92mYOU WIN!!!\033[0m')
    elif player_points == bot_points:
        print('\033[93mITS A DRAW!!!\033[0m')
    else:
        print('\033[91mYOU LOST!!!\033[0m')

    return player_points >= bot_points

def draw_map(variables) -> str:
    '''
    Generating map for the game
    '''

    def display_map(my_map: list, coins: int):
        '''
        Printing map
        '''
        os.system('cls' if os.name == 'nt' else 'clear') # clear terminal
        print(f"Your coins: {coins}")
        print('\n'.join(["".join(i) for i in my_map]))

    # variables = {0: blocks, 1: coins, 2: treasures, 3: has_key, 4: pos}
    blocks = variables[0]
    coins = variables[1]
    treasures = variables[2]
    has_key = variables[3]
    pos = variables[4]
    etap = variables[5]
    hp = variables[6]

    match etap:
        case 0:
            file_path = 'map1.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        my_map = file.read()

    my_map = my_map.split('\n')
    my_map = [list(i) for i in my_map]


    ############################################################
    # blocking directions if its wall or door
    try:
        blocks['D'] = my_map[pos[1]][pos[0]+2] == '#'
        blocks['A'] = my_map[pos[1]][pos[0]-2] == '#'
        blocks['W'] = my_map[pos[1]-1][pos[0]] == '#'
        blocks['S'] = my_map[pos[1]+1][pos[0]] == '#'
        if not has_key:
            if my_map[pos[1]][pos[0]+2] == '=':
                blocks['D'] = True
            if my_map[pos[1]][pos[0]-2] == '=':
                blocks['A'] = True
            if my_map[pos[1]-1][pos[0]] == '=':
                blocks['W'] = True
            if my_map[pos[1]+1][pos[0]] == '=':
                blocks['S'] = True
    except IndexError:
        pass

    visible_radius = 5

    if pos in treasures:
        my_map[pos[1]][pos[0]] = '?'
        coins += 1
        treasures.remove(pos)

    if pos == (3, 7):
        print(pos)
        has_key = True

    my_map[pos[1]][pos[0]] = '\033[92m𓀚\033[0m'
    ############################################################
    for index, value in enumerate(my_map): # colorize and draw visible area
        for j_index, j_value in enumerate(value):

            distance = max(abs((pos[0] - j_index)/2), abs(pos[1] - index))

            match j_value:
                case '¢':
                    if distance <= visible_radius:
                        if (j_index, index) not in treasures:
                            my_map[index][j_index] = ' '
                        else:
                            my_map[index][j_index] = '\033[93m¢\033[0m'
                    else:
                        my_map[index][j_index] = '\033[90m?\033[0m'
                case '?':
                    if distance <= visible_radius:
                        my_map[index][j_index] = ' '
                    else:
                        my_map[index][j_index] = '\033[90m?\033[0m'
                case '#':
                    my_map[index][j_index] = '\033[91m▒\033[0m'
                case '⚷':
                    if distance <= visible_radius:
                        if has_key and (j_index, index) != pos:
                            my_map[index][j_index] = ' '
                        else:
                            my_map[index][j_index] = '\033[93m⚷\033[0m'
                    else:
                        my_map[index][j_index] = '\033[90m?\033[0m'

    display_map(my_map, coins)

    n = random.choice(range(30))
    if n == 0: # Minigame appearing
        win = False
        print('\033[91mITS A TRAP!!!\033[0m')
        print('Type skip to skip rules')
        print('Type start to draw rules')
        while(input1:=input('\033[95m>>> \033[0m')) !='start':
            if input1 == 'skip':
                print(DICE_RULES)
                break
            print('Wrong input!!!')
        else:
            for char in DICE_RULES:
                sys.stdout.write(char)
                sys.stdout.flush()
                if char in '═─':
                    speed = 0.001
                else:
                    speed = 0.02
                if char in ".!?":
                    sleep(5*speed)
                elif char == "\n":
                    sleep(10*speed)
                else:
                    sleep(speed)
        while(input1:=input('\033[95m>>> \033[0m')) !='start':
            if input1 == 'quit':
                break
            print('Wrong input!!!')
        else:
            win = game()
        if not win:
            hp -= 20
        if hp <= 0:
            print('!You lost all!💀💀💀')
            print('\033[91mGG\033[0m')
            sys.exit()
        sleep(3)
        display_map(my_map, coins)
    variables = {0: blocks, 1: coins, 2: treasures, 3: has_key, 4: pos, 5: etap, 6: hp}
    move(variables)

def draw_rules() -> None:
    '''
    Just drawing rules in start of the game
    '''
    print('Rules:')

def move(variables):
    '''
    I like to move it
    '''
    def read_direction():
        print('\033[95m>>> \033[0m', end='', flush=True)
        while True:
            key = msvcrt.getch()
            if key == b'\r':
                continue  # ignore Enter
            if key == b'\xe0':  # special key prefix
                key = msvcrt.getch()
                if key in ARROW_KEYS:
                    print()  # move to next line
                    return ARROW_KEYS[key]
            elif key.lower() in b'wasd':
                print(key.decode().upper())
                return key.decode().upper()
            elif key == b'q':
                return 'quit'
    blocks = variables[0]
    coins = variables[1]
    treasures = variables[2]
    has_key = variables[3]
    pos = variables[4]
    etap = variables[5]
    hp = variables[6]
    direction = read_direction()

    if direction == 'quit':
        exit()
    if direction == 'startminigame':
        game()
    direction = direction.upper()
    if len(direction) != 1 or direction not in 'WASD':
        move(variables)
    if not blocks[direction]:
        match direction:
            case 'W':
                if pos[1] > 0:
                    pos = (pos[0], pos[1] - 1)
            case 'S':
                if pos[1] < 49:
                    pos = (pos[0], pos[1] + 1)
            case 'A':
                if pos[0] > 3:
                    pos = (pos[0] - 2, pos[1])
            case 'D':
                if pos[0] > 0:
                    pos = (pos[0] + 2, pos[1])
    variables = {0: blocks, 1: coins, 2: treasures, 3: has_key, 4: pos, 5: etap, 6: hp}

    draw_map(variables)


if __name__ == '__main__':
    def main():
        '''
        Main function for programm
        '''

        blocks = {'W': True, 'A': True, 'S': False, 'D': False}
        coins = 0
        etap = 0
        pos = (3, 1)
        has_key = False
        treasures = []
        hp = 100
        a = 0.0 # Добавив float
        a = a*a
        with open('treasures.txt', 'r', encoding='utf-8') as file:
            treasures = [(i.strip('\n')) for i in file]
            treasures = [i.split(" ") for i in treasures]
            treasures = [(int(i[1]), int(i[0])) for i in treasures]
        variables = {0: blocks, 1: coins, 2: treasures, 3: has_key, 4: pos, 5: etap, 6: hp}
        draw_map(variables)

    main()
    import doctest
    print(doctest.testmod())

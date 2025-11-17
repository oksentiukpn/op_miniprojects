'''
Dungeon rpg game
'''
import random
from time import sleep, perf_counter
import sys
import os
from typing import List
try:
    import msvcrt
except ImportError:  # pragma: no cover - fallback for non-Windows platforms
    msvcrt = None
try:  # pragma: no cover - Windows builds do not provide these modules
    import termios  # type: ignore
    import tty  # type: ignore
except ImportError:
    termios = None  # type: ignore
    tty = None  # type: ignore

ARROW_KEYS = {
    b'H': 'W',  # up arrow
    b'P': 'S',  # down arrow
    b'K': 'A',  # left arrow
    b'M': 'D',  # right arrow
}
POSIX_ARROW_KEYS = {
    b'A': 'W',
    b'B': 'S',
    b'C': 'D',
    b'D': 'A',
}



def rolling_animation(num_dices: int, duration: float = 2.0, refresh: float = 0.1,
                      prefix: str = 'Rolling dice') -> None:
    '''
    Animate dice rolling by rapidly showing random ASCII dice faces.
    '''
    if num_dices <= 0:
        return
    end_time = perf_counter() + duration
    printed_lines = 0
    while perf_counter() < end_time:
        animated = [random.choice(DICES) for _ in range(num_dices)]
        block = f'{prefix}...\n{format_dice_rows(animated, color="\033[96m")}'
        line_count = block.count('\n') + 1
        if printed_lines:
            sys.stdout.write(f'\033[{printed_lines}A')
            sys.stdout.write('\033[J')
        print(block)
        sys.stdout.flush()
        printed_lines = line_count
        sleep(refresh)
    if printed_lines:
        sys.stdout.write(f'\033[{printed_lines}A')
        sys.stdout.write('\033[J')
        sys.stdout.flush()

def get_single_keypress() -> bytes:
    '''
    Platform-independent single key reader.
    '''
    if msvcrt is not None:
        return msvcrt.getch()
    if termios is None or tty is None:
        raise RuntimeError('Terminal control modules unavailable on this platform')
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
        if char == '\x1b':
            char += sys.stdin.read(1)
            if char.endswith('['):
                while True:
                    next_char = sys.stdin.read(1)
                    char += next_char
                    if next_char.isalpha() or next_char == '~':
                        break
        return char.encode()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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

def format_dice_rows(dices: List[str], color: str = '\033[94m',
                     include_labels: bool = False) -> str:
    '''
    Create a printable block of dice faces; optionally include numeric labels.
    '''
    if not dices:
        return ''
    lines_ = []
    if include_labels:
        labels = [str(i + 1) for i in range(len(dices))]
        for start in range(0, len(labels), 3):
            slice_labels = '   '.join(labels[start:start + 3])
            lines_.append(f'{color}{slice_labels}\033[0m')
    printable = [dice.split('\n') for dice in dices]
    for start in range(0, len(printable), 3):
        chunk = printable[start:start + 3]
        rows = len(chunk[0])
        for row in range(rows):
            row_content = '   '.join(face[row] for face in chunk)
            lines_.append(f'{color}{row_content}\033[0m')
        if start + 3 < len(printable):
            lines_.append('')
    return '\n'.join(lines_)
def create_combinations() -> dict:
    '''
    Reading file with combinations
    '''
    with open('combinations.txt', 'r', encoding='utf-8') as file1:
        lines = file1.readlines()
        lines = dict([(line.strip()).split(' ') for line in lines])
    lines = {tuple(DICES[int(i)-1] for i in combo): int(points) for combo, points in lines.items()}
    return lines
COMBINATIONS = create_combinations()

def bot_move(num_dices: int = 6) -> int:
    '''
    Automatically perform the bot move by rolling all dice,
    finding the most valuable combo and returning its score.
    '''

    rolling_animation(num_dices, prefix='Bot is rolling')
    dices = [DICES[random.choice(range(len(DICES)))] for _ in range(num_dices)]
    print('\nBot rolls the dice!')
    block = format_dice_rows(dices, color='\033[91m')
    if block:
        print(block)
        print()

    combos = find_combinations(''.join(str(i + 1) for i in range(num_dices)), dices)
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
        if input1 == 'exit':
            print('\n\033[91mUSED EXIT!!!\033[0m')
            sys.exit()
        if input1 == 'quit':
            return None
        if input1 == 'pass':
            return combo_result
        print('Wrong input!!!')

    rolling_animation(num_dices, prefix='Rolling your dice')
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
    dice_block = format_dice_rows(dices, include_labels=True)
    if dice_block:
        print(dice_block)
        print()
    if zero:
        print('\033[91mZero combos, opponent`s turn!\033[0m')
        sleep(2.5)
        return 0

    print('Choose dices')
    print("Input format: dices: 1 2 3 or 4 3 2 or 1 or 1 2 3 4 5\nOr type \
pass to score and pass\nType quit to quit")

    while(input1:=input('\033[95m>>> \033[0m')) != 'quit':
        if input1 == 'exit':
            print('\n\033[91mUSED EXIT!!!\033[0m')
            sys.exit()
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

def boss_battle() -> bool:
    '''
    Harder dice minigame variant where the boss rolls 9 dice.
    '''
    player_points = 0
    boss_points = 0

    while player_points < 4000 and boss_points < 4000:
        player_plus = player_move(6, 0)
        if player_plus is None:
            return False
        player_points += player_plus
        boss_points += bot_move(9) // 2
        print(f'BOSS POINTS: \033[91m{boss_points}\033[0m')
        print(f'YOUR POINTS: \033[92m{player_points}\033[0m')
        print('\033[93m=========================================\033[0m')

    if player_points >= boss_points:
        print('\033[92mYOU DEFEATED THE BOSS!!!\033[0m')
    else:
        print('\033[91mTHE BOSS PREVAILED!!!\033[0m')

    return player_points >= boss_points

def start_boss_battle() -> bool:
    '''
    Trigger the boss battle minigame and return True if the player wins.
    '''
    print('\033[91mYOU ENTERED THE BOSS ROOM!!!\033[0m')
    print('Defeat the boss in an enhanced dice duel to proceed.')
    result = boss_battle()
    if result:
        print('\033[92mThe path forward is open!\033[0m')
    else:
        print('\033[91mThe dungeon master has claimed your soul...\033[0m')
    return result

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
        case _:
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
        has_key = True
    if pos == (43, 20) and etap == 0:
        if not start_boss_battle():
            print('!You lost all!??????')
            print('\033[91mGG\033[0m')
            sys.exit()
        etap = 1

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
                case 'Ω':
                    my_map[index][j_index] = '\033[91mΩ\033[0m'

    display_map(my_map, coins)

    n = random.choice(range(30))
    if n == 0: # Minigame appearing
        win = False
        print('\033[91mITS A TRAP!!!\033[0m')
        print('Type skip to skip rules')
        print('Type start to draw rules')
        while(input1:=input('\033[95m>>> \033[0m')) !='start':
            if input1 == 'exit':
                print('\n\033[91mUSED EXIT!!!\033[0m')
                sys.exit()
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
            if input1 == 'exit':
                print('\n\033[91mUSED EXIT!!!\033[0m')
                sys.exit()
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
    #####
    # exit for exit
    ####
    print('Rules:')

def move(variables):
    '''
    I like to move it
    '''
    def read_direction():
        print('\033[95m>>> \033[0m', end='', flush=True)
        while True:
            key = get_single_keypress()
            if key in (b'\r', b'\n'):
                continue  # ignore Enter
            if msvcrt is not None and key == b'\xe0':  # special key prefix on Windows
                key = get_single_keypress()
                direction = ARROW_KEYS.get(key)
                if direction:
                    print()
                    return direction
                continue
            if key.startswith(b'\x1b'):  # escape sequences on POSIX terminals
                direction = POSIX_ARROW_KEYS.get(key[-1:])
                if direction:
                    print()
                    return direction
                continue
            try:
                char = key.decode()
            except UnicodeDecodeError:
                continue
            if char.lower() in 'wasd':
                print(char.upper())
                return char.upper()
            if char.lower() == 'q':
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
        sys.exit()
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
        with open('treasures.txt', 'r', encoding='utf-8') as file:
            treasures = [(i.strip('\n')) for i in file]
            treasures = [i.split(" ") for i in treasures]
            treasures = [(int(i[1]), int(i[0])) for i in treasures]
        variables = {0: blocks, 1: coins, 2: treasures, 3: has_key, 4: pos, 5: etap, 6: hp}
        draw_map(variables)
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('\033[91m====================================================')
        print('KeyboardInterruptError!')
        print('\033[91m====================================================\033[0m')
        sys.exit()
    import doctest
    print(doctest.testmod())

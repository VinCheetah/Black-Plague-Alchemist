from math import inf

input_str = "\t --> "

# Foreground text colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Background colors
BLACK_BG = '\033[40m'
RED_BG = '\033[41m'
GREEN_BG = '\033[42m'
YELLOW_BG = '\033[43m'
BLUE_BG = '\033[44m'
MAGENTA_BG = '\033[45m'
CYAN_BG = '\033[46m'
WHITE_BG = '\033[47m'

# Styles
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'
STRIKETHROUGH = '\033[9m'
RESET_ALL = '\033[0m'
CLEAR = '\033[H\033[J'
CLEAR_TERMINAL = '\033c'

NO_ITALIC = '\033[23m'
NO_UNDERLINE = '\033[24m'
NO_BOLD = '\033[22m'
NO_STRIKETHROUGH = '\033[29m'

def get_input():
    return input(BLUE + input_str + RESET_ALL)

def request(question, choices):
    say(question, CYAN)
    for i, choice in enumerate(choices):
        say("\t"+str(1 + i)+" : *" + str(choice) + "*")
    ans = get_input()
    while not ans.isnumeric() or not (1 <= int(ans) <= len(choices)):
        ans = get_input()
    return int(ans) - 1


def answer_yn(question, default=True):
    say(question + " (default: "+("yes" if default else "no")+")")
    ans = get_input()
    while ans.lower() not in ["", "yes", "y", "no", "n"]:
        ans = get_input()
    if ans == "":
        return default
    else:
        return ans in ["yes", "y"]


def request_number(question, min_val=-inf, max_val=inf, ans_type=int):
    say(question)
    ans = get_input()
    while not (ans.isnumeric() and min_val <= ans_type(ans) <= max_val):
        ans = get_input()
    return ans_type(ans)

def match_transform_begin(transform):
    match transform:
        case "*":
            return BOLD
        case "_":
            return ITALIC
        case "|":
            return UNDERLINE
        case _:
            say("Transform not recognized", "warning")
            return ""


def match_transform_over(transform):
    match transform:
        case "*":
            return NO_BOLD
        case "_":
            return NO_ITALIC
        case "|":
            return NO_UNDERLINE
        case _:
            say("Transform not recognized", "warning")
            return ""


def say(what, who="bot", bold=False, end="\n", map_what=True, body_color=""):
    from character import Character
    bold_str = BOLD if bold else ""
    if who == "bot":
        who_str = ""
    elif isinstance(who, Character):
        who_str = who.color + who.name + RESET_ALL + ": "
    elif who == "warning":
        who_str = YELLOW + "[WARNING]: " + RESET_ALL
    else:
        who_str = who
    last_chars = []
    if map_what:
        what_map = ""
        for char in what:
            if char in ["*", "_", "|"]:
                if len(last_chars) > 0 and last_chars[-1] == char:
                    what_map += match_transform_over(last_chars.pop())
                else:
                    last_chars.append(char)
                    what_map += match_transform_begin(char)
            else:
                what_map += char
        if len(last_chars) > 0:
            print("Transform is not correct [IGNORED]")
    else:
        what_map = what
    print(RESET_ALL + bold_str + who_str + body_color + what_map + RESET_ALL, end=end)


def life_bar(character, bar_size=20):
    life_ratio = character.health / character.health.max
    return GREEN_BG + int(bar_size * life_ratio) * " " + RED_BG + int(bar_size * (1 - life_ratio)) * " " + RESET_ALL



def print_fight(fight):
    msg = CLEAR_TERMINAL + RESET_ALL + "\n"
    ally = fight.player_team + fight.dead_ally
    enemy = fight.enemy_team + fight.dead_enemy
    for i in range(max(fight.player_team_size, fight.enemy_team_size)):
        temp = ""
        if len(ally) > i:
            temp += ally[i].name + ": "
            temp += " " * max(0, (15 - len(temp)))
            temp += life_bar(ally[i])

        temp2 = ""
        if len(enemy) > i:
            temp2 += enemy[i].name + ": "
            temp2 += " " * max(0, (15 - len(temp2)))
            temp2 += life_bar(enemy[i])

        msg += temp + " " * max(70 - len(temp), 0) + temp2 + "\n\n"

    print(msg)











import random

BLACK = 0, 0, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255
GREEN = 0, 255, 0
GOLD = 200, 150, 30
GOLD2 = 212, 175, 55
GREY = 125, 125, 125
VIOLET = 210, 130, 210
LIGHT_BLUE = 140, 160, 255
LIGHT_GREEN = 140, 240, 160
LIGHT_RED = 150, 50, 50
LIGHT_GREY = 200, 200, 200
DARK_GREY = 50, 50, 50
DARK_GREY_1 = 90, 90, 90
DARK_GREY_2 = 70, 70, 70
DARK_GREY_3 = 30, 30, 30
DARK_BLUE = 50, 50, 100
DARK_GREEN = 100, 150, 100
DARK_RED = 120, 50, 50
YELLOW = 190, 240, 0
BROWN = 200, 140, 150

CREA1 = 70, 160, 100
CREA2 = 100, 80, 150
CREA3 = 200, 70, 140
CREA4 = 107, 230, 170


def mix(c1, c2):
    return (c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2, (c1[2] + c2[2]) / 2


def darker(c, darkness=30):
    return max(0, c[0] - darkness), max(0, c[1] - darkness), max(0, c[2] - darkness)


def rand_color(r_inf=0, r_sup=255, g_inf=0, g_sup=255, b_inf=0, b_sup=255):
    return random.randint(r_inf, r_sup), random.randint(g_inf, g_sup), random.randint(b_inf, b_sup)


def lighter(c, lightness=30):
    return min(255, c[0] + lightness), min(255, c[1] + lightness), min(255, c[2] + lightness)


def lighter_absolute(c, lightness=1.3):
    return min(255, c[0] * lightness), min(255, c[1] * lightness), min(255, c[2] * lightness)


def darker_absolute(c, darkness=1.3):
    return max(0, c[0] / darkness), max(0, c[1] / darkness), max(0, c[2] / darkness)


def lighter_compensative(c, lightness=30):
    comp = max(255, c[0] + lightness) + max(255, c[1] + lightness) + max(255, c[2] + lightness) - 765
    return min(255, c[0] + lightness + comp), min(255, c[1] + lightness + comp), min(255, c[2] + lightness + comp)


def darker_compensative(c, darkness=30):
    comp = - min(0, c[0] - darkness) - min(0, c[1] - darkness) - min(0, c[2] - darkness)
    return max(0, c[0] - darkness - comp), max(0, c[1] - darkness - comp), max(0, c[2] - darkness - comp)


def make_alpha(color, alpha):
    return color + tuple([alpha])
class ANSIColor(object):
    RESET = '\x1b[0m'
    BLUE = '\x1b[34m'
    YELLOW = '\x1b[93;1m'
    RED = '\x1b[31;1m'
    MAGENTA = '\x1b[35m'


colors: dict = {
    'default': ANSIColor.RESET,
    'blue': ANSIColor.BLUE,
    'yellow': ANSIColor.YELLOW,
    'red': ANSIColor.RED,
    'magenta': ANSIColor.MAGENTA
}


def colored(tocolor, color: str = 'default'):
    color = colors.get(color, ANSIColor.RESET)
    return color + str(tocolor) + ANSIColor.RESET

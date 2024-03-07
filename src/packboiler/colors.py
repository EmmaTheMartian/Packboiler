# Shorthands for ANSI escape codes
# See https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124
import os


class Code:
    def __init__(self, code: str):
        self.code = code

    def __repr__(self):
        return f"\033[{self.code}m"

    def __str__(self):
        return self.__repr__()

    def __add__(self, other: "Code"):
        return Code(f"{self.code};{other.code}")

    def __call__(self, string: str):
        return f"{self}{string}\033[0m"

    @staticmethod
    def weird_code(code: str):
        """Makes a Code object a custom ANSI code."""
        c = Code("")
        c.code = code
        return c


# Styling
RESET = Code("0")
BOLD = Code("1")
ITALIC = Code("3")
UNDERLINE = Code("4")
STRIKETHROUGH = Code("9")
CLEAR = Code.weird_code("\033[2J")

# Foreground Colors
BLACK = Code("30")
RED = Code("31")
GREEN = Code("32")
YELLOW = Code("33")
BLUE = Code("34")
PURPLE = Code("35")
CYAN = Code("36")
WHITE = Code("37")

# High Intensity Foreground Colors
HI_BLACK = Code("90")
HI_RED = Code("91")
HI_GREEN = Code("92")
HI_YELLOW = Code("93")
HI_BLUE = Code("94")
HI_PURPLE = Code("95")
HI_CYAN = Code("96")
HI_WHITE = Code("97")

# Background Colors
BG_BLACK = Code("40")
BG_RED = Code("41")
BG_GREEN = Code("42")
BG_YELLOW = Code("43")
BG_BLUE = Code("44")
BG_PURPLE = Code("45")
BG_CYAN = Code("46")
BG_WHITE = Code("47")

# High Intensity Background Colors
HI_BG_BLACK = Code("100")
HI_BG_RED = Code("101")
HI_BG_GREEN = Code("102")
HI_BG_YELLOW = Code("103")
HI_BG_BLUE = Code("104")
HI_BG_PURPLE = Code("105")
HI_BG_CYAN = Code("106")
HI_BG_WHITE = Code("107")


# Extra Utilities (totally not an unintended reference to the "Extra Utilities" Minecraft Mod :D)
hr = lambda: print("-" * os.get_terminal_size().columns)
clear = lambda: print(CLEAR.code)

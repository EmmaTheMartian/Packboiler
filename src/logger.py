import src.colors as colors


class Logger:
    def __init__(self, show_debug: bool = False, indents: int = 0):
        self.show_debug = show_debug
        self.indents = indents

    def make_child(self):
        return Logger(self.show_debug, self.indents + 2)

    def log(self, color: colors.Code, text: str):
        print((" " * self.indents) + color(f"-> {text}"))

    def debug(self, text: str):
        if self.show_debug:
            self.log(colors.GREEN + colors.ITALIC, "debug: " + text)

    def info(self, text: str):
        self.log(colors.CYAN, text)

    def warn(self, text: str):
        self.log(colors.YELLOW, "warning:" + text)

    def error(self, text: str):
        self.log(colors.RED, "error: " + text)

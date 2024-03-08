import sys


HELP_MESSAGE = """usage: packboiler [-tmMIydh]
flags:
  -t --template PATH        Path to a template to use. This is a required argument
  -m --modules MODULES      Comma-separated list of modules to enable
  -M --all-modules          Enable all modules
  -I --ignore-automated     Ignores all automated modules specified by the template
  -y --yes-packwiz          Skip confirmation to init a Packwiz pack
  -d --debug                Enable debug logging
  -h --help                 Shows this message

You can pass a URL to a valid template by using `-t "@<URL>"`, where `<URL>` is a URL to a template."""

arg_options = {
    "template": None,
    "modules": None,
    "all-modules": False,
    "ignore-automated": False,
    "yes-packwiz": False,
    "debug": False,
    "help": False,
}

SHORTHANDS = {
    "t": "template",
    "m": "modules",
    "M": "all-modules",
    "I": "ignore-automated",
    "y": "yes-packwiz",
    "d": "debug",
    "h": "help",
}


def prompt(prompt: str, valid_inputs: dict[str]) -> str:
    i = input(prompt)
    while i not in valid_inputs:
        i = input(prompt)
    return i


def parse_arg(arg: str, index: int) -> bool | None:
    """Parses a single argument.
    True is returned if the next argument should be skipped.
    None is returned if the argument did not exist."""
    if arg.count("-") == 1:
        res = False

        for char in arg[1:]:
            p = parse_arg(f"--{SHORTHANDS[char]}", index)
            if p:
                res = True
            if p is None:
                return None

        return res

    arg = arg[2:]  # Strip the --
    if arg == "template":
        arg_options[arg] = sys.argv[index + 1]
        return True
    elif arg == "modules":
        arg_options["modules"] = sys.argv[index + 1].split(",")
        return True
    elif arg in {"all-modules", "ignore-automated", "yes-packwiz", "debug", "help"}:
        arg_options[arg] = True
        return False

    return None

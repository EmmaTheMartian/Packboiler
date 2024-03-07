import sys


HELP_MESSAGE = """usage: packboiler [-tmMAVydh]
flags:
  -t --template PATH        Path to a template to use. This is a required argument
  -m --modules MODULES      Comma-separated list of modules to enable
  -M --all-modules          Enable all modules
  -I --ignore-automated     Ignores all automated modules specified by the template
  -A --pack-author          Specify the author(s) of the Packwiz modpack. If provided, overrides the value in the template if it exists.
  -V --pack-version         Specify the Packwiz modpack version. If provided, overrides the value in the template if it exists.
  -y --yes-packwiz          Skip confirmation to init a Packwiz pack
  -d --debug                Enable debug logging
  -h --help                 Shows this message"""

arg_options = {
    "template": None,
    "modules": None,
    "all-modules": False,
    "pack-author": None,
    "pack-version": None,
    "yes-packwiz": False,
    "debug": False,
    "help": False,
    "ignore-automated": False,
}

SHORTHANDS = {
    "t": "template",
    "m": "modules",
    "M": "all-modules",
    "A": "pack-author",
    "V": "pack-version",
    "y": "yes-packwiz",
    "d": "debug",
    "h": "help",
    "I": "ignore-automated",
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
    if arg in {"template", "author", "pack-version"}:
        arg_options[arg] = sys.argv[index + 1]
        return True
    elif arg == "modules":
        arg_options["modules"] = sys.argv[index + 1].split(",")
        return True
    elif arg in {"all-modules", "yes-packwiz", "debug", "help", "ignore-automated"}:
        arg_options[arg] = True
        return False

    return None

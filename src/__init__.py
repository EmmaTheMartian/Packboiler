import sys


HELP_MESSAGE = """help:
usage: packboiler --template (TEMPLATE PATH)
flags:
  -t --template path        Pass a template to use. Required.
  -m --modules modules      Pass a comma-separated list of modules to toggle.
  -M --all-modules          Enable all modules
  -A --author               Skip confirmation to init a Packwiz pack.
  -V --pack-version         Skip confirmation to init a Packwiz pack.
  -y --yes-packwiz          Skip confirmation to init a Packwiz pack.
  -d --debug                Enable debug logging
  -h --help                 This message."""

arg_options = {
    "template": None,
    "modules": None,
    "all-modules": False,
    "author": None,
    "pack-version": None,
    "yes-packwiz": False,
    "debug": False,
    "help": False,
}

SHORTHANDS = {
    "t": "template",
    "m": "modules",
    "M": "all-modules",
    "A": "author",
    "V": "pack-version",
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
    if arg in {"template", "author", "pack-version"}:
        arg_options[arg] = sys.argv[index + 1]
        return True
    elif arg == "modules":
        arg_options["modules"] = sys.argv[index + 1].split(",")
        return True
    elif arg in {"all-modules", "yes-packwiz", "debug", "help"}:
        arg_options[arg] = True
        return False

    return None

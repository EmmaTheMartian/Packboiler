import sys
import os
import src.template_loader as loader
import src.colors as colors
import src.packwiz as packwiz


def prompt(prompt: str, valid_inputs: dict[str]) -> str:
    i = input(prompt)
    while i not in valid_inputs:
        i = input(prompt)
    return i


def main():
    print((colors.YELLOW + colors.BOLD)("-> Loading template..."))
    template = loader.load_template("templates/forge/20.1.hjson")

    builder = template.build()
    colors.clear()

    print((colors.YELLOW + colors.BOLD)("-> Building modules..."))
    builder.build_modules()
    builder.print()
    builder.print_mods(True)

    should_continue = prompt(
        "Continue and create Packwiz pack? [Y/n] ", {"y", "Y", "n", "N", ""}
    ).lower()

    if should_continue in {"y", ""}:
        colors.clear()
        print((colors.YELLOW + colors.BOLD)("-> Creating Packwiz pack..."))
        context = packwiz.Context("output/forge-1-20-1/")
        packwiz.init_pack(context, builder)


if __name__ == "__main__":
    main()

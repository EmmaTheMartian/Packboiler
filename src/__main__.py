import sys
import src as packboiler
import src.template_loader as loader
import src.packwiz as packwiz
import src.colors as colors
from src.logger import Logger


def main():
    logger = Logger()

    # Parse arguments
    skip = False
    for i in range(1, len(sys.argv)):
        if skip:
            skip = False
            continue

        res = packboiler.parse_arg(sys.argv[i], i)

        if res is None:
            logger.error("Unknown argument: " + sys.argv[i])
        elif res:
            skip = True
            continue

    logger.show_debug = packboiler.arg_options["debug"]
    for arg, value in packboiler.arg_options.items():
        logger.debug(f"Arg `{arg}` = {value}")

    if packboiler.arg_options["help"]:
        logger.info(packboiler.HELP_MESSAGE)
        exit(0)

    # Check if args are invalid
    logger.debug("Provided template: " + str(packboiler.arg_options["template"]))
    if packboiler.arg_options["template"] is None:
        logger.error("No template provided. See packboiler --help.")
        exit(1)

    logger.info("Loading template...")
    template = loader.load_template(
        packboiler.arg_options["template"],
        packboiler.arg_options["author"],
        packboiler.arg_options["pack-version"],
    )

    should_pick = (
        packboiler.arg_options["all-modules"] or packboiler.arg_options["modules"] is not None
    )
    builder = template.build(not should_pick, packboiler.arg_options["modules"])
    colors.clear()

    logger.info("Building modules...")
    builder.build_modules()
    builder.print()
    builder.print_mods(True)

    should_continue = packboiler.arg_options["yes-packwiz"] or packboiler.prompt(
        "Continue and create Packwiz pack? [Y/n] ", {"y", "Y", "n", "N", ""}
    ).lower() in {"y", ""}

    if should_continue:
        colors.clear()
        logger.info("Creating Packwiz pack...")
        context = packwiz.Context("output/")
        packwiz.init_pack(context, builder, logger.make_child())
        logger.info("Pack created in ./output/ directory!")


if __name__ == "__main__":
    main()

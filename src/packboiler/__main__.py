import sys
import packboiler
import packboiler.template_loader as loader
import packboiler.packwiz as packwiz
import packboiler.colors as colors
from packboiler.logger import Logger


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
    tp = packboiler.arg_options["template"]
    logger.debug("Provided template: " + str(tp))
    if tp is None:
        logger.error("No template provided. See packboiler --help.")
        exit(1)

    # Get the template and parse the Hjson for it
    logger.info("Loading template...")
    template_data = loader.load_template_data(tp)
    if template_data is None:
        raise Exception("Failed to load template: " + str(tp))

    template = loader.load_template(
        template_data,
        packboiler.arg_options["pack-author"],
        packboiler.arg_options["pack-version"],
    )

    # Determine if we should ignore the "Pick Modules" prompt
    ignore_pick = (
        packboiler.arg_options["all-modules"] or packboiler.arg_options["modules"] is not None
    )

    # Make the template builder
    builder = template.build(
        logger,
        not ignore_pick,
        packboiler.arg_options["modules"],
        packboiler.arg_options["ignore-automated"],
    )

    # Clear the terminal
    colors.clear()

    # Build the template
    logger.info("Building modules...")
    builder.build_modules()
    builder.print(logger)
    builder.print_mods(logger, True, packboiler.arg_options["debug"])

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

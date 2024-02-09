# Provides utilities to manage a Packwiz pack from Python.
import os
import subprocess
import packboiler.template_loader as loader
import packboiler.colors as colors
from packboiler.logger import Logger


class Context:
    def __init__(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.path = path

    def init(self, *args):
        self._packwiz("init", *args)

    def add_cf(self, slug: str, version: str | None = None, yes: bool = True):
        args = ["cf", "add", slug]
        if version is not None:
            args.extend(["--file-id", version])
        if yes:
            args.append("--yes")
        self._packwiz(*args)

    def add_mr(self, slug: str, version: str | None = None, yes: bool = True):
        args = ["mr", "add", slug]
        if version is not None:
            args.extend(["--version-filename", version])
        if yes:
            args.append("--yes")
        self._packwiz(*args)

    def add_url(self, path: str, force: bool = False, yes: bool = True):
        args = ["url", "add", path]
        if force:
            args.append("--force")
        if yes:
            args.append("--yes")
        self._packwiz(*args)

    def add_entry(self, entry: loader.BuiltModEntry, yes: bool = True):
        args = [entry.provider, "add", entry.mod]
        if yes:
            args.append("--yes")
        self._packwiz(*args)

    def _packwiz(self, *args):
        subprocess.run(["packwiz", *args])


def init_pack(context: Context, builder: loader.TemplateBuilder, logger: Logger, yes: bool = True):
    original_path = os.getcwd()
    os.chdir(context.path)

    logger.info("Initializing pack...")
    context.init(
        "--author",
        builder.template.author,
        "--modloader",
        builder.template.loader,
        f"--{builder.template.loader}-version",
        builder.template.loader_version,
        "--mc-version",
        builder.template.mc_version,
        "--version",
        builder.template.pack_version,
        "--name",
        builder.template.name,
    )

    logger.info("Adding mods...")
    logger_adding = logger.make_child()
    total_mods = sum([len(mods) for mods in builder.module_mods.values()])
    progress = 0

    for module, mods in builder.module_mods.items():
        for mod in mods:
            progress += 1
            logger_adding.info(f"[{progress}/{total_mods}] Adding {mod.mod}")
            context.add_entry(mod, yes)

    os.chdir(original_path)
    logger.info("Done!")

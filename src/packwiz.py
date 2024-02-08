# Provides utilities to manage a Packwiz pack from Python.
import os
import subprocess
import src.template_loader as loader
import src.colors as colors
from src.logger import Logger


class Context:
    def __init__(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.path = path

    def init(self, *args):
        self._packwiz("init", *args)

    def add_cf(self, slug: str, version=None):
        if version is not None:
            self._packwiz("cf", "add", slug, "--file-id", version)
        else:
            self._packwiz("cf", "add", slug)

    def add_mr(self, slug: str, version=None):
        if version is not None:
            self._packwiz("mr", "add", slug, "--version-filename", version)
        else:
            self._packwiz("mr", "add", slug)

    def add_url(self, path: str, force=False):
        if force:
            self._packwiz("url", "add", path, "--force")
        else:
            self._packwiz("url", "add", path)

    def add_entry(self, entry: loader.BuiltModEntry):
        self._packwiz(entry.provider, "add", entry.mod)

    def _packwiz(self, *args):
        subprocess.run(["packwiz", *args])


def init_pack(context: Context, builder: loader.TemplateBuilder, logger: Logger):
    original_path = os.getcwd()
    os.chdir(context.path)

    logger.log("Initializing pack...")
    context.init(
        "--author",
        ", ".join(builder.template.authors),
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

    logger.log("Adding mods...")
    for module, mods in builder.module_mods.items():
        for mod in mods:
            logger.info(f" -> Adding {mod.mod}")
            context.add_entry(mod)

    os.chdir(original_path)
    logger.info(" -> Done!")

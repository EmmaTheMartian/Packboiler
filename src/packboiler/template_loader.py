from abc import ABC
import collections
import hjson
import urllib.request
import simple_term_menu as stm
import packboiler.colors as colors
from packboiler.logger import Logger


DISALLOW_TEMPLATES_FROM_URL = False


class BuiltModEntry:
    def __init__(self, mod: str, provider: str, display_name: str | None = None):
        self.mod = mod
        self.provider = provider
        self.display_name = self.mod if display_name is None else display_name


class ModEntry(ABC):
    TYPE_SINGLE_MOD = "single"
    TYPE_MOD_LIST = "list"
    TYPE_PICK_MOD = "pick"

    def __init__(self, type: str):
        self.type = type

    def build(self) -> BuiltModEntry | list[BuiltModEntry]:
        raise Exception("Cannot build base ModEntry")


class ModEntrySingleMod(ModEntry):
    def __init__(self, mod: str, provider: str, display_name: str | None = None):
        super().__init__(ModEntry.TYPE_SINGLE_MOD)
        self.mod = mod
        self.provider = provider
        self.display_name = self.mod if display_name is None else display_name

    def build(self) -> BuiltModEntry:
        return BuiltModEntry(self.mod, self.provider, self.display_name)


class ModEntryList(ModEntry):
    def __init__(self, mods: list[ModEntrySingleMod]):
        super().__init__(ModEntry.TYPE_MOD_LIST)
        self.mods = mods

    def build(self) -> list[BuiltModEntry]:
        return [entry.build() for entry in self.mods]


class ModEntryPickMod(ModEntry):
    def __init__(self, entries: ModEntryList, desc: str, id: str):
        super().__init__(ModEntry.TYPE_PICK_MOD)
        self.entries = entries
        self.desc = desc
        self.id = id

    def build(self, pick: list[str] | None = None) -> list[BuiltModEntry]:
        mod_names = [entry.display_name for entry in self.entries.mods]
        selection = []
        if pick is None:
            menu = stm.TerminalMenu(
                mod_names,
                title=self.desc,
                multi_select=True,
                show_multi_select_hint=True,
                clear_menu_on_exit=True,
                multi_select_empty_ok=True,
                multi_select_select_on_accept=False,
            )
            selection = menu.show()
            if selection is None:
                return []
        else:
            selection = [mod_names.index(p) for p in pick]

        return [self.entries.mods[selected].build() for selected in selection]


class Module:
    def __init__(
        self, name: str, desc: str, mods: list[ModEntry], pick: dict[str, list[str]] | None = None
    ):
        self.name = name
        self.desc = desc
        self.mods = mods
        self.pick = pick

    def build_entries(self) -> list[ModEntry]:
        built = []
        for entry in self.mods:
            if self.pick is not None and type(entry) is ModEntryPickMod and entry.id in self.pick:
                built.append(entry.build(self.pick[entry.id]))
            else:
                built.append(entry.build())
        return built


class TemplateBuilder:
    def __init__(self, template: "Template"):
        self.template = template
        self.toggled_modules = []
        # All mods in this pack, organized by module
        self.module_mods = {}

    def print(self, logger: Logger):
        c = colors.BLUE + colors.BOLD
        logger.info(f"{c}Template:{colors.RESET} {self.template.name}")
        logger.info(f"{c}Description:{colors.RESET} {colors.ITALIC(self.template.desc)}")
        logger.info(f"{c}Modules:{colors.RESET} {', '.join(self.toggled_modules)}")

    def print_mods(self, logger: Logger, show_providers: bool = False, show_ids: bool = False):
        logger.info("Mods:")
        child = logger.make_child()
        for module, mods in self.module_mods.items():
            child.info((colors.WHITE + colors.ITALIC)(self.template.modules[module].name))
            module_child = child.make_child()
            for mod in mods:
                text = colors.WHITE(mod.display_name)
                if show_providers:
                    text += colors.GREEN(f" (@{mod.provider})")
                if show_ids:
                    text += (colors.WHITE + colors.ITALIC)(f" (id: {mod.mod})")

                module_child.info(text)

    def build_modules(self):
        for module in self.toggled_modules:
            entries = self.template.modules[module].build_entries()
            mods = []
            for entry in entries:
                mods.extend(entry) if type(entry) is list else mods.append(entry)
            self.module_mods[module] = mods


class Template:
    def __init__(
        self,
        name: str,
        desc: str,
        author: str,
        provider: str,
        loader: str,
        loader_version: str,
        mc_version: str,
        pack_version: str,
        imports: dict[str, "Template"],
        modules: dict[str, Module],
        automated_modules: list[str],  # Modules specified by the template to be enabled
        enable_all_modules: bool,
    ):
        self.name = name
        self.desc = desc
        self.author = author
        self.provider = provider
        self.loader = loader
        self.loader_version = loader_version
        self.mc_version = mc_version
        self.pack_version = pack_version
        self.imports = imports
        self.modules = modules
        self.automated_modules = [] if automated_modules is None else automated_modules
        self.enable_all_modules = enable_all_modules

    def print(self, logger: Logger):
        c = colors.BOLD + colors.BLUE
        logger.info(f"{c}Template:{colors.RESET} {self.name}")
        logger.info(f"{c}Description:{colors.RESET} {colors.ITALIC(self.desc)}")
        logger.info(f"{c}Author(s):{colors.RESET} {self.author}")
        logger.info(f"{c}Version:{colors.RESET} {self.loader} {self.loader_version}")
        logger.info(f"{c}Pack Version:{colors.RESET} {self.pack_version}")
        logger.info(f"{c}Imports:{colors.RESET} {', '.join(self.imports.keys())}")
        logger.info(f"{c}Modules:{colors.RESET} {', '.join(self.modules.keys())}")

    def build(
        self,
        logger: Logger,
        pick_modules: bool = True,
        modules: list[str] | None = None,
        ignore_automated_modules: bool = False,
    ) -> TemplateBuilder:
        self.print(logger)
        builder = TemplateBuilder(self)

        if self.enable_all_modules:
            builder.toggled_modules = list(self.modules.keys())
            return builder

        if pick_modules:
            keys = list(
                [module for module in self.modules.keys() if module not in self.automated_modules]
            )
            menu = stm.TerminalMenu(
                keys,
                multi_select=True,
                show_multi_select_hint=True,
                clear_menu_on_exit=True,
                multi_select_empty_ok=True,
                multi_select_select_on_accept=False,
            )
            pick = menu.show()
            builder.toggled_modules = list(menu.chosen_menu_entries)
        else:
            builder.toggled_modules = modules if modules is not None else list(self.modules.keys())

        if not ignore_automated_modules:
            builder.toggled_modules += self.automated_modules

        return builder


def get_mod_entry(entry: dict | str | list[str | dict], default_provider: str) -> ModEntry:
    if type(entry) is str:
        return ModEntrySingleMod(entry, default_provider)
    elif type(entry) is list:
        return ModEntryList([get_mod_entry(e, default_provider) for e in entry])
    elif isinstance(entry, dict):
        provider = default_provider if "provider" not in entry else entry["provider"]
        entry_type = None if "type" not in entry else entry["type"]

        if entry_type == "pick":
            mod_list = get_mod_entry(entry["mods"], provider)
            return ModEntryPickMod(mod_list, entry["desc"], entry["id"])
        else:
            display_name = None if "display-name" not in entry else entry["display-name"]
            return ModEntrySingleMod(entry["name"], provider, display_name=display_name)

    raise Exception(f"Invalid ModEntry: {entry} (type is {type(entry)})")


def module_from_data(id: str, data: dict, template: Template) -> Module:
    name = None
    desc = None
    mods = None
    pick = None

    # Importing from another module
    if "from" in data:
        if data["from"][0] == "$":
            module = template.imports[data["from"][1:]].modules[id]
        else:
            module = load_template(data["from"], template.author, template.pack_version).modules[id]

        name = module.name
        desc = module.desc
        mods = module.mods
        pick = module.pick

    # Override values if able
    name = name if "name" not in data else data["name"]
    desc = desc if "desc" not in data else data["name"]
    mods = (
        mods
        if "mods" not in data
        else [get_mod_entry(mod, template.provider) for mod in data["mods"]]
    )
    pick = pick if "pick" not in data else data["pick"]

    return Module(name, desc, mods, pick)


def load_template_data(path: str) -> dict:
    data = None
    if path.startswith("@"):
        if DISALLOW_TEMPLATES_FROM_URL:
            raise Exception(
                f"Attempted to load template from URL but DISALLOW_TEMPLATES_FROM_URL was True. URL: ({path})"
            )

        with urllib.request.urlopen(path[1:]) as fp:
            data = hjson.load(fp)
    else:
        with open(path) as fp:
            data = hjson.load(fp)
    return data


def load_template(
    data: dict, author: str | None = None, pack_version: str | None = None
) -> Template:
    if author is None:
        if "pack-author" in data:
            author = data["pack-author"]
        else:
            author = input("Pack Author(s): ")

    if pack_version is None:
        if "pack-version" in data:
            pack_version = data["pack-version"]
        else:
            pack_version = input("Pack Version: ")

    provider = data["provider"]

    imports = {}
    if "imports" in data:
        for import_key, import_path in data["imports"].items():
            imports[import_key] = load_template(
                load_template_data(import_path), author, pack_version
            )

    automated_modules = None if "automated-modules" not in data else data["automated-modules"]
    enable_all_modules = False if "enable-all-modules" not in data else data["enable-all-modules"]

    template = Template(
        data["name"],
        data["desc"],
        author,
        provider,
        data["loader"],
        data["loader-version"],
        data["mc-version"],
        pack_version,
        imports,
        {},
        automated_modules,
        enable_all_modules,
    )

    for module, module_data in data["modules"].items():
        template.modules[module] = module_from_data(
            module,
            module_data,
            template,
        )

    return template

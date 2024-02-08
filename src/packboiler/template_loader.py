from abc import ABC
import hjson
import simple_term_menu as stm
import packboiler.colors as colors


class BuiltModEntry:
    def __init__(self, mod: str, provider: str):
        self.mod = mod
        self.provider = provider

    def add(self):
        pass


class ModEntry(ABC):
    TYPE_SINGLE_MOD = "single"
    TYPE_MOD_LIST = "list"
    TYPE_PICK_MOD = "pick"

    def __init__(self, type: str):
        self.type = type

    def build(self) -> BuiltModEntry | list[BuiltModEntry]:
        raise Exception("Cannot build base ModEntry")


class ModEntrySingleMod(ModEntry):
    def __init__(self, mod: str, provider: str):
        super().__init__(ModEntry.TYPE_SINGLE_MOD)
        self.mod = mod
        self.provider = provider

    def build(self) -> BuiltModEntry:
        return BuiltModEntry(self.mod, self.provider)


class ModEntryList(ModEntry):
    def __init__(self, mods: list[ModEntrySingleMod]):
        super().__init__(ModEntry.TYPE_MOD_LIST)
        self.mods = mods

    def build(self) -> list[BuiltModEntry]:
        return [entry.build() for entry in self.mods]


class ModEntryPickMod(ModEntry):
    def __init__(self, entries: ModEntryList, desc: str):
        super().__init__(ModEntry.TYPE_PICK_MOD)
        self.entries = entries
        self.desc = desc

    def build(self) -> list[BuiltModEntry]:
        menu = stm.TerminalMenu(
            [entry.mod for entry in self.entries.mods],
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
        return [self.entries.mods[selected].build() for selected in selection]


class Module:
    def __init__(self, name: str, desc: str, mods: list[ModEntry]):
        self.name = name
        self.desc = desc
        self.mods = mods

    def build_entries(self) -> list[ModEntry]:
        return [entry.build() for entry in self.mods]


class TemplateBuilder:
    def __init__(self, template: "Template"):
        self.template = template
        self.toggled_modules = []
        # All mods in this pack, organized by module
        self.module_mods = {}

    def print(self):
        print(f"{(colors.BOLD + colors.BLUE)('Template:')} {self.template.name}")
        print(str(colors.ITALIC(self.template.desc)))
        print(f"{(colors.BOLD + colors.BLUE)('Modules:')} {', '.join(self.toggled_modules)}")

    def print_mods(self, show_providers: bool = False):
        print((colors.BOLD + colors.BLUE)("Mods:"))
        for module, mods in self.module_mods.items():
            print((colors.ITALIC + colors.BLUE)(f"  {self.template.modules[module].name}"))
            for mod in mods:
                print(
                    f"    - {mod.mod}{(' @' + (colors.GREEN)(mod.provider)) if show_providers else ''}"
                )

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
        modules: list[Module],
    ):
        self.name = name
        self.desc = desc
        self.author = author
        self.provider = provider
        self.loader = loader
        self.loader_version = loader_version
        self.mc_version = mc_version
        self.pack_version = pack_version
        self.modules = modules

    def print(self):
        print(f"{(colors.BOLD + colors.BLUE)('Template:')} {self.name}")
        print(str(colors.ITALIC(self.desc)))
        print(f"{(colors.BOLD + colors.BLUE)('Author(s):')} {self.author}")
        print(f"{(colors.BOLD + colors.BLUE)('Version:')} {self.loader} {self.loader_version}")
        print(f"{(colors.BOLD + colors.BLUE)('Pack Version:')} {self.pack_version}")
        print(f"{(colors.BOLD + colors.BLUE)('Modules:')} {', '.join(self.modules)}")

    def build(self, pick_modules=True, modules: list[str] | None = None) -> TemplateBuilder:
        self.print()
        builder = TemplateBuilder(self)

        if pick_modules:
            keys = list(self.modules.keys())
            menu = stm.TerminalMenu(
                keys,
                multi_select=True,
                show_multi_select_hint=True,
                clear_menu_on_exit=True,
                multi_select_empty_ok=True,
                multi_select_select_on_accept=False,
            )
            picks = menu.show()
            builder.toggled_modules = menu.chosen_menu_entries
        else:
            builder.toggled_modules = modules if modules is not None else list(self.modules.keys())

        return builder


def get_mod_entry(entry: dict | str | list[str], default_provider: str) -> ModEntry:
    if type(entry) is str:
        return ModEntrySingleMod(entry, default_provider)
    elif type(entry) is list:
        return ModEntryList([get_mod_entry(e, default_provider) for e in entry])

    # Assume type is dict
    if entry["type"] == "pick":
        return ModEntryPickMod(get_mod_entry(entry["mods"], default_provider), entry["desc"])

    raise Exception("Unknown ModEntry: " + str(entry))


def load_template(
    path: str, author: str | None = None, pack_version: str | None = None
) -> Template:
    data = None

    with open(path, "r") as fp:
        data = hjson.load(fp)

    if data is None:
        raise Exception("Failed to load template: " + path)

    author = author if author is not None else input("Pack Author(s): ")
    pack_version = pack_version if pack_version is not None else input("Pack Version: ")
    provider = data["provider"]
    modules = {}

    for module, module_data in data["modules"].items():
        mods = [get_mod_entry(mod, provider) for mod in module_data["mods"]]
        modules[module] = Module(module_data["name"], module_data["desc"], mods)

    return Template(
        data["name"],
        data["desc"],
        author,
        provider,
        data["loader"],
        data["loader-version"],
        data["mc-version"],
        pack_version,
        modules,
    )

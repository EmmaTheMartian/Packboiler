# Template Spec

**Notes:**
- This spec is not a specific format.
- This is not valid (H)JSON.
- Packboiler uses Hjson, which does not support JSON schema in editors, so it will not be added unless there's another way to implement a schema (if so please let me know!).

**Syntax Info:**
- Types with a `?` are optional
- `enum`s have a type before them. This is the type of the values in the enum. For example, a `string enum(my, example, enum)` would have three possible values, each are `string`s

```json
{
    // Name of the template
    name: string
    // Description of the template
    desc: string

    // The author(s) of the pack for the Packwiz output
    author: string?
    // The version of the pack for the Packwiz output
    pack-version: string?

    // Default provider to use
    provider: string enum(modrinth, curseforge, url)
    // Mod loader to use
    loader: string enum(forge, fabric, neoforge, quilt)
    // Version of the mod loader to use
    loader-version: string
    // Minecraft version to use
    mc-version: string

    // Any modules that should be enabled automatically
    automated-modules: string[]?
    // If all modules should be enabled automatically. If this is true then automated-modules is ignored
    // Defaults to `false` if not provided
    enable-all-modules: bool?

    // Other templates to import. Keys represent the ID of that import
    // The value is the path or URL to that template
    // Prefix with `@` for URLs
    imports: {
        *: string
    }?

    // Modules. Keys represent the ID of the module.
    modules: {
        *: {
            // Name of the module
            name: string
            // A short description of the module
            desc: string
            // A list of each mod in the module
            mods: Mod[]
            // Used to automatically select options from mod actions with the type of `pick`
            pick: {
                *: {
                    // ID of the action to pick for
                    id: string
                    // The mods to select, by name
                    mods: string[]
                }
            }?
            // Where to import this module from
            from: string?
        }
    }
}

// When Mod is a `string` then it refers just to a slug for the default provider.
// When Mod is an object:
//   If `type` is "single" then `id` is required and `mods` is ignored.
//   If `type` is "pick" or "list" then `id` is ignored and `mods` is required.
Mod = string or {
    // The type of the mod action. Defaults to `single` if not provided
    type: string enum(pick, single, list)?
    // The ID of the mod action
    id: string?
    // The mod provider to get this mod from. Defaults to whatever `provider` is in the template.
    provider: string?
    // A short description shown if the action is invoked
    desc: string?
    // A list of mods to select from, toggle, etc. depending on the type of the action
    mods: Mod[]?
}
```


# Template Spec

**Notes:**
- This spec is not a specific format.
- This is not valid (H)JSON.
- Packboiler uses Hjson, which does not support JSON schema in editors, so it will not be added unless there's another way to implement a schema (if so please let me know!).

```json
{
    // Name of the template
    name: string
    // Description of the template
    desc: string

    // Default provider to use
    provider: string enum(modrinth, curseforge, url)
    // Mod loader to use
    loader: string enum(forge, fabric, neoforge, quilt)
    // Version of the mod loader to use
    loader-version: string
    // Minecraft version to use
    mc-version: string

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
            }
            // Where to import this module from
            from: string
        }
    }
}

Mod = string or {
    // The type of the mod action
    type: string enum(pick)
    // The ID of the mod action
    id: string
    // A short description shown if the action is invoked
    desc: string
    // A list of mods to select from, toggle, etc. depending on the type of the action
    mods: Mod[]
}
```


# Packboiler

> A Packwiz-based modpack boilerplate builder.

Packboiler is a tool intended to allow modpack developers the ability to focus on adding the content and focal mods without needing to spend time installing and configuring performance, tweak, and bug fix mods that are used in nearly every modpack.

Packboiler uses a template system which allows it to work regardless of Minecraft version, modloader, and modloader version. It's extremely flexible too without sacrificing ease-of-use.

Packboiler can also be used simply as a tool to make building modpacks using an Hjson interface rather than managing Packwiz TOML files.

## Installation

If you do not already have it, install [Packwiz](https://packwiz.infra.link).

```shell
# I recommend creating a virtual environment to work in, though you do not have to.
python3 -m venv env && source ./env/bin/activate
python3 -m pip install -r requirements.txt

# Build and install Packboiler
# Replace VERSION with the version in pyproject.toml
python3 -m build
python3 -m pip install ./dist/packboiler-VERSION-py3-none-any.whl

# If you want to make an alias so that you do not have to type out `python3 -m packboiler` to use Packboiler, here:
alias packboiler="python3 -m packboiler"
```

## Usage

```
help:
usage: packboiler [-tmMAVydh]
flags:
  -t --template PATH        Path to a template to use. This is a required argument
  -m --modules MODULES      Comma-separated list of modules to enable
  -M --all-modules          Enable all modules
  -A --author               Specify the author(s) of the modpack
  -V --pack-version         Specify the modpack version
  -y --yes-packwiz          Skip confirmation to init a Packwiz pack
  -d --debug                Enable debug logging
  -h --help                 Shows this message
```

## Template Specification

Naming scheme:
1. Organized into a folder corresponding to the mod loader the template is for
1. Named according to the version it's for, excluding the `1.` of each version (Let's be honest: Minecraft 2.0 will never be released)

See the [template spec](./spec/template.md) for detailed information.

You can also reference one of the existing templates in the `templates` folder.

## Making a Template

Making templates is quite easy, though first you'll want to know some terminology:

```
Provider - A source to download a mod from, such as Modrinth or Curseforge
Module - A togglable module of a template
(Mod) Action - An action which prompts the user to pick certain mods from a list, toggle options, or other configuration for a template
```

Now you can make your first template.

1. Create a file ending with `.hjson`
2. Add the following to the file:
    ```
    {
        name: Example Template
        desc: My first Packboiler template!
        provider: modrinth
        loader: forge
        loader-version: 47.2.20
        mc-version: 1.20.1
    }
    ```

    > Note that this is just an example, feel free to change the provider, loader, versions, names, etc.
3. Start adding some modules, these are togglable parts of your template. You can have multiple or a single one.
    ```
    {
        ...
        modules: {
            my-module: {
                name: My Module
                desc: Core mods for this really cool template
                mods: [
                    jei
                    embeddium
                    create
                ]
            }
            my-other-module: {
                name: My Other Module
                desc: Optional mods for this really cool template
                mods: [
                    emi
                    create-steam-n-rails
                ]
            }
        }
    }
    ```

And that's it! When you use this template, you will be prompted with which modules you want to toggle. You can select any of these (select with `<space>` and continue with `<enter>` or `<return>`) to toggle. Then you will be able to review the mods and make a Packwiz pack using the mods you provided!

# Packboiler

> A Packwiz-based modpack boilerplate builder.

Packboiler is a tool intended to allow modpack developers the ability to focus on adding the content and focal mods without needing to spend time installing and configuring performance, tweak, and bug fix mods that are used in nearly every modpack.

Packboiler uses a template system which allows it to work regardless of Minecraft version, modloader, and modloader version. It's extremely flexible too without sacrificing ease-of-use.

Packboiler can also be used simply as a tool to make building modpacks using an Hjson interface rather than managing Packwiz TOML files.

## Installation

1. Install [Packwiz](https://packwiz.infra.link)
2. (Recommended but not required) Create a venv
    ```shell
    python3 -m venv env && source ./env/bin/activate
    ```
3. Install requirements
    ```shell
    python3 -m pip install -r requirements.txt
    ```
4. Build Packboiler
    ```shell
    python3 -m build
    ```
5. Install Packboiler using Pip
    ```shell
    python3 -m pip install ./dist/packboiler-VERSION-py3-none-any.whl
    ```
    > Replace `VERSION` with whatever version Packboiler is in `pyproject.toml`
6. Confirm install
    ```shell
    python3 -m packboiler -v
    ```
7. (Optional) Alias
    ```shell
    # Add to .bashrc/.zshrc/etc
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

Each template should be:
1. Organized into a folder corresponding to the mod loader the template is for.
1. Named according to the version it's for, excluding the `1.` of each version (Let's be honest: Minecraft 2.0 will never be released).
3. Use Hjson, because it's *so* much more convienient to write.

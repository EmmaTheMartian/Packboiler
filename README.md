# Packboiler

> A Packwiz-based modpack boilerplate builder.

Packboiler is a tool intended to allow modpack developers the ability to focus on adding the content and focal mods without needing to spend time installing and configuring performance, tweak, and bug fix mods that are used in nearly every modpack.

Packboiler uses a template system which allows it to work regardless of Minecraft version, modloader, and modloader version. It's extremely flexible too without sacrificing ease-of-use.

Packboiler can also be used simply as a tool to make building modpacks using an Hjson interface rather than managing Packwiz TOML files.

## Usage

First you'll need to install [Packwiz](https://packwiz.infra.link/) and Packboiler.

> To install Packboiler, just clone this repository and use the provided `packboiler` executable.

## Template Naming Scheme

Each template should be:
1. Organized into a folder corresponding to the modloader the template is for.
1. Named according to the version it's for, excluding the `1.` of each version (Let's be honest: Minecraft 2.0 will never be released).
3. Use Hjson, because it's *so* much more convienient to write.

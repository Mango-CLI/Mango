<div align="center">
  <img src="./img/mango-logo.png" alt="mango-logo" width="180">
</div>

# Mango

> A lightweight script management system for everyday tasks.

Mango utilizes the file system to provide fast and intuitive access to well-organized scripts. It is extremely suitable for managing scripts on personal computers, and is both robust and versatile.

## Installation

### Prerequisites

**Mango primarily targets Linux**, though it should be easily adapted to suit other os systems. Pull requests and feature requests are welcome regarding cross-platform support.

**This project requires Python**, and is tested on Python 3.12, though it should work on Python 3.6 and above. Make sure you have a compatible version of Python installed on your system. If not, you can run:

```bash
sudo apt install python3.12
```

### Installing Mango

There are several approaches to do that.

#### (Recommended) Using the installer script

First clone this repository:

```bash
git clone https://github.com/RayZh-hs/Mango.git
```

Then cd inside to run the script

```bash
cd Mango
./install.sh
```

This will walk you through a guide in the terminal to install Mango on your device. The home mango repo is included by default.

#### Manual installation

Mango itself is a single Python script in `src/`, so you only need to download it and put it somewhere in your system PATH. It is optional but highly recommended that you download the `.mango` folder and put it in `~/`.

## Basic Usage

The core of Mango is extremely simple: It looks up your file system hierarchy in search for folders containing `.mango`, which are called mango repos. You use:
```bash
mango <command> [args]
```
To call a command registered in the closet mango repo. To keep looking up the hierarchy, you append a @ symbol to the command:
```bash
mango @<host_command> [args]
```

For instance, consider this file system:
```text
 - folder_a
    - .mango        # with foo, bar registered
    - folder_b
        - .mango    # with foo, baz registered
        - folder_c
    - folder_d
        - .mango    # with bar registered
```

Suppose you are in `folder_c`, then:
```bash
mango foo
```
Will invoke the foo defined in folder_b;
```bash
mango bar
```
Is going to give an error. To call the host command defined up in the file hierarchy, do:
```bash
mango @bar
```
You have no access to `folder_d` from `folder_c`.

A command is matched to a script by the .instructions file.

## The .instructions File

The .instructions file in the .mango folder is the core registry of a mango repo.

Each non-empty line either starts with #, making it a comment, or follows this format:
```text
<script>: <command1> <command2> ...
```
The script is the name of the executable, which must reside in the .mango folder. The commands are the words the user type after `mango` in the shell to call the script. A script can be tied to multiple commands, separated by spaces in the .instructions file.

## Sourcing Scripts (experimental)

You can source scripts by adding a `-s` or `--source` flag directly after `mango`, for instance:
```bash
mango -s foo arg1 arg2
```
This will force the script to be sourced, allowing it to modify the environment of the user shell. In reality, this is done by mango creating a separate bash shell that mirrors the current shell, and then transporting the user to that shell instance. You can exit the sourced shell by typing `exit`. This feature is experimental, and has a larger performance overhead, so use it sparingly.

If a script is always supposed to be sourced all the time, you can append `*` to the script name in the .instructions file. This will force the script to be executed in sourced mode. For instance:

```text
# This makes foo a sourced script
*foo: bar baz
```

## Home Mango Scripts

To make things easier, Mango comes with prebuilt scripts, which the installer will put in your home folder. You can read them in `~/.mango/`. They are here to make working with mango easier. As long as you work **under** your home directory, and they aren't overridden by other mango repos, you can use them as ordinary host commands:

```bash
mango @init (repo_path) (-t, --template)
```

This command creates a new mango repo in repo_path, which defaults to the current directory, using a template if specified. A list of prebuilt templates can be found in `~/.mango/templates/`, and you can skip to advanced usage to learn how to create your own.

```bash
mango @del (repo_path)
```

This command deletes a mango repo in repo_path, which defaults to the current directory. Only the .mango folder is removed in essence.

```bash
mango @list (repo_path)
```

This command lists all available scripts and commands that are registered in repo_path, which defaults to the current directory.

```bash
mango @add [script_name] (-b, --bind [command_name...]) (-s, --source) (--noopen)
```

This command is called to add a new script to the closest repo, and optionally source it and/or bind commands to it. By default after doing so the script will be opened in the default editor, configured in `~/.mango/_config.py`, but you can skip this by using `--noopen`.

```bash
mango @edit [script_name]
```

Edits the script in the closest repo.

```bash
mango @rm/remove [script_name] (-b, --bind (command_name ...)) (-s, --source)
```

If -b/--bind is specified, this command removes bindings from a script. If nothing follows -b/--bind, all bindings are removed. If -s/--source is present, the script will become an ordinary, ie. not sourced. If neither is present, the script, along with all bindings, is removed.

```bash
mango @bind [script_name] [command_name ...]
```

This command binds commands to a script.

```bash
mango @unbind [script_name] [command_name ...]
```

Conversely, this command unbinds commands from a script.

These commands all have aliases, which you will find in the `~/.mango/.instructions` file.

## Advanced Usage

### Creating a Template

A template is essentially a script that is executed to create other scripts, repos, etc. Currently only the `init` command uses templates, which are stored in `~/.mango/templates/`. You can create your own templates as well, which will be **executed in the '.mango' folder in the initialized repo, after all else is done**.

### Hooks

Hooks are scripts that are executed when called by another script. They follow name conventions. For instance, any file named `.on-add` will be executed by the home repo's add command after a script is added. You can for instance use this to automatically fill the script with some fixed content.

By convention, `.on-add` is executed with $1 as the name of the newly added script, and $2 as all bindings passed in the add command, defaulting to an empty string.

### Configuration

Currently, only the default editor can be configured in `~/.mango/_config.py`. Simply open it up and adjust the string to whatever editor you prefer, so long as it can be launched via the terminal through `<editor_name> [file_path]`.

## Troubleshooting

### Why isn't PS1 updated when sourcing scripts?

This issue is due to the mechanism Mango uses to source scripts. When a script is sourced, it is executed in a separate shell managed by python, and then the results are transported to an interactive new shell instance, which then takes the place of the python script. In most cases your startup script (eg. `~/.bashrc`) overwrites the PS1 setup.  declared in your script.

Tracking down startup scripts is tedious, so alternatively, you can append to your .bashrc script the following:

```bash
if [ -n "$MANGO_PS1" ]; then
    PS1=$MANGO_PS1
fi
unset MANGO_PS1
```

And instead of exporting PS1 in your script, export MANGO_PS1 instead.

From version 1.3.1, Mango will automatically export `MANGO_SOURCED=true` when a mango script is sourced. You can use this to fine-tune your startup scripts.

## Acknowledgements

The logo was made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com). For more information, see the license in `img/license-flaticon`.
<div align="center">
  <img src="./img/mango-logo.png" alt="mango-logo" width="180">
</div>

# Mango

> A lightweight script management system for everyday tasks.

Mango utilizes the file system to provide fast and intuitive access to well-organized scripts. It is extremely suitable for managing scripts on personal computers, and is both robust and versatile.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Concepts](#basic-concepts)
- [Commands](#commands)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Acknowledgements](#acknowledgements)

## Installation

### Prerequisites

**Mango primarily targets Linux**, though it should be easily adapted to suit other OS systems. Pull requests and feature requests are welcome regarding cross-platform support.

**This project requires Python**, and is tested on Python 3.12, though it should work on Python 3.6 and above. Make sure you have a compatible version of Python installed on your system. If not, you can run:

```bash
sudo apt install python3.12
```

### Installing Mango

#### (Recommended) Using the installer script

You can use the provided installer script to set up Mango automatically. Run the following command in your terminal:

```bash
curl -LsSf https://raw.githubusercontent.com/Mango-CLI/Mango/main/install.sh | bash
```

#### Manual installation

Mango itself is a single Python script in `src/`, so you only need to download it and put it somewhere in your system PATH. It is optional but highly recommended that you put the `builtins.mango` submodule under `~/.mango/.submodules`, renaming it to `builtins`. You can then export the bindings by creating the `.instructions` file under `~/.mango/` with the following content:

```text
# Builtin mango scripts
[builtins] *
```

This will make all builtin mango commands available without needing to prepend submodule path.

## Quick Start

New to Mango? Follow these steps to get started quickly:

1. **Initialize a new Mango repository** in your project directory:
   ```bash
   cd ~/my-project
   mango @init
   ```

2. **Create your first script** with a command binding:
   ```bash
   mango @add hello -b greet
   ```

3. **Edit the script** to add your functionality:
   ```bash
   # The script will open in your default editor
   # Add this content:
   echo "Hello, Mango!"
   ```

4. **Run your script** using the command binding:
   ```bash
   mango greet
   ```

5. **List all available commands** in your repository:
   ```bash
   mango @list
   ```

## Basic Concepts

### Mango Repositories

A **mango repository** is any directory containing a `.mango` folder. The `.mango` folder contains an `.instructions` file that defines the bindings between commands and scripts.

### Commands and Bindings

- A **script** is a file managed by mango which can be executed
- A **binding** is a tag attached to a script, used by the user to invoke it
- A **command** is an invocation of an item by its binding

### Host Commands vs Normal Commands

- **Normal commands** only search within the active mango repo (closest `.mango` folder)
- **Host commands** (prefixed with `@`) search up the filesystem, across multiple mango repos, until they find a matching binding

## Commands

For detailed information about any command, use the help system:
```bash
mango @help [command]
```

### Core Commands

- `mango @help` - Display help for mango commands
- `mango @which` - Show which script a command is bound to
- `mango @self update` - Update the mango executable
- `mango @self uninstall` - Uninstall the mango executable

### Repository Management

- `mango @init` - Create a new mango repository
- `mango @deinit` - Remove the mango repository metadata
- `mango @list` - Show scripts and bindings in a repository

### Script Management

- `mango @add` - Create or reopen a script
- `mango @edit` - Open an existing script
- `mango @remove` - Delete scripts or drop their bindings

### Binding Management

- `mango @bind` - Attach commands to a script
- `mango @unbind` - Detach commands from a script

## Advanced Usage

### Submodules

Submodules are mango repositories nested inside `.mango/.submodules/`. They are designed to be externally maintained and facilitate easier version management.

To reference commands from a submodule, use the syntax `module-path:command-name`:

```bash
mango module-1:a
```

To create your own submodule, make a project folder, cd inside and run:

```bash
mango init --template submodule
```

The template will automatically setup the project as a git repo.

### Templates

A template is a mango submodule designed to replace the outer `.mango` folder with its own .mango folder. Templates are useful for creating project scaffolding.

To build a template, cd into the project folder and run:

```bash
mango @init --template template
```

### Registries

You should have noticed that you can already use a selection of mango templates (like `python`, `submodule` and `template`). These are stored in the builtins submodule.

When you finish creating a mango submodule or template, you can either publish it to a remote git repository, or store it locally. Run `mango @{template,submodule} register` to register into your local mango registry (`~/.mango/.*.registry`).

You will then be able to use them like builtin templates and submodules, using their name.

```
mango @submodule list
mango @template list
```

You can run these commands to view your registered submodules and templates.

### Hooks

Hooks are scripts that are executed when called by another script. They follow name conventions. All hooks in Mango are CONVENTIONAL, which means that they are NOT part of any syntax. They work because the mango builtin scripts look for them and execute them if they exist.

Default hooks:
- `.on-add`: Called after `@add` is triggered
- `.on-install`: Called after a submodule (or template) is installed.

You are free to customize and create your own hooks for your scripts as you see fit.

### Environment Variables

When mango invokes a script, it sets the following environment variables:

- `MANGO`: set to indicate that the script is being run by mango
- `MANGO_REPO_PATH`: path to the directory containing .mango
- `MANGO_USER_PATH`: path to the user's present working directory when invoking mango
- `MANGO_SCRIPT_PATH`: full path to the script being invoked
- `MANGO_SCRIPT_NAME`: name of the script being invoked

## Troubleshooting

### Common Issues

1. **Command not found**: Ensure that mango is in your system PATH and that you have a `.mango` folder in your current directory or a parent directory.

2. **Script not executable**: Mango automatically makes scripts executable, but if you're having issues, check the script permissions with `ls -la .mango/`.

3. **Editor not opening**: Make sure you have the `EDITOR` environment variable set to your preferred editor.

## Acknowledgements

The logo was made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com). For more information, see the license in `img/license-flaticon`.
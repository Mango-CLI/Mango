# Changelog

## [1.2.1] - 2025-03-12

### Added

- Source flag to the mango executable.
- Full source support to the home mango commands.
- Full documentation for the source flag.
- A dedicated section in the README for .instruction files.

### Fixed

- Fix bug where script names are misinterpreted as commands names.

## [1.3.1]

### Added

- Flag MANGO_SOURCE to indicate the shell serving after sourcing a script.
- Troubleshooting guide for PS1 issues in README.

## [1.3.2]

### Added

- Support for versioning in the mango cli.

## [2.0.0-alpha] - 2025-10-14

### Added

- Support for submodules in mango repositories.
- Support for exporting commands in mango repositories.

### Changed

- Home mango builtins are moved into `builtins` submodule.
- Development for builtins is migrated to a nwe git repo to facilitate independent versioning and updating.

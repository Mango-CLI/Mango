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

This release is a breaking change, introducing support for submodules in mango repos. The mango executable is backward-compatible with previous versions, but the structure of the home mango has been altered for better modularity and maintainability.

### Added

- Support for submodules in mango repositories.
- Support for exporting commands in mango repositories.
- More comprehensive design documentation for submodules.

### Changed

- Home mango builtins are moved into `builtins` submodule.
- Development for builtins is migrated to a new git repo to facilitate independent versioning and updating.

## [2.0.0-beta] - 2025-10-17

This release is a breaking change, modifying the syntax for exporting submodules and bindings in mango repositories compared with the alpha release. It maintains backward compatibility with stable releases prior to 2.0.0-alpha.

### Added

- Introduce `terminology` section in design docs.
- Pytest-based test suite for mango core.

### Changed

- Changed alpha-staged-proposed exporting syntax from `@export` to `[submodule] *`, and rebinding script from `submodule:binding: ...` to `[submodule] binding: ...` to facilitate simpler parsing and more consistent syntax.

## [2.0.0-beta.1] - 2025-10-17

### Fixed

- Fixed outdated exporting syntax in the installation script for builtins submodule.

## [2.0.0-beta.2] - 2025-10-18

After public beta problems have been identified in the previous design. This release introduces a breaking change to the submodule design to encode mango scripts in a nested .mango folder, making submodules a repo.
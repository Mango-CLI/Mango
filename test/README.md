# Mango Testing Documentation

This document provides comprehensive information about the testing suite for Mango, including the new syntax migration and end-to-end testing.

## Overview

The Mango testing suite has been completely rewritten to support the new syntax redesign. The testing framework covers:

1. **New Syntax Parsing** - Tests for the new `[submodule]` syntax
2. **End-to-End Testing** - Comprehensive integration tests using JSON specifications
3. **Unit Testing** - Individual component tests

## Test Structure

```
test/
├── conftest.py                 # Test configuration and fixtures
├── test_mango_find.py          # Core functionality tests (updated)
├── test_map_submodule_path.py  # Submodule path mapping tests
├── test_split_command.py       # Command splitting tests
├── test_new_syntax_parsing.py  # New syntax parsing tests
├── test_end_to_end.py          # End-to-end integration tests
├── testcases/                  # JSON-based test cases
│   ├── README.md               # Testcases documentation
│   ├── basic_command_execution/
│   ├── submodule_export/
│   └── selective_rebind/
└── TESTING.md                  # This documentation
```
## New Syntax Overview

The new syntax introduces a way to export all bindings from a submodule or selectively rebind specific bindings. The syntax is as follows:

```bash
# Regular bindings (unchanged)
script_path: binding1 binding2 binding3
path/to/script: binding4

# Export all bindings from submodule
[submodule] *

# Selective rebind from submodule
[submodule] old_binding: new_binding1 new_binding2
```

## Test Categories

### 1. New Syntax Parsing Tests (`test_new_syntax_parsing.py`)

These tests verify that the new syntax is correctly parsed and executed:

- **Submodule Export All**: Tests `[submodule] *` syntax
- **Selective Rebind**: Tests `[submodule] old_binding: new_binding1 new_binding2` syntax
- **Mixed Syntax**: Tests combining new syntax with regular bindings
- **Nested Submodules**: Tests nested submodule structures with new syntax
- **Error Handling**: Tests invalid new syntax handling

#### Example Test Case
```python
def test_parse_submodule_export_all(self, tmp_path, mango_module):
    """Test parsing [submodule] * syntax for exporting all bindings."""
    # Create repository structure
    # Create instructions with [tools] *
    # Verify command resolution
```

### 2. End-to-End Tests (`test_end_to_end.py`)

These tests provide comprehensive integration testing using JSON-based testcases:

- **Testcase Runner**: Automatically discovers and runs all testcases in `test/testcases/`
- **JSON Specifications**: Each test is defined in a JSON file with expected inputs and outputs
- **Performance Testing**: Tests performance with large repositories

#### Example Test Case (JSON)
```json
{
  "name": "Basic Command Execution",
  "description": "Test basic command execution without submodules",
  "tests": [
    {
      "from": "workspace",
      "command": "greet",
      "expected_output": "Hello from mango!",
      "expected_exit_code": 0
    }
  ]
}
```

### 3. Updated Unit Tests

Existing unit tests have been updated to work with the new syntax:

- **`test_mango_find.py`**: Updated to use new syntax for export tests
- **`test_map_submodule_path.py`**: Unchanged (path mapping logic)
- **`test_split_command.py`**: Unchanged (command splitting logic)

## Testcases Structure

The `test/testcases/` folder contains end-to-end testcases with JSON specifications. Each testcase is a folder containing:

- `test.json` - JSON specification of the test
- `workspace/` - A mango repository workspace for the test

### Current Testcases

1. **basic_command_execution**: Tests basic command execution without submodules
2. **submodule_export**: Tests new syntax `[submodule] *` for exporting all bindings
3. **selective_rebind**: Tests new syntax `[submodule] old_binding: new_binding1 new_binding2`

For more details, see [`test/testcases/README.md`](test/testcases/README.md).

## Running Tests

### Prerequisites
- Python 3.7+
- pytest
- test dependencies in `conftest.py`

### Running All Tests
```bash
cd /path/to/mango
python -m pytest test/ -v
```

### Running Specific Test Categories
```bash
# Run new syntax tests
python -m pytest test/test_new_syntax_parsing.py -v

# Run end-to-end tests
python -m pytest test/test_end_to_end.py -v

# Run all testcases
python -m pytest test/test_end_to_end.py::TestEndToEnd::test_all_testcases -v

# Run specific test
python -m pytest test/test_new_syntax_parsing.py::TestNewSyntaxParsing::test_parse_submodule_export_all -v
```

### Running with Coverage
```bash
python -m pytest test/ --cov=src --cov-report=html
```

## Test Fixtures

### mango_module Fixture
Provides access to the mango module for testing:
```python
def test_example(mango_module):
    result_path, use_source = mango_module.mangoFind(mango_path, command)
```

### mango_repo Fixture
Creates a temporary mango repository with test scripts:
```python
def test_example(mango_repo):
    repo, mango_dir, tools_dir, nested_dir = mango_repo
    # Use the repository structure for testing
```

## Troubleshooting

### Common Test Issues

1. **Module Import Errors**: Ensure the mango module is properly loaded
2. **Path Issues**: Check that temporary directories are created correctly
3. **Permission Issues**: Ensure test scripts have execute permissions
4. **Syntax Errors**: Verify instruction file syntax is correct

### Debugging Tests

Use pytest's built-in debugging:

```bash
# Run with pdb on failure
python -m pytest test/ --pdb

# Run with verbose output
python -m pytest test/ -v -s

# Stop on first failure
python -m pytest test/ -x
```

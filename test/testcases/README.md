# Mango Testcases

This directory contains end-to-end testcases for Mango, organized as individual test scenarios with JSON specifications.

## Structure

Each testcase is a folder containing:
- `test.json` - JSON specification of the test
- `workspace/` - A mango repository workspace for the test

## JSON Test Specification Format

```json
{
  "name": "Test Case Name",
  "description": "Description of what this test verifies",
  "tests": [
    {
      "from": "workspace",
      "command": "mango command to execute",
      "expected_output": "Expected output text",
      "expected_exit_code": 0,
      "check_stderr": false
    }
  ]
}
```

### Test Fields

- `from`: Directory to execute the command from (relative to the testcase folder)
- `command`: The mango command to execute
- `expected_output`: Text that should appear in the output (default: stdout)
- `expected_exit_code`: Expected exit code (default: 0)
- `check_stderr`: If true, check stderr instead of stdout for expected_output (default: false)

## Current Testcases

1. **basic_command_execution**: Tests basic command execution without submodules
   - Verifies script execution with arguments
   - Tests error handling for non-existent commands

2. **submodule_export**: Tests new syntax `[submodule] *` for exporting all bindings
   - Verifies that all commands from a submodule are exported
   - Tests mixed local and exported commands

3. **selective_rebind**: Tests new syntax `[submodule] old_binding: new_binding1 new_binding2`
   - Verifies selective rebinding of submodule commands
   - Tests multiple new bindings for the same old command

## Adding New Testcases

1. Create a new folder under `test/testcases/`
2. Create a `workspace/` subfolder with a mango repository
3. Create a `test.json` file with the test specification
4. The test will be automatically picked up by the test runner

## Running Tests

To run all testcases:
```bash
python -m pytest test/test_end_to_end.py::TestEndToEnd::test_all_testcases -v
```

To run a specific testcase:
```bash
python -m pytest test/test_end_to_end.py -k "testcase_name" -v
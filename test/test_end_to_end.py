"""Comprehensive end-to-end tests for mango with new syntax."""

import os
import subprocess
import tempfile
import json
from pathlib import Path
import pytest
import time


class TestEndToEnd:
    """End-to-end tests for mango functionality using JSON test specifications."""

    @pytest.fixture(autouse=True)
    def setup_testcases(self):
        """Find all testcases in the testcases folder."""
        self.testcases_dir = Path(__file__).parent / "testcases"
        self.testcase_dirs = [d for d in self.testcases_dir.iterdir() if d.is_dir() and (d / "test.json").exists()]

    def test_all_testcases(self):
        """Run all testcases defined in the testcases folder."""
        mango_script = Path(__file__).parent.parent / "src" / "mango"
        
        for testcase_dir in self.testcase_dirs:
            print(f"\nRunning testcase: {testcase_dir.name}")
            
            # Load the test specification
            with open(testcase_dir / "test.json", "r") as f:
                test_spec = json.load(f)
            
            # Run each test in the specification
            for test in test_spec["tests"]:
                self._run_single_test(testcase_dir, test, mango_script)

    def _run_single_test(self, testcase_dir, test, mango_script):
        """Run a single test from a test specification."""
        workspace_dir = testcase_dir / "workspace"
        
        # Change to the specified directory
        if test["from"] == "workspace":
            cwd = workspace_dir
        else:
            # Support for relative paths from workspace
            cwd = workspace_dir / test["from"]
        
        # Build the command
        cmd_parts = ["python3", str(mango_script)]
        cmd_parts.extend(test["command"].split())
        
        # Execute the command
        result = subprocess.run(
            cmd_parts,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        # Check exit code
        if "expected_exit_code" in test:
            assert result.returncode == test["expected_exit_code"], (
                f"Command '{test['command']}' returned exit code {result.returncode}, "
                f"expected {test['expected_exit_code']}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
        
        # Check output
        if "expected_output" in test:
            output_to_check = result.stderr if test.get("check_stderr", False) else result.stdout
            assert test["expected_output"] in output_to_check, (
                f"Command '{test['command']}' output did not contain expected text\n"
                f"Expected: {test['expected_output']}\n"
                f"Got: {output_to_check}\n"
                f"stderr: {result.stderr}"
            )
        
        print(f"  ✓ {test['command']}: {test.get('expected_output', 'success')}")

    def test_performance_with_large_repository(self, tmp_path):
        """Test performance with a large number of commands and submodules."""
        repo = tmp_path / "large_repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)
        
        # Create many submodules with commands
        instructions_lines = []
        for i in range(10):
            submodule_dir = mango_dir / ".submodules" / f"module_{i}" / ".mango"
            submodule_dir.mkdir(parents=True)
            
            # Create scripts in each submodule
            for j in range(5):
                script_path = submodule_dir / f"script_{j}.sh"
                script_path.write_text(f"#!/bin/bash\necho 'Module {i} Script {j}'\n")
                script_path.chmod(0o755)
            
            # Create instructions for each submodule
            submodule_instructions = []
            for j in range(5):
                submodule_instructions.append(f"script_{j}.sh: cmd_{i}_{j}")
            
            (submodule_dir / ".instructions").write_text("\n".join(submodule_instructions))
            
            # Add to main instructions using new syntax
            instructions_lines.append(f"[module_{i}] *")
        
        (mango_dir / ".instructions").write_text("\n".join(instructions_lines))
        
        # Test finding commands from various modules
        start_time = time.time()
        mango_script = Path(__file__).parent.parent / "src" / "mango"
        
        for i in range(10):
            for j in range(5):
                cmd_parts = ["python3", str(mango_script), f"cmd_{i}_{j}"]
                result = subprocess.run(
                    cmd_parts,
                    cwd=repo,
                    capture_output=True,
                    text=True
                )
                assert result.returncode == 0
                assert f"Module {i} Script {j}" in result.stdout
        
        elapsed_time = time.time() - start_time
        # Should complete reasonably quickly (adjust threshold as needed)
        assert elapsed_time < 5.0, f"Performance test took too long: {elapsed_time} seconds"
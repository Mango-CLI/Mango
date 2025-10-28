"""Tests for environment variables set when mango executes a script."""

import os
import subprocess
import tempfile
import json
from pathlib import Path
import pytest


class TestEnvVariables:
    """Tests for environment variables set during script execution."""

    # Template for test scripts that output environment variables as JSON
    TEST_SCRIPT_TEMPLATE = """#!/bin/bash
# Output environment variables as JSON for easy parsing
cat << EOF
{
  "MANGO": "${MANGO}",
  "MANGO_REPO_PATH": "${MANGO_REPO_PATH}",
  "MANGO_USER_PATH": "${MANGO_USER_PATH}",
  "MANGO_SCRIPT_PATH": "${MANGO_SCRIPT_PATH}",
  "MANGO_SCRIPT_NAME": "${MANGO_SCRIPT_NAME}"
}
EOF
"""

    def _create_test_script(self, script_path):
        """Create a test script that outputs environment variables as JSON."""
        script_path.write_text(self.TEST_SCRIPT_TEMPLATE)
        script_path.chmod(0o755)
        return script_path

    def _create_mango_repo(self, tmp_path, repo_name="test_repo"):
        """Create a basic mango repository structure."""
        repo = tmp_path / repo_name
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)
        return repo, mango_dir

    def _create_submodule(self, mango_dir, module_name="test_module"):
        """Create a submodule structure and return the submodule mango directory."""
        submodule_dir = mango_dir / ".submodules" / module_name / ".mango"
        submodule_dir.mkdir(parents=True)
        return submodule_dir

    def _execute_mango_command(self, repo, command):
        """Execute a mango command and return the result."""
        mango_script_path = Path(__file__).parent.parent / "src" / "mango"
        result = subprocess.run(
            ["python3", str(mango_script_path), command],
            cwd=repo,
            capture_output=True,
            text=True
        )
        return result

    def _parse_env_vars(self, result):
        """Parse environment variables from script output."""
        if result.returncode != 0:
            pytest.fail(f"Script execution failed with error: {result.stderr}")
        
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON output from script: {e}\nOutput: {result.stdout}")

    def _verify_env_vars(self, env_vars, repo, script_path, script_name):
        """Verify all required environment variables are set with correct values."""
        required_vars = [
            "MANGO", "MANGO_REPO_PATH", "MANGO_USER_PATH", 
            "MANGO_SCRIPT_PATH", "MANGO_SCRIPT_NAME"
        ]
        
        for var in required_vars:
            assert var in env_vars, f"{var} environment variable not set"
        
        # Verify the values are correct
        assert env_vars["MANGO"] == "", "MANGO should be set to an empty string"
        assert env_vars["MANGO_REPO_PATH"] == str(repo), f"MANGO_REPO_PATH should be {repo}"
        assert env_vars["MANGO_USER_PATH"] == str(repo), f"MANGO_USER_PATH should be {repo}"
        assert env_vars["MANGO_SCRIPT_PATH"] == str(script_path), f"MANGO_SCRIPT_PATH should be {script_path}"
        assert env_vars["MANGO_SCRIPT_NAME"] == script_name, f"MANGO_SCRIPT_NAME should be '{script_name}'"

    def test_env_variables_set_when_executing_script(self, tmp_path, mango_module):
        """Test that all required environment variables are set when mango executes a script."""
        repo, mango_dir = self._create_mango_repo(tmp_path)
        
        # Create a test script
        test_script = self._create_test_script(mango_dir / "env_test.sh")
        
        # Create instructions file to bind the script
        instructions_path = mango_dir / ".instructions"
        instructions_path.write_text("env_test.sh: test-env\n")
        
        # Execute the script using mango
        result = self._execute_mango_command(repo, "test-env")
        
        # Parse and verify environment variables
        env_vars = self._parse_env_vars(result)
        self._verify_env_vars(env_vars, repo, test_script, "env_test.sh")

    def test_env_variables_with_nested_script(self, tmp_path, mango_module):
        """Test environment variables when executing a script in a subdirectory."""
        repo, mango_dir = self._create_mango_repo(tmp_path)
        
        # Create a subdirectory for the script
        script_dir = mango_dir / "scripts"
        script_dir.mkdir()
        
        # Create a test script in the subdirectory
        test_script = self._create_test_script(script_dir / "nested_env_test.sh")
        
        # Create instructions file to bind the script
        instructions_path = mango_dir / ".instructions"
        instructions_path.write_text("scripts/nested_env_test.sh: test-nested-env\n")
        
        # Execute the script using mango
        result = self._execute_mango_command(repo, "test-nested-env")
        
        # Parse and verify environment variables
        env_vars = self._parse_env_vars(result)
        self._verify_env_vars(env_vars, repo, test_script, "nested_env_test.sh")

    def test_env_variables_with_submodule_script(self, tmp_path, mango_module):
        """Test environment variables when executing a script from a submodule."""
        repo, mango_dir = self._create_mango_repo(tmp_path)
        
        # Create a submodule
        submodule_dir = self._create_submodule(mango_dir)
        
        # Create a test script in the submodule
        test_script = self._create_test_script(submodule_dir / "submodule_env_test.sh")
        
        # Create instructions for the submodule
        submodule_instructions = submodule_dir / ".instructions"
        submodule_instructions.write_text("submodule_env_test.sh: submodule-test\n")
        
        # Create instructions file to bind the submodule script
        instructions_path = mango_dir / ".instructions"
        instructions_path.write_text("[test_module] submodule-test: submodule-test\n")
        
        # Execute the script using mango
        result = self._execute_mango_command(repo, "submodule-test")
        
        # Parse and verify environment variables
        env_vars = self._parse_env_vars(result)
        self._verify_env_vars(env_vars, repo, test_script, "submodule_env_test.sh")
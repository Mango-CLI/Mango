"""Tests for the new syntax parsing in mango."""

import os
import tempfile
from pathlib import Path
import pytest


class TestNewSyntaxParsing:
    """Test cases for the new syntax parsing functionality."""

    def test_parse_submodule_export_all(self, tmp_path, mango_module):
        """Test parsing [submodule] * syntax for exporting all bindings."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create a submodule with instructions
        submodule_dir = mango_dir / ".submodules" / "tools"
        submodule_dir.mkdir(parents=True)
        (submodule_dir / ".instructions").write_text("tool.sh: tool_run\n")
        (submodule_dir / "tool.sh").write_text("#!/bin/sh\necho 'tool executed'\n")

        # Create main instructions with new syntax
        (mango_dir / ".instructions").write_text("[tools] *\n")
        
        # Test finding the exported command
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "tool_run")
        assert Path(result_path) == submodule_dir / "tool.sh"
        assert use_source is False

    def test_parse_submodule_selective_rebind(self, tmp_path, mango_module):
        """Test parsing [submodule] old_binding: new_binding1 new_binding2 syntax."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create a submodule with instructions
        submodule_dir = mango_dir / ".submodules" / "database"
        submodule_dir.mkdir(parents=True)
        (submodule_dir / ".instructions").write_text("db_script.sh: db_connect\n")
        (submodule_dir / "db_script.sh").write_text("#!/bin/sh\necho 'connecting to db'\n")

        # Create main instructions with new rebind syntax
        (mango_dir / ".instructions").write_text("[database] db_connect: db connect\n")
        
        # Test finding the rebound command with new name
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "db")
        assert Path(result_path) == submodule_dir / "db_script.sh"
        assert use_source is False
        
        # Test finding the other rebound command
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "connect")
        assert Path(result_path) == submodule_dir / "db_script.sh"
        assert use_source is False

    def test_parse_mixed_syntax(self, tmp_path, mango_module):
        """Test parsing a mix of new syntax and regular bindings."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create a submodule with instructions
        submodule_dir = mango_dir / ".submodules" / "utils"
        submodule_dir.mkdir(parents=True)
        (submodule_dir / ".instructions").write_text("util.sh: helper\n")
        (submodule_dir / "util.sh").write_text("#!/bin/sh\necho 'helper utility'\n")

        # Create main instructions with mixed syntax
        instructions_content = """# Regular binding
local.sh: local_cmd

# Export all from submodule
[utils] *

# Selective rebind from submodule
[utils] helper: util

# Source script
*source_me.sh: source_cmd
"""
        (mango_dir / ".instructions").write_text(instructions_content)
        
        # Create local scripts
        (mango_dir / "local.sh").write_text("#!/bin/sh\necho 'local command'\n")
        (mango_dir / "source_me.sh").write_text("#!/bin/sh\necho 'sourced command'\n")

        # Test regular binding
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "local_cmd")
        assert Path(result_path) == mango_dir / "local.sh"
        assert use_source is False

        # Test exported all binding
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "helper")
        assert Path(result_path) == submodule_dir / "util.sh"
        assert use_source is False

        # Test selective rebind
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "util")
        assert Path(result_path) == submodule_dir / "util.sh"
        assert use_source is False

        # Test source script
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "source_cmd")
        assert Path(result_path) == mango_dir / "source_me.sh"
        assert use_source is True

    def test_nested_submodule_with_new_syntax(self, tmp_path, mango_module):
        """Test nested submodules with new syntax."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create nested submodule structure
        nested_dir = mango_dir / ".submodules" / "level1" / ".submodules" / "level2"
        nested_dir.mkdir(parents=True)
        (nested_dir / ".instructions").write_text("deep.sh: deep_cmd\n")
        (nested_dir / "deep.sh").write_text("#!/bin/sh\necho 'deep command'\n")

        # Create intermediate level with new syntax
        level1_dir = mango_dir / ".submodules" / "level1"
        (level1_dir / ".instructions").write_text("[level2] *\n")

        # Create main instructions
        (mango_dir / ".instructions").write_text("[level1] *\n")
        
        # Test finding the deeply nested command
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "deep_cmd")
        assert Path(result_path) == nested_dir / "deep.sh"
        assert use_source is False

    def test_invalid_new_syntax_handling(self, tmp_path, mango_module):
        """Test handling of invalid new syntax."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create instructions with invalid new syntax
        (mango_dir / ".instructions").write_text("[invalid\n")  # Missing closing bracket
        
        # Should raise SyntaxError
        with pytest.raises(SyntaxError):
            mango_module.mangoFind(str(mango_dir), "any_command")

    def test_multiple_submodule_exports(self, tmp_path, mango_module):
        """Test exporting multiple submodules with new syntax."""
        repo = tmp_path / "repo"
        mango_dir = repo / ".mango"
        mango_dir.mkdir(parents=True)

        # Create two submodules
        tools_dir = mango_dir / ".submodules" / "tools"
        tools_dir.mkdir(parents=True)
        (tools_dir / ".instructions").write_text("tool.sh: tool_cmd\n")
        (tools_dir / "tool.sh").write_text("#!/bin/sh\necho 'tool'\n")

        utils_dir = mango_dir / ".submodules" / "utils"
        utils_dir.mkdir(parents=True)
        (utils_dir / ".instructions").write_text("util.sh: util_cmd\n")
        (utils_dir / "util.sh").write_text("#!/bin/sh\necho 'utility'\n")

        # Create main instructions exporting both submodules
        instructions_content = """[tools] *
[utils] *
"""
        (mango_dir / ".instructions").write_text(instructions_content)
        
        # Test finding commands from both submodules
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "tool_cmd")
        assert Path(result_path) == tools_dir / "tool.sh"
        
        result_path, use_source = mango_module.mangoFind(str(mango_dir), "util_cmd")
        assert Path(result_path) == utils_dir / "util.sh"
import os
from pathlib import Path

import pytest


def test_split_command_nested_path(mango_module):
    submodule_path, binding = mango_module.splitCommand("sub1:sub2:script")
    assert submodule_path == "sub1:sub2"
    assert binding == "script"


def test_split_command_without_submodule(mango_module):
    submodule_path, binding = mango_module.splitCommand("script")
    assert submodule_path == ""
    assert binding == "script"


def test_map_submodule_path(monkeypatch, tmp_path, mango_module):
    nested_dir = tmp_path / ".submodules" / "alpha" / ".submodules" / "beta"
    nested_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)

    path = mango_module.mapSubmodulePath("alpha:beta")
    expected = os.path.join(".", ".submodules", "alpha", ".submodules", "beta")
    assert os.path.normpath(path) == os.path.normpath(expected)


def test_map_submodule_path_missing(monkeypatch, tmp_path, mango_module):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        mango_module.mapSubmodulePath("missing")


def test_mango_find_returns_script(monkeypatch, tmp_path, mango_module):
    repo = tmp_path / "repo"
    mango_dir = repo / ".mango"
    mango_dir.mkdir(parents=True)

    instructions_path = mango_dir / ".instructions"
    instructions_path.write_text("script.sh: run\n")
    script_path = mango_dir / "script.sh"
    script_path.write_text("#!/bin/sh\n")

    result_path, use_source = mango_module.mangoFind(str(mango_dir), "run")

    assert Path(result_path) == script_path
    assert use_source is False


def test_mango_find_enforces_source_when_marked(tmp_path, mango_module):
    repo = tmp_path / "repo"
    mango_dir = repo / ".mango"
    mango_dir.mkdir(parents=True)

    instructions_path = mango_dir / ".instructions"
    instructions_path.write_text("*script.sh: run\n")
    script_path = mango_dir / "script.sh"
    script_path.write_text("#!/bin/sh\n")

    result_path, use_source = mango_module.mangoFind(str(mango_dir), "run")

    assert Path(result_path) == script_path
    assert use_source is True


def test_mango_find_follows_export(monkeypatch, tmp_path, mango_module):
    repo = tmp_path / "repo"
    mango_dir = repo / ".mango"
    mango_dir.mkdir(parents=True)

    # Create an exported submodule with its own instructions
    submodule_dir = mango_dir / ".submodules" / "tools"
    submodule_dir.mkdir(parents=True)
    (submodule_dir / ".instructions").write_text("nested.sh: nested\n")
    nested_script = submodule_dir / "nested.sh"
    nested_script.write_text("#!/bin/sh\n")

    (mango_dir / ".instructions").write_text("@export tools\n")

    monkeypatch.chdir(repo)

    result_path, use_source = mango_module.mangoFind(str(mango_dir), "nested")

    assert Path(result_path) == nested_script
    assert use_source is False

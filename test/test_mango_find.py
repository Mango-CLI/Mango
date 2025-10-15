from pathlib import Path


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

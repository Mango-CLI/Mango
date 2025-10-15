import os

import pytest


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

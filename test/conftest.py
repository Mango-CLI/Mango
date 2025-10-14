import sys
import builtins
import importlib.machinery
import importlib.util
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_MANGO_PATH = PROJECT_ROOT / "src" / "mango"
BUILTINS_PATH = PROJECT_ROOT / "builtins.mango"

# Ensure builtins.mango is importable as a module source
builtins_path_str = str(BUILTINS_PATH)
if builtins_path_str not in sys.path:
    sys.path.insert(0, builtins_path_str)


def _load_module(module_name: str, module_path: Path):
    """Load a module from an arbitrary file path."""
    if not module_path.exists():
        raise FileNotFoundError(f"Cannot import {module_name}; file not found at {module_path}")
    loader = importlib.machinery.SourceFileLoader(module_name, str(module_path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load spec for module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def mango_module():
    """Provide the mango CLI module for importable access in tests."""
    return _load_module("mango_main", SRC_MANGO_PATH)


@pytest.fixture(scope="session", autouse=True)
def restore_print_after_tests():
    """Ensure the global print function is restored after tests run."""
    original_print = builtins.print
    yield
    builtins.print = original_print

def test_split_command_nested_path(mango_module):
    submodule_path, binding = mango_module.splitCommand("sub1:sub2:script")
    assert submodule_path == "sub1:sub2"
    assert binding == "script"


def test_split_command_without_submodule(mango_module):
    submodule_path, binding = mango_module.splitCommand("script")
    assert submodule_path == ""
    assert binding == "script"

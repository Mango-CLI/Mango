import sys, os, shutil

def existMangoRepo(scan_path_str: str) -> bool:
    """check whether a directory is a mango repo

    Keyword arguments:
    - scan_path_str -- the string of the directory to check
    
    Return: bool for whether the directory is a mango repo
    """
    
    return os.path.exists(os.path.join(scan_path_str, ".mango"))

def closestMangoRepo() -> str:
    """find the first mango repo up the directory tree, raises a FileNotFoundError if none is found

    Return: string for the path of the closest mango repo
    """
    
    cur_exec_path_str = os.getcwd()
    while cur_exec_path_str != "/":
        if existMangoRepo(cur_exec_path_str):
            return cur_exec_path_str
        cur_exec_path_str = os.path.dirname(cur_exec_path_str)
    raise FileNotFoundError("mango repo not found")

def executeIfExists(executable_path: str, args, throw: bool = False) -> None:
    """execute a command if it exists in the path

    Keyword arguments:
    - executable_path -- the path to the script to execute
    - *args -- the arguments to pass to the command
    """
    
    if os.path.exists(executable_path):
        os.system(" ".join([executable_path] + [f'"{arg}"' for arg in args]))
    elif throw:
        raise FileNotFoundError(f"{executable_path} not found")

def removeFolderRecursively(folder_path: str) -> None:
    """remove a folder and all its contents

    Keyword arguments:
    - folder_path -- the path to the folder to remove
    
    This implementation is suggested by Nick Stinemates and Mark Amery on StackOverflow.
    See link: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    """
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Remove failed: {e}")
            raise e
    os.rmdir(folder_path)

def existRegisteredScript(repo_path: str, script_name: str) -> bool:
    """determine whether a script is registered in the .instructions file

    Keyword arguments:
    - repo_path -- the path to the mango repo
    - script_name -- the name of the script
    """
    
    with open(os.path.join(repo_path, ".mango", ".instructions"), "r") as instructions_file:
        for line in instructions_file:
            if line.startswith(f"{script_name}:"):
                return True
    return False

def existRegisteredCommand(repo_path: str, command_name: str) -> bool:
    """determine whether a command is registered in the .instructions file
    
    Keyword arguments:
    - repo_path -- the path to the mango repo
    - command_name -- the name of the command
    """
    
    with open(os.path.join(repo_path, ".mango", ".instructions"), "r") as instructions_file:
        for line in instructions_file:
            if command_name in line.split(" "):
                return True
    return False

def existScript(repo_path: str, script_name: str) -> bool:
    """determine whether a script exists in the mango repo

    Keyword arguments:
    - repo_path -- the path to the mango repo
    - script_name -- the name of the script
    """
    
    return os.path.exists(os.path.join(repo_path, ".mango", script_name))

def registerNewScript(repo_path: str, script_name: str) -> None:
    """register a new script in the mango repo

    Keyword arguments:
    - repo_path -- the path to the mango repo
    - script_name -- the name of the script to register
    """
    
    with open(os.path.join(repo_path, ".mango", script_name), "a") as scripts_file:
        pass
    os.chmod(os.path.join(repo_path, ".mango", script_name), 0o754)
    
    # add the script to .instructions
    with open(os.path.join(repo_path, ".mango", ".instructions"), "a") as instructions_file:
        instructions_file.write(f"{script_name}:")

def bindCommandsToScript(repo_path: str, command_names: list, script_name: str) -> None:
    """bind a list of commands to a script in the mango repo

    Keyword arguments:
    - repo_path -- the path to the mango repo
    - command_names -- the names of the commands to bind
    - script_name -- the name of the script to bind to the commands
    """
    
    lines = []
    has_appended = False
    with open(os.path.join(repo_path, ".mango", ".instructions"), "r") as instructions_file:
        lines = instructions_file.readlines()
        def processLine(line: str) -> str:
            if line.startswith(f"{script_name}:"):
                nonlocal has_appended
                has_appended= True
                present_commands = line.split(":")[1].strip().split(" ")
                if present_commands == [""]:    # this edge case happens when the list is originally empty
                    present_commands = []
                new_commands = set(present_commands + command_names)
                line = f"{script_name}: {' '.join(new_commands)}\n"
            return line
        lines = [processLine(line) for line in lines]
    if not has_appended:
        lines.append(f"{script_name}: {' '.join(command_names)}\n")
    with open(os.path.join(repo_path, ".mango", ".instructions"), "w") as instructions_file:
        instructions_file.writelines(lines)

def openInEditor(editor: str, file_path: str) -> None:
    """open a file in an editor

    Keyword arguments:
    - editor -- the command to open the editor
    - file_path -- the path to the file to open
    """
    
    os.system(f"{editor} {file_path}")
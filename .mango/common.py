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

def executeIfExists(executable_path: str, *args, throw: bool = False) -> None:
    """execute a command if it exists in the path

    Keyword arguments:
    - executable_path -- the path to the script to execute
    - *args -- the arguments to pass to the command
    """
    
    if os.path.exists(executable_path):
        os.system(" ".join([executable_path] + list(args)))
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
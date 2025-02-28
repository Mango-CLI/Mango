import sys, os

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
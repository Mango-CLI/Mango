import sys
import builtins

# ANSI color codes
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m"
}

# ANSI style codes
STYLES = {
    "bold": "\033[1m",
    "underlined": "\033[4m",
}

# Reset flag
RESET = "\033[0m"

original_print = builtins.print

def print(*args, color=None, bold=False, underlined=False, **kwargs):
    """
    Custom print function that supports colored output.

    Usage:
        print("Hello", color="red")
        print("Success!", color="green")

    Args:
        color (str, optional): The color name (red, green, yellow, etc.)
    """
    flags = ""
    
    if color in COLORS:
        flags += COLORS[color]
    if bold:
        flags += STYLES["bold"]
    if underlined:
        flags += STYLES["underlined"]
    
    sys.stdout.write(flags)
    original_print(*args, **kwargs)
    sys.stdout.write(RESET)
    sys.stdout.flush()

# Required to override print globally
builtins.print = print
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
    "white": "\033[97m",
    "reset": "\033[0m"
}

original_print = builtins.print

def print(*args, color=None, **kwargs):
    """
    Custom print function that supports colored output.

    Usage:
        print("Hello", color="red")
        print("Success!", color="green")

    Args:
        color (str, optional): The color name (red, green, yellow, etc.)
    """
    if color in COLORS:
        sys.stdout.write(COLORS[color])  # Apply color
        original_print(*args, **kwargs)
        sys.stdout.write(COLORS["reset"])  # Reset color
        sys.stdout.flush()
    else:
        original_print(*args, **kwargs)  # Default print

# Required to override print globally
builtins.print = print
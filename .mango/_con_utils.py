import sys, tty
import termios
import _print_utils

def get_key():
    """Reads a single key press and blocks until a key is pressed."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)  # Set terminal to raw mode (no buffering)
        key = sys.stdin.read(1)  # Read a single character
        
        if key == '\x1b':
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore settings

    return key

def hideCursor(func):
    """Decorator that hides the cursor before running the function and shows it afterwards."""
    def wrapper(*args, **kwargs):
        try:
            print("\033[?25l", end='')  # Hide cursor
            return func(*args, **kwargs)
        finally:
            print("\033[?25h", end='')  # Show cursor
    return wrapper

def removeLines(n: int):
    """Removes the last n lines from the terminal."""
    for _ in range(n):
        print("\033[F\033[K", end='')

def makeQuery(section_name: str, color: str = "cyan", prefix: str = "+ ", bold: bool = True):
    """Prints a section with the given name."""
    print(prefix, color=color, bold=bold, end='')
    print(section_name, color=color, bold=bold)

def getInput(prompt: str, prompt_color: str = "white", response_color: str = "cyan", prefix: str = "> ", bold: bool = False):
    """Prints a prompt and returns the user input."""
    print(prefix, color=prompt_color, bold=bold, end='')
    if prompt:
        print(f"({prompt}) ", color=prompt_color, bold=bold, end='')
    try:
        _print_utils.original_print(_print_utils.COLORS[response_color], end='')
        response = input()
    finally:
        _print_utils.original_print(_print_utils.RESET, end='')
    return response

@hideCursor
def launchSelectMenu(options: list, selected_prefix: str = "> ", selected_color: str = "cyan", unselected_prefix: str = "  ", unselected_color: str = "white"):
    """Launches a select menu with the given options and returns the index of the selected option."""
    selected_line_number = 0
    while True:
        # first print the options
        for i, option in enumerate(options):
            if i == selected_line_number:
                print(selected_prefix, color=selected_color, end='')
                print(option, color=selected_color, underlined=True)
            else:
                print(unselected_prefix, color=unselected_color, end='')
                print(option, color=unselected_color)
        
        # then get the user input
        key = get_key()
        
        # handle the user input
        if key == '\x1b[A':
            selected_line_number = max(0, selected_line_number - 1)
        elif key == '\x1b[B':
            selected_line_number = min(len(options) - 1, selected_line_number + 1)
        elif key == '\x0d':
            return selected_line_number
        elif key == '\x03':
            print("ctrl-c")
            exit(0)
        
        # clear the lines above
        removeLines(len(options))
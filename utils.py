import sys

def start_screen(stdscr):
    """Displays the starting screen."""
    stdscr.clear()
    stdscr.addstr("Press any key start Words Per Minute\n\nPress ESC to exit")
    stdscr.refresh()
    key = stdscr.getkey()
    if len(key) == 1:
        if ord(key) == 27: sys.exit()

    

def load_files() -> list[str]:
    """Loads the text examples and the best score. Returns the list of text lines 
    and the best score."""
    with open("text.txt") as file:
        text = file.readlines()

    try:
        with open("best_score.txt") as file:
            best = file.readline()
    except:
        with open("best_score.txt", "w") as file:
            file.write("0")
        best = 0

    return text, int(best)


def record_best(best):
    """Records the new best score."""
    with open("best_score.txt", "w") as file:
        file.write(str(best))
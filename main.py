# TODO:
# fix the cursor blinking
# add records


import curses, time, random
from curses import wrapper


def start_screen(stdscr):
    """Displays the starting screen."""
    stdscr.clear()
    stdscr.addstr("Press any key start Words Per Minute\n")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    """Displays the text."""
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    correct_text = 0

    for i, char in enumerate(current):
        # If the input is correct, display it green.
        if char == target[i]:
            color = curses.color_pair(1)
            correct_text += 1
        # If it's incorrect, but it's an space, display it with red bg.
        elif char == ' ':
            color = curses.color_pair(3)
        # Else, display it red.
        else:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

    return correct_text


def wpm_test(stdscr, target_text):
    """Gets the input from the user and calculates the WPM."""
    current_text = []
    correct_text = 0
    wpm=0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        # Calculate the WPM.
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((correct_text / (time_elapsed / 60)) / 5)

        # Display the text.
        stdscr.clear()
        correct_text = display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Check if text is successfully completed.
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # Try to store the inputted key. (When nodelay active, no inputting a ket may raise an error).
        try:
            key = stdscr.getkey()
        except:
            continue

        # Try to check if the key is ESC (Some keys may raise errors when getting their ordenance.)
        try:
            if ord(key) == 27:
                break
        except TypeError:
            pass

        # If backspace, pop the last char from the text.
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        # Else add char to the text.
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    # Get the example text.
    with open("text.txt") as file:
        text = file.readlines()

    # Init the color pairs.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)

    start_screen(stdscr)

    # Init loop to play and replay.
    while True:
        wpm_test(stdscr, random.choice(text).strip())
        stdscr.addstr(2, 0, "Text completed! Press any key to continue...")
        key = stdscr.getkey()
        
        try:
            if ord(key) == 27:
                break
        except TypeError:
            pass


wrapper(main)
import curses, time, random, sys
from curses import wrapper
from utils import start_screen, load_files, record_best


def main(stdscr):
    # Get the example text and best score.
    text, best = load_files()

    # Init the color pairs.
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)

    start_screen(stdscr)

    # Init loop to play and replay.
    while True: 
        wpm = wpm_test(stdscr, random.choice(text).strip(), int(best))
        stdscr.addstr(4, 0, "Text completed! Press any key to continue...")
        stdscr.addstr(6, 0, "Press ESC to exit")
        
        if wpm > best:
            best = wpm
            record_best(best)
        
        # Ask for a key to continue.
        key = stdscr.getkey()
        # If no input, ESC was pressed, exit.
        if len(key) == 1:
            if ord(key) == 27: sys.exit()


def wpm_test(stdscr, target_text, best):
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

        timer = round(time.time() - start_time, 1)

        # Display the text.
        stdscr.clear()
        correct_text = display_text(stdscr, target_text, current_text, best, timer, wpm)
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

        # Reset time then no text written.
        if current_text == []:
            start_time = time.time()

        # Check if the key is ESC.
        if len(key) == 1:
            if ord(key) == 27: sys.exit()
        # Else it's an special key that don't need to be recorded.
        else:
            continue     

        # If backspace, pop the last char from the text.
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()               
        # Else add char to the text.
        elif len(current_text) < len(target_text):
            current_text.append(key)


    return wpm
    

def display_text(stdscr, target, current, best, timer, wpm=0):
    """Displays the text."""
    stdscr.addstr(target)
    stdscr.addstr(2, 0, f"WPM: {wpm}")
    stdscr.addstr(2, 15, f"Best Score: {best}")
    stdscr.addstr(2, 40, f"Time: {timer}")
    stdscr.addstr(4, 0, "Press ESC to exit")
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


wrapper(main)
# TODO:
# make the wrong spaces appear with red background
# make the wrong input don't count to the WPM

import curses, time, random
from curses import wrapper


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Press any key start Words Per Minute\n")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        if char == target[i]:
            color = curses.color_pair(1)
        else:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr, target_text):
    current_text = []
    wpm=0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        try:
            if ord(key) == 27:
                break
        except TypeError:
            pass

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    with open("text.txt") as file:
        text = file.readlines()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)

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
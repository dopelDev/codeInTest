import curses
from typing import List
from time import sleep
from os import environ as env


stdscr = curses.initscr()

def select_option(current_option):
    stdscr.clear() 
    stdscr.addstr(current_option, curses.color_pair(3))
    stdscr.getch()

def select_key(key, current_option, options):
    if key == ord('j') and current_option < len(options) - 1:
        current_option += 1
    elif key == ord('k') and current_option > 0:
        current_option -= 1
    elif key == ord('e'):
        select_option(options[current_option])
    elif key == ord('q'):
        exit(0)
    return current_option



def main(stdscr):
    curses.cbreak()
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_YELLOW)
    curses.curs_set(False)

    stdscr.clear()
    stdscr.addstr('Curses work it!!!', curses.A_BOLD + curses.color_pair(3))
    stdscr.nodelay(False)
    stdscr.getch()
    stdscr.clear()
    options = ['markdown', 'qtile', 'postgresql']
    current_option = 0
    while True:
        for index, option in enumerate(options):
            if index == current_option:
                stdscr.addstr(option, curses.color_pair(1))
                stdscr.addstr('\n')
            elif index != current_option:
                stdscr.addstr(option, curses.color_pair(2))
                stdscr.addstr('\n')

        key = stdscr.getch()
        current_option = select_key(key, current_option, options)
        

        stdscr.clear()
        curses.endwin()
    return stdscr
if __name__ == '__main__':
    curses.wrapper(main)

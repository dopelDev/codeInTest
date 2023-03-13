import curses
from time import sleep

def main():
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_GREEN)
    stdscr.addstr('----->', curses.A_BOLD + curses.color_pair(1))
    stdscr.addstr('\n')
    stdscr.addstr('----->', curses.A_NORMAL + curses.color_pair(2))
    stdscr.addstr('\n')
    stdscr.addstr('NORMAL')
    stdscr.getch()
    curses.endwin()


if __name__ == '__main__':
    main()

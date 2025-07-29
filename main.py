import curses
from tui.main_page import main_page

if __name__ == "__main__":
    curses.wrapper(main_page)
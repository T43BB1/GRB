from tqdm import tqdm

class ProgressBar_IO:
    def __init__(self, stdscr, x0, y0):
        self.stdscr = stdscr
        self.x0 = x0
        self.y0 = y0
        self.buffer = ''
    def write(self, s):
        self.buffer = s
        return len(s)
    def flush(self):
        self.stdscr.addstr(self.y0, self.x0, self.buffer)
        self.buffer = ''

class ProgressBar(tqdm):
    def __init__(self, stdscr, x0, y0, *args, **kwargs):
        super().__init__(file=ProgressBar_IO(stdscr=stdscr, x0=x0, y0=y0), ascii=False, *args, **kwargs)
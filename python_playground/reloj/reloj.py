import curses
import logging
from time import sleep, strftime

class window(object):
    def __init__(self):
        self.logger = self.make_logger('Timeline')
        self.logger.info('Initializing')

    def make_logger(self, name):
        file_handler = logging.FileHandler(name + '.log', mode='w')
        logger = logging.getLogger('logger')
        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(10)

        return logger

    def half(self):
        height ,width = self.stdsrc.getmaxyx()
        return int(height/2), int(width/2)   

    def add_event(self):
        event = strftime('%H:%M:%S')
        return event

    def events_run(self, events : list):
        # usarlo con multithreading or multiprocessing

        self.stdsrc.clear()
        _, width = self.half()
        for event in events:
            self.stdsrc.move(len(events) + 2, width -  int(len(event)/2))
            self.stdsrc.addstr(event)
            self.stdsrc.refresh()


    def title_reloj(self):
        _ , width = self.half()
        self.stdsrc.move(0, width)
        self.stdsrc.addstr(strftime('%H:%M:%S'))
        self.stdsrc.refresh()

    def main_options(self):
        events = []
        opt: int = 0
        while True:
            self.stdsrc.clear()
            self.title_reloj()
            self.stdsrc.nodelay(True)
            opt = self.stdsrc.getch()
            if opt == ord('q'):
                break
            if opt == -1:
                pass
            if opt == 32:
                events.append(self.add_event())
            if len(events) > 0:
                self.logger.debug("{} es evento, {} la lista de eventos, {} , es el type de events".format(events, events, type(events)))
                self.events_run(events)
            # less processing power needed
            sleep(0.1)

        self.logger.info("closed successfully")


    def run(self):
        self.stdsrc = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(False)

        self.main_options()
        
        curses.endwin()

if __name__ == '__main__':
    win = window()
    win.run()

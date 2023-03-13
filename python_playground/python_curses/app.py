import curses

class time_tracking():

    def __init__(self):
        self.logger = self.make_logger()
        self.logger.info('Initializing time tracking')
    def __repr__(self):
        return f'object : time_tracking, logger : {self.logger}'

    def make_logger(self):
        import logging
        file_handler = logging.FileHandler('time_tracking.log', mode='w')
        logger = logging.getLogger('logger')
        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger

    def top_witget(self):
        pass
    def middle_witget(self):
        pass
    def bottom_witget(self):
        pass

    def run(self):
        self.main_scr = curses.initscr()
        curses.cbreak()
        self.logger.info('Object: %s' % self.main_scr)  

        self.main_scr.getch()
        curses.endwin() 
        


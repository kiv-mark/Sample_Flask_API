import logging
import os.path

class Logger(object):

    def __new__(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        log_path = os.path.join(my_path, "../My_API/Logs/connections.log")
        logger = logging.getLogger('get_item')
        logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(log_path)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            '%m-%d %H:%M:%S')
        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        return logger

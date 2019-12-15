import logging
import logging.handlers
import getpass
import os


class MyLog:

    def __init__(self, absolute_log_folder=None):
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        # config logging level here
        self.logger.setLevel(logging.DEBUG)
        format_str = '[%(levelname)7s] %(asctime)s - %(module)s #%(lineno)d : %(message)s'
        formatter = logging.Formatter(format_str)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        logfile = os.path.join(absolute_log_folder, 'autoStnMove.log')
        file_handler = logging.handlers.RotatingFileHandler(logfile,
                                                            maxBytes=5 * 1024 * 1024,  # 5 MB
                                                            backupCount=10)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

import logging


class Logger:
    def __init__(self, log_file='logger.log'):
        self.logger = logging.getLogger('LibraryLogger')
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

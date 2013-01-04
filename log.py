import logging
import logging.handlers

class Logger(object):
    
    def __init__(self, module):
        self.logger = logging.getLogger("mermmaid." + module)
        self.logger.setLevel(logging.DEBUG)
        
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(levelname)s]: %(message)s")
        console_logger.setFormatter(formatter)

        self.logger.addHandler(console_logger)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if __name__ == '__main__':
    l = Logger("test")
    l.debug("Test")
    l.info("Test")
    l.warn("Test")
    l.error("Test")
    l.critical("Test")

import logging


class LoggerFactory:
    @staticmethod
    def create_logger(formatter, handlers):
        logger = logging.getLogger('chatgpt_logger')
        logger.setLevel(logging.INFO)
        for handler in handlers:
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
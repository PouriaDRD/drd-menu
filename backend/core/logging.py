import logging


class ExactLevelFilter(logging.Filter):
    """
    Allow only records matching the configured log level.
    """

    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level

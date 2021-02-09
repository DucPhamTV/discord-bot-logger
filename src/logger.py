"""
Local loggers, stream logger and file logger for debug purpose
"""

import logging


class Logger():
    """Singleton pattern"""
    _instance = None
    def __new__(cls, path="/var/log/bots/discord-bot.log", level=logging.DEBUG):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            log = logging.getLogger("bot")
            log.setLevel(logging.DEBUG)
            handler = logging.FileHandler(path)
            handler.setLevel(level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            log.addHandler(handler)
            cls._instance.log = log

        return cls._instance

    def info(self, *args):
        self.log.info(*args)

    def debug(self, *args):
        self.log.debug(*args)

    def error(self, *args):
        self.log.error(*args)


log = Logger()

if __name__ == "__main__":
    log = Logger()
    log.info("Hello world!")
    log2 = Logger()
    log2.info("Is this singleton: %s", "Yes" if log is log2 else "No")
    log.info("Bye")

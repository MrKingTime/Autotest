from time import strftime, localtime
import logging
import logging.handlers
import settings


def init_logger() -> logging.Logger:
    """初始化logger，同时打印到日志和控制台中

    :return _type_: _description_
    """
    file_name = f"logs/{settings.TITLE} {strftime('%Y-%m-%d', localtime())}.log"

    logger = logging.getLogger(settings.TITLE)
    logger.setLevel(logging.DEBUG)
    ls = logging.StreamHandler()
    open(file_name, mode="a", encoding="utf-8").close()
    lf = logging.handlers.TimedRotatingFileHandler(filename=f"{file_name}", when="d", backupCount=3, encoding="utf-8")
    fmt = "%(asctime)s %(levelname)s [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s"
    formatter = logging.Formatter(fmt=fmt)
    ls.setFormatter(formatter)
    lf.setFormatter(formatter)
    logger.addHandler(ls)
    logger.addHandler(lf)
    logger.info("日志初始化")
    return logger


def get_logger() -> logging.Logger:
    return _logger


_logger = init_logger()

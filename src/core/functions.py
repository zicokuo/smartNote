import logging

import flet

from .i18n import get_text
from settings import DEBUG, LOG_PATH, CODING_SET


def _(t: str, *args):
    """
    翻译
    :param t:
    :param args:
    :return:
    """
    return get_text(t.format(*args)) if args else get_text(t)


logging.basicConfig(format='%(asctime)s %(module)s %(name)s_%(levelname)s:  %(message)s',
                    # filename=f'{LOG_PATH}/log.log',
                    filemode='a+',
                    datefmt='%y%m%d %H:%M:%S',
                    encoding=CODING_SET)
logger = logging.getLogger("SYS")
logger.setLevel(DEBUG if logging.INFO else logging.WARN)

log: logging.Logger = logger


def event_back(e: flet.ControlEvent):
    e.page.go('/')

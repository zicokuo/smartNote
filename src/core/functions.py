import logging

import flet

from core.i18n import get_text
from settings import DEBUG, LOG_PATH, CODING_SET


def _(t: str, *args):
    """
    快捷翻译
    """
    if len(args) > 0:
        return get_text(t.format(*args))
    return get_text(t)


logging.basicConfig(format='%(asctime)s %(module)s %(name)s_%(levelname)s:  %(message)s',
                    filename=f'{LOG_PATH}/log.txt',
                    filemode='a+',
                    datefmt='%y%m%d %H:%M:%S',
                    encoding=CODING_SET,
                    level=DEBUG if logging.DEBUG else logging.INFO)
logger = logging.getLogger("SYS")
logger.setLevel(DEBUG if logging.DEBUG else logging.INFO)

log: logging.Logger = logger


def event_back(e: flet.ControlEvent):
    e.page.go('/')

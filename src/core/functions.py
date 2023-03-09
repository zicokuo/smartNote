import logging

import flet

from core.i18n import get_text


def _(t: str, *args):
    """
    快捷翻译
    """
    if len(args) > 0:
        return get_text(t.format(*args))
    return get_text(t)


logging.basicConfig(format='%(asctime)s %(module)s %(name)s_%(levelname)s:  %(message)s',
                    datefmt='%y%m%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger("SYS")
logger.setLevel(logging.INFO)

def event_back(e:flet.ControlEvent):
    e.page.go('/')
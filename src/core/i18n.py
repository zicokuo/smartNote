import gettext
from functools import cache
from typing import Optional

from settings import LANG, LOCALE_PATH


@cache
def locale_lang(lang: Optional[str] = None):
    """
    加载本地语言文件
    :param lang:
    :return:
    """
    if lang is None:
        lang = LANG

    locale_dir = LOCALE_PATH
    translate = gettext.translation('lang', languages=[lang], localedir=locale_dir, fallback=True)
    _ = translate.gettext
    print(_(f'load lang file {lang}'))
    _ = None
    return translate.gettext


get_text = locale_lang()
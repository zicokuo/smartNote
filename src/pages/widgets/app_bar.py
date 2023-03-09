import flet

from core.functions import _


def app_bar(title=""):
    return flet.AppBar(title=flet.Text(_(f"{title}"), bgcolor=flet.colors.SURFACE))

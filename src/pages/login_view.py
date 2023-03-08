import flet

from core.functions import _


def page(ctx: flet.Page, route: str):
    view: flet.View = flet.View(
        route,
        [
            flet.Text('牛逼'),
            login_form()
        ]
    )
    return view


def login_form():
    form = flet.Column([
        flet.TextField(prefix_icon=flet.icons.FAVORITE, hint_text=_("账户登录"))
    ])
    return form

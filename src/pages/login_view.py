import flet
from flet_core import MainAxisAlignment, CrossAxisAlignment, AppBar

from core.functions import _, event_back

view_input: flet.View = None


def page(ctx: flet.Page, route: str):
    view_input = flet.View(
        route, [
            login_form()
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    ctx.banner = banner_ctl

    return view_input


def login_form():
    form = flet.Column([
        flet.Row([
            flet.Text(_("用户登录")),
        ]),
        account_input_ctl,
        password_input_ctl,
        flet.Row([
            flet.ElevatedButton(text=_("登录"), on_click=event_login_form_submit),
            flet.ElevatedButton(text=_("返回"), on_click=event_back),
        ])
    ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        width=420)
    return form


def event_login_form_submit(e: flet.ControlEvent):
    banner_ctl.content = flet.Text(f"账号:{account_input_ctl.value},密码:{password_input_ctl.value}")
    banner_ctl.open = True
    e.page.update()


def event_close_banner(e: flet.ControlEvent):
    banner_ctl.open = False
    e.page.update()


account_input_ctl = flet.TextField(prefix_icon=flet.icons.FAVORITE, hint_text=_("账户"), )
password_input_ctl = flet.TextField(prefix_icon=flet.icons.FAVORITE, hint_text=_("密码"), password=True, max_length=8)
banner_ctl = flet.Banner(
    bgcolor=flet.colors.RED,
    leading=flet.Icon(flet.icons.WARNING_AMBER_ROUNDED, color=flet.colors.AMBER, size=40),
    content=flet.Text(
        "Oops, there were some errors while trying to delete the file. What would you like me to do?"
    ),
    actions=[
        flet.TextButton("Retry", on_click=event_close_banner),
        flet.TextButton("Ignore", on_click=event_close_banner),
        flet.TextButton("Cancel", on_click=event_close_banner),
    ],
)

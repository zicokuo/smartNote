import flet
from flet_core import CrossAxisAlignment

from pages.widgets.app_bar import app_bar
from pages.widgets.welcome import welcome_ctl

view_input: flet.View = None


def page(ctx: flet.Page, route: str):
    view_input = flet.View(
        route, [
            welcome_ctl(),
            flet.ElevatedButton("登了个录2", on_click=lambda _: ctx.go("/login")),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view_input

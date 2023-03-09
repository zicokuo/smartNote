import flet
from flet_core import CrossAxisAlignment

from core.functions import _
from pages.widgets.app_bar import app_bar

view_input: flet.View = None


def page(ctx: flet.Page, route: str):
    view_input = flet.View(
        route, [
            flet.ElevatedButton("登了个录", on_click=lambda _: ctx.go("/login")),
        ],
        appbar=app_bar(title="Index"),
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view_input

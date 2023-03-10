from flet_core import CrossAxisAlignment, ElevatedButton, Page, View

from core.functions import _
from pages.widgets.welcome import welcome_ctl

view_input: View = None


def page(ctx: Page, route: str):
    view_input = View(
        route, [
            welcome_ctl(),
            ElevatedButton(_("登入"), on_click=lambda _: ctx.go("/dashboard")),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view_input

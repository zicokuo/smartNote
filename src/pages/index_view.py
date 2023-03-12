from flet_core import CrossAxisAlignment, ElevatedButton, Page, View

from core.functions import _
from pages.widgets.welcome import welcome_widget

view_input: View = None


def page(ctx: Page, route: str):
    view = View(
        route, [
            welcome_widget(),
            ElevatedButton(_("登入"), on_click=lambda _: ctx.go("/dashboard")),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view

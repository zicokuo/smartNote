import flet
from flet_core import CrossAxisAlignment, colors, Page, View, AppBar, Text, Container, Row

from core.functions import _
from pages.widgets.sub_menu import sub_menu

view_input: View = None
app_bar = AppBar(title=Text(_("工作台")), color=colors.SURFACE, bgcolor=colors.WHITE)


def page(ctx: Page, route: str):
    view_input = View(
        route, [
            app_bar,
            Container(content=Row([
                sub_menu()]))
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view_input

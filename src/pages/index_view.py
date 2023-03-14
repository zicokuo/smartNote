from flet_core import CrossAxisAlignment, ElevatedButton, Page, View, Text, ControlEvent

from core.functions import _
from pages.widgets.welcome import welcome_widget
from settings import APP_CONFIG

view_input: View = None


def on_pices_click(e: ControlEvent):
    e.page.go("/apps/pices")


def page(ctx: Page, route: str):
    view = View(
        route, [
            welcome_widget(),
            ElevatedButton(_("改图工具"), on_click=on_pices_click),
            Text(APP_CONFIG.get('version')),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view

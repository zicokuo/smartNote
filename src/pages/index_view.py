from flet_core import CrossAxisAlignment, ElevatedButton, Page, View, Text

from core.functions import _
from pages.widgets.welcome import welcome_widget
from settings import APP_CONFIG

view_input: View = None


def page(ctx: Page, route: str):
    view = View(
        route, [
            welcome_widget(),
            Text(APP_CONFIG.get('version')),
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    return view

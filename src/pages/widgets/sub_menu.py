from typing import List

from flet_core import Page, Column, ScrollMode, Text, Container, colors, border, BorderSide

from core.boot import flet_context


@flet_context
def sub_menu_widget(ctx: Page, controls: List = []):
    """
    侧栏菜单
    @type ctx: Page
    @type controls: List
    """
    widget = Container(Column(controls=[
        *controls
    ], width=ctx.window_width / 4,
    ), border=border.only(right=BorderSide(1, colors.BLACK12)))
    return widget

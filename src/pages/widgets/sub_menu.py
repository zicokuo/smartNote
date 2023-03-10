from flet_core import Page, Column, ScrollMode, Text, Container, colors

from core.boot import flet_context


@flet_context
def sub_menu(ctx: Page):
    ctl = Container(Column(controls=[
        Text("1"),
        Text("1"),
        Text("1"),
        Text("1"),
        Text("1"),
    ],
        scroll=ScrollMode.ADAPTIVE,
        width=ctx.window_width / 4,
        height=ctx.window_height,
    ),
    bgcolor=colors.BLACK87)
    return ctl

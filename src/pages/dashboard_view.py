from flet_core import CrossAxisAlignment, Page, View, Container, Row, Card, Image, Column, ImageFit, Text, ImageRepeat, \
    border_radius, IconButton, icons, MainAxisAlignment, colors, ControlEvent

from core.boot import flet_context
from core.functions import _
from pages.widgets.sub_menu import sub_menu_widget
from settings import DEFAULT_IMG
from styles import FONT_SIZE, SUMMARY_SIZE

view_input: View = None


def page(ctx: Page, route: str):
    view = View(
        route, [
            Container(Row([
                sub_menu_widget(controls=[
                    user_card_widget(),
                    post_list_toolbar_widget(),
                ]),
            ]), margin=0)
        ],
        horizontal_alignment=CrossAxisAlignment.CENTER,
        padding=0
    )

    return view


@flet_context
def post_list_toolbar_widget(ctx: Page):
    """
    文章列表工具栏
    @param ctx:
    @return:
    """
    post_list_toolbar = Container(Row([
        IconButton(icons.CREATE_NEW_FOLDER, icon_size=SUMMARY_SIZE, tooltip=_("创建新分类"))
    ],
        alignment=MainAxisAlignment.END),
        bgcolor=colors.BLACK12)
    return post_list_toolbar


@flet_context
def user_card_widget(ctx: Page):
    """
    用户信息卡片
    @param ctx:
    @return:
    """
    user_avatar_ctl = Container(
        Image(f"{DEFAULT_IMG}",
              width=64,
              height=64,
              repeat=ImageRepeat.NO_REPEAT,
              border_radius=border_radius.all(FONT_SIZE),
              fit=ImageFit.CONTAIN))

    widget = Row([
        user_avatar_ctl,
        Column([
            Text("User nick", size=20),
            Text("User role", font_family="PTMono")
        ], spacing=0, expand=True),
        IconButton(icons.LOGOUT, icon_size=SUMMARY_SIZE, tooltip=_("用户登出"), on_click=user_logout_event)
    ])

    return widget

def user_logout_event(e:ControlEvent):

    e.page.go("/")
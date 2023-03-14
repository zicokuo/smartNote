from typing import Optional, List

import pydash
from flet_core import CrossAxisAlignment, Page, View, Container, Row, Image, Column, ImageFit, Text, ImageRepeat, \
    border_radius, IconButton, icons, MainAxisAlignment, colors, ControlEvent, AlertDialog, TextField, TextButton, \
    Switch, Dropdown, dropdown, ListView, UserControl, Ref, ListTile, Card, Markdown, MarkdownExtensionSet, ScrollMode

from core.boot import flet_context
from core.database import db_this
from core.functions import _, log
from core.widgets import dynamic_msg_show
from pages.widgets.sub_menu import sub_menu_widget
from prisma_client import Prisma
from prisma_client.models import User, PostCate
from settings import DEFAULT_IMG
from styles import FONT_SIZE, SUMMARY_SIZE


class CateTreeControl(UserControl):
    cate_tree: List[PostCate]
    lv = ListView(expand=1, spacing=0, auto_scroll=True)

    def build(self):
        self.cate_tree = refresh_cate_tree()
        self.lv.controls = list(
            ListTile(title=Text(f"{item.title}"), data=item, on_click=self
                     .on_cate_item_show) for item in self.cate_tree
        )
        return self.lv

    def refresh(self):
        self.cate_tree = refresh_cate_tree(is_refresh=True)
        self.lv.controls = list(
            ListTile(title=Text(f"{item.title}"), data=item, on_click=self
                     .on_cate_item_show) for item in self.cate_tree
        )
        print(self.cate_tree)
        self.update()

    def on_cate_item_show(self, e: ControlEvent):
        pass


class MarkdownEditor(UserControl):
    content: str = ""
    text_area: TextField = TextField(
        label="Markdown Editor",
        multiline=True,
        expand=1,
        min_lines=20,
        selection_color=colors.LIME,

    )
    view_area: Markdown = Markdown(
        selectable=True,
        extension_set=MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
        expand=1
    )
    ctl = Card(Row([text_area, view_area]), expand=1)

    def build(self):
        self.text_area.on_change = self.on_text_area_change

        self.view_area.value = f"""{self.content}"""

        return self.ctl

    def on_text_area_change(self, e):
        self.content = e.control.value
        self.view_area.value = f"""{self.content}"""
        self.ctl.controls = [self.text_area, self.view_area]
        self.update()


view_input: View = None
cate_tree_ctl = Ref[CateTreeControl]()
markdown_editor_ctl = Ref[MarkdownEditor]()


@flet_context
def refresh_cate_tree(ctx: Page, is_refresh=False):
    cate_tree = ctx.session.get("cate_tree")

    if is_refresh or pydash.is_empty(cate_tree):
        log.debug(_("刷新CateTree"))
        cate_tree = get_cate_tree()
        ctx.session.set("cate_tree", cate_tree)

    return cate_tree


def page(ctx: Page, route: str):
    view = View(
        route, [
            Container(Row([
                sub_menu_widget(controls=[
                    user_card_widget(),
                    post_list_toolbar_widget(),
                    Container(CateTreeControl(ref=cate_tree_ctl), expand=1)
                ]),
                Column([MarkdownEditor(ref=markdown_editor_ctl)], expand=1, scroll=ScrollMode.AUTO)
            ], expand=1), margin=0, expand=1)
        ], horizontal_alignment=CrossAxisAlignment.CENTER,
        padding=0,
    )

    return view


@db_this
def get_cate_tree(db: Prisma):
    cate_tree = db.postcate.find_many(where=dict(is_root=True))
    return cate_tree


@flet_context
def post_list_toolbar_widget(ctx: Page):
    """
    文章列表工具栏
    @param ctx:
    @return:
    """

    post_list_toolbar = Container(Row([
        IconButton(icons.CREATE_NEW_FOLDER,
                   icon_size=FONT_SIZE,
                   tooltip=_("创建新分类"),
                   on_click=on_create_cate_event)
    ], alignment=MainAxisAlignment.END),
        opacity=1,
        bgcolor=colors.BLACK12)
    return post_list_toolbar


def on_create_cate_event(e: ControlEvent):
    bottom_dialog_widget: AlertDialog
    cate_title_ctl = TextField(hint_text=_("输入分类标题"), text_size=FONT_SIZE)
    cate_is_root_ctl = Switch(label=_("跟分类"), value=True)
    cate_parent_ctl = Dropdown(options=[dropdown.Option(_("根分类"))])

    def on_cancel_create_cate_event(e: ControlEvent):
        bottom_dialog_widget.open = False
        refresh_cate_tree(is_refresh=True)
        e.page.update()

    @db_this
    @flet_context
    def on_submit_create_cate_event(e: ControlEvent, db: Prisma, ctx: Page):
        db.postcate.create(data=dict(
            title=cate_title_ctl.value,
            code=cate_title_ctl.value.upper(),
            is_root=cate_is_root_ctl.value,
        ))
        dynamic_msg_show(_("创建分类成功"), _(f"创建{cate_title_ctl.value}分类."))
        bottom_dialog_widget.open = False
        refresh_cate_tree(is_refresh=True)
        cate_tree_ctl.current.refresh()
        e.page.update()

    bottom_dialog_widget = AlertDialog(
        modal=True,
        title=Text(_("新建分类")),
        content=Column([
            cate_title_ctl,
            cate_is_root_ctl,
            cate_parent_ctl,
        ]),
        actions=[
            TextButton(_("创建"), on_click=on_submit_create_cate_event),
            TextButton(_("取消"), on_click=on_cancel_create_cate_event),
        ],
        actions_alignment=MainAxisAlignment.END,

    )
    e.page.dialog = bottom_dialog_widget
    bottom_dialog_widget.open = True
    e.page.update()


@flet_context
def user_card_widget(ctx: Page):
    """
    用户信息卡片
    @param ctx:
    @return:
    """
    login_account: Optional[User] = ctx.session.get('login_account')
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
            Text(f"{pydash.upper_first(login_account.account) or 'User nick'}", size=20, font_family="Harmony"),
            Text(f"{'会员' if login_account.status == 1 else '游客'}", font_family="PTMono")
        ], spacing=0, expand=True),
        IconButton(icons.LOGOUT, icon_size=SUMMARY_SIZE, tooltip=_("用户登出"), on_click=user_logout_event)
    ])

    return widget


def user_logout_event(e: ControlEvent):
    e.page.session.remove('login_account')
    e.page.go("/")

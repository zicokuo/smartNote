import sys
from functools import wraps
from importlib import import_module
from typing import List, Optional, Callable, T

import flet
import pydash
from flet_core import RouteChangeEvent, CrossAxisAlignment, MainAxisAlignment, Page, KeyboardEvent, Theme

from prisma_client import Prisma
from prisma_client.models import User
from .database import db_this
from .functions import _, log
from .vos import RouteItemVo
from settings import PAGES, FONTS, APP_CONFIG, DEBUG

# 全局缓存对象
boot_ctx = {}


def auto_import(item: RouteItemVo):
    log.info(_(f"自动加载{item.route}挂在{item.filename}"))
    if not item.filename.startswith("apps"):
        pydash.set_(boot_ctx,
                    f"routers.{item.route}",
                    import_module(name=f".{item.filename}", package="pages").page, )
    else:
        pydash.set_(boot_ctx,
                    f"routers.{item.route}",
                    import_module(name=f"{item.filename}",).page, )


def init_app(routers: Optional[List[RouteItemVo]] = None):
    """
    应用入口
    :param routers: 自定义路由表
    :return:
    """
    sys.path.append(r'/src/')
    # 自动加载
    pydash.for_in(PAGES, lambda v, k: auto_import(RouteItemVo(route=k, filename=v))) if PAGES is not None else None
    pydash.for_each(routers, auto_import) if routers is not None else None

    # 应用开始
    flet.app(target=boot, assets_dir="../assets/")


@db_this
def retrieve_session(session_account: str, db: Prisma) -> User:
    user = db.user.find_first(where={'account': session_account})
    return user


def boot(ctx: flet.Page):
    pydash.set_(boot_ctx, 'ctx', ctx)

    # 加载字体
    if FONTS:
        ctx.fonts = FONTS

    # 加载 APP_CONFIG:
    for v in APP_CONFIG:
        pydash.set_(ctx, v, APP_CONFIG[v])

    ctx.horizontal_alignment = CrossAxisAlignment.CENTER
    ctx.vertical_alignment = MainAxisAlignment.CENTER

    ctx.on_route_change = route_change
    ctx.on_view_pop = view_pop

    ctx.go(ctx.route)


def flet_context(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: Callable[..., T], **kwargs: Callable[..., T]):
        ctx: flet.Page = pydash.get(boot_ctx, 'ctx')
        res = func(ctx=ctx, *args, **kwargs)
        pydash.set_(boot_ctx, 'ctx', ctx)
        return res

    return wrapper


def flet_view(func, path: str):
    pydash.set_(boot_ctx, f'routers.{path}', func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx: flet.Page = pydash.get(boot_ctx, 'ctx')
        route_path, view = func(ctx=ctx, *args, **kwargs)
        pydash.set_(boot_ctx, 'ctx', ctx)
        return view

    return wrapper


@flet_context
def route_change(route: RouteChangeEvent, ctx: Page):
    ctx.views.clear()
    # 检查 会话
    if ctx.session.get('login_account') is None:
        session_account = ctx.client_storage.get('login_account')

        if session_account:
            session_user = retrieve_session(session_account)
            ctx.session.set('login_account', session_user)

    ctx_view = pydash.get(boot_ctx, f"routers.{route.data}")
    log.debug(_(f"路由跳转{route.data},视图{ctx_view}"))

    if ctx_view:
        ctx.views.append(ctx_view(ctx, ctx.route))

    else:
        ctx.views.append(
            flet.View(
                "/",
                [
                    flet.AppBar(title=flet.Text("着了个陆"), bgcolor=flet.colors.SURFACE),
                    flet.ElevatedButton("登了个录", on_click=lambda _: ctx.go("/login")),
                    # flet.ElevatedButton("首了个页", on_click=lambda _: ctx.go("/index")),
                ],
            )
        )
    if DEBUG:
        ctx.on_keyboard_event = keybard_event

    ctx.update()


@flet_context
def view_pop(view, ctx: Page):
    ctx.views.pop()
    top_view = ctx.views[-1]
    ctx.go(top_view.route)


def keybard_event(e: KeyboardEvent):
    """
    调试模式
    @param e:
    @return:
    """
    if e.key == "H" and e.ctrl:
        log.debug(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")
        e.page.show_semantics_debugger = not e.page.show_semantics_debugger
        e.page.update()

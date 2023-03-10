from functools import wraps
from importlib import import_module
from typing import List, Optional, Callable, T

import flet
import pydash
from flet_core import RouteChangeEvent, CrossAxisAlignment, MainAxisAlignment

from core.functions import _, log
from core.vos import RouteItemVo
from settings import PAGES, FONTS, APP_CONFIG

# 全局缓存对象
boot_ctx = {}


def auto_import(item: RouteItemVo):
    log.info(_(f"自动加载{item.route}挂在{item.filename}"))
    pydash.set_(boot_ctx,
                f"routers.{item.route}",
                import_module(name=f".{item.filename}", package="pages").page, )


def init_app(routers: Optional[List[RouteItemVo]] = None):
    """
    应用入口
    :param routers: 自定义路由表
    :return:
    """

    # 自动加载
    pydash.for_in(PAGES, lambda v, k: auto_import(RouteItemVo(route=k, filename=v))) if PAGES is not None else None
    pydash.for_each(routers, auto_import) if routers is not None else None

    # 应用开始
    flet.app(target=boot, assets_dir="../assets")


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
    def wrapper(*args, **kwargs):
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
def route_change(route: RouteChangeEvent, ctx):
    ctx.views.clear()
    ctx_view = pydash.get(boot_ctx, f"routers.{route.data}")

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

    ctx.update()


@flet_context
def view_pop(view, ctx):
    ctx.views.pop()
    top_view = ctx.views[-1]
    ctx.go(top_view.route)

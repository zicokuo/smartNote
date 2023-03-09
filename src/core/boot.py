from functools import wraps
from importlib import import_module
from typing import List

import flet
import pydash
from flet_core import RouteChangeEvent
from pydantic import BaseModel

boot_ctx = {}


class RouteItem(BaseModel):
    route: str
    filename: str = None


def auto_import(item: RouteItem):
    pydash.set_(boot_ctx,
                f"routers.{item.route}",
                import_module(name=f".{item.filename}", package="pages").page, )


def init_app(routers: List[RouteItem]):
    # 加载页面
    pydash.for_each(routers, auto_import)
    flet.app(target=boot, assets_dir="assets")


def boot(ctx: flet.Page):
    pydash.set_(boot_ctx, 'ctx', ctx)
    ctx.on_route_change = route_change
    ctx.on_view_pop = view_pop
    ctx.go(ctx.route)


def flet_context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ctx: flet.Page = pydash.get(boot_ctx, 'ctx')
        res = f(ctx=ctx, *args, **kwargs)
        pydash.set_(boot_ctx, 'ctx', ctx)
        return res

    return wrapper


def flet_view(f, path: str):
    pydash.set_(boot_ctx, f'routers.{path}', f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        ctx: flet.Page = pydash.get(boot_ctx, 'ctx')
        route_path, view = f(ctx=ctx, *args, **kwargs)
        pydash.set_(boot_ctx, 'ctx', ctx)
        return view

    return wrapper


@flet_context
def route_change(route: RouteChangeEvent, ctx):

    ctx.views.clear()
    ctx_view = pydash.get(boot_ctx, f'routers.{route.data}')

    if ctx_view:
        ctx.views.append(ctx_view(ctx, ctx.route))

    else:
        ctx.views.append(
            flet.View(
                "/",
                [
                    flet.AppBar(title=flet.Text("着了个陆"), bgcolor=flet.colors.SURFACE),
                    flet.ElevatedButton("登了个录", on_click=lambda _: ctx.go("/login")),
                ],
            )
        )

    ctx.update()


@flet_context
def view_pop(view, ctx):
    ctx.views.pop()
    top_view = ctx.views[-1]
    ctx.go(top_view.route)

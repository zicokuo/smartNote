from functools import wraps

import flet
import pydash

from src.pages.login_view import login_view

boot_ctx = {}


def init_app():
    flet.app(target=boot)


def boot(ctx: flet.Page):
    pydash.set_(boot_ctx, 'ctx', ctx)
    pydash.set_(boot_ctx, 'routers', {
        "/login": login_view
    })

    ctx.on_route_change = route_change
    ctx.on_view_pop = view_pop
    ctx.go(ctx.route)


def flet_context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ctx: flet.Page = pydash.get(boot_ctx, 'ctx')
        res = f(ctx=ctx, *args, **kwargs, )
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
def route_change(route, ctx):
    ctx.views.clear()
    ctx_view = pydash.get(boot_ctx, f'routers.{ctx.route}')
    if ctx_view:
        ctx.views.append(ctx_view(ctx))
    else:
        ctx.views.append(
            flet.View(
                "/",
                [
                    flet.AppBar(title=flet.Text("Flet app"), bgcolor=flet.colors.SURFACE_VARIANT),
                    flet.ElevatedButton("Visit Store", on_click=lambda _: ctx.go("/login")),
                ],
            )
        )

    # if ctx.route == "/store":
    #     ctx.views.append(
    #         flet.View(
    #             "/store",
    #             [
    #                 flet.AppBar(title=flet.Text("Store"), bgcolor=flet.colors.SURFACE_VARIANT),
    #                 flet.ElevatedButton("Go Home", on_click=lambda _: ctx.go("/")),
    #             ],
    #         )
    #     )

    ctx.update()


@flet_context
def view_pop(view, ctx):
    ctx.views.pop()
    top_view = ctx.views[-1]
    ctx.go(top_view.route)

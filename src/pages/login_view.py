import flet


def page(ctx: flet.Page, route: str):
    view: flet.View = flet.View(
        route,
        [
            flet.Text('牛逼')
        ]
    )
    return view

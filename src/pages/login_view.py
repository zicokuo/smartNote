import flet


def login_view(ctx):
    path = '/login'
    view: flet.View = flet.View(
        path,
        [
            flet.Text('牛逼')
        ]
    )
    return view

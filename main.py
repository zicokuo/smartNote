from src.core.boot import init_app, RouteItem

if __name__ == '__main__':
    routers = [
        RouteItem(route="/login", filename="login_view")
    ]
    init_app(routers)

from src.core.boot import init_app
from src.pages import login_view

if __name__ == '__main__':
    routers = {
        "/login": login_view
    }
    init_app()

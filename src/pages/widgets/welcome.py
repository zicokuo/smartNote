import random
import threading
from time import sleep

import flet
import pydash
from flet_core.alignment import center

from core.boot import flet_context
from core.functions import _
from pages.widgets.login_form import login_form_widget
from settings import APP_CONFIG
from styles import FONT_SIZE

text_list = ["Welcome", "欢迎", "ようこそ", "Benvenuto", "Accueillir"]


@flet_context
def welcome_widget(ctx: flet.Page):
    """
    欢迎
    """
    ctl = flet.Column(
        [flet.Container(
            content=
            flet.Column(
                controls=[
                    flet.Container(
                        content=WelcomeControl(),
                        alignment=center,
                        height=ctx.height / 2
                    ),
                    login_form_widget(),
                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                width=pydash.min_([FONT_SIZE * 20, ])
            ),
        )])
    return ctl


class WelcomeControl(flet.UserControl):

    def __init__(self):
        super().__init__()
        self.running = None
        self.th = None
        self.welcome_text = text_list[random.randint(0, len(text_list)) - 1]

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_timer(self):
        while self.running:
            self.ctl.animate = flet.Animation(duration=1)
            txt = text_list[random.randint(0, len(text_list)) - 1]
            self.ctl.value = txt
            self.ctl.size = pydash.min_([APP_CONFIG.get('window_width') / len(txt) * 0.8, FONT_SIZE*4], FONT_SIZE*2)
            self.update()
            sleep(3)

    def build(self):
        self.ctl = flet.Text(self.welcome_text,
                             color=flet.colors.BLUE_400,
                             font_family="PTMono")
        return self.ctl

import random
import threading
from time import sleep

import flet
import pydash
from flet_core.alignment import center

from core.boot import flet_context
from core.functions import _
from settings import APP_CONFIG

text_list = ["Welcome", "欢迎", "ようこそ", "Benvenuto", "Accueillir"]
account_input_ctl = flet.TextField(prefix_icon=flet.icons.FAVORITE, hint_text=_("Input your name"), )


@flet_context
def welcome_ctl(ctx: flet.Page):
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
                    account_input_ctl
                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            ),
        )])
    return ctl


class WelcomeControl(flet.UserControl):

    def __init__(self):
        super().__init__()
        self.th = None
        self.welcome_text = text_list[random.randint(0, len(text_list)) - 1]

    def did_mount(self):
        self.runnning = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.runnning = False

    def update_timer(self):
        while self.runnning:
            self.ctl.animate = flet.Animation(duration=1)
            txt = text_list[random.randint(0, len(text_list)) - 1]
            self.ctl.value = txt
            self.ctl.size = pydash.min_([APP_CONFIG.get('window_width') / len(txt) * 0.8,64],32)
            self.update()
            sleep(3)


    def build(self):
        self.ctl = flet.Text(self.welcome_text,
                             size=64,
                             color=flet.colors.BLUE_400,
                             font_family="PTMono")
        return self.ctl

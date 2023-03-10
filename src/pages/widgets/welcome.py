import random
import threading
from time import sleep

import flet

from core.boot import flet_context
from core.functions import _, log

text_list = ["Welcome", "欢迎", "ようこそ", "ยินดีต้อนรับ", "тавтай морил"]
account_input_ctl = flet.TextField(prefix_icon=flet.icons.FAVORITE, hint_text=_("Input your name"), )


@flet_context
def welcome_ctl(ctx: flet.Page):
    ctl = flet.Column(
        [flet.Container(
            content=
            flet.Column(
                controls=[
                    WelcomeControl(),
                    account_input_ctl
                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER
            ),
            margin=64,
            padding=64,
        )])
    return ctl


class WelcomeControl(flet.UserControl):

    def __init__(self):
        super().__init__()
        self.welcome_text = text_list[random.randint(0, len(text_list)) - 1]

    def did_mount(self):
        self.runnning = True
        self.th = threading.Thread(target=self.update_timer, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.runnning = False

    def update_timer(self):
        while self.runnning:
            self.ctl.value = text_list[random.randint(0, len(text_list)) - 1]
            self.update()
            sleep(3)

    def build(self):
        self.ctl = flet.Text(self.welcome_text,
                             size=64,
                             color=flet.colors.BLUE_400,
                             font_family="PTMono")
        return self.ctl

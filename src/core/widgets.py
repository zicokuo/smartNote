from enum import Enum

from flet_core import FloatingActionButton, ControlEvent, Page, colors, icons, SnackBar, Column, Text

from core.boot import flet_context
from styles import FONT_SIZE, SUMMARY_SIZE


def app_banner_widget():
    pass


class StatusEnum(Enum):
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"


snack_bar_colors = dict(
    info=colors.BLACK54,
    success=colors.GREEN_300,
    error=colors.RED_300,
)


@flet_context
def dynamic_msg_show(title: str, msg: str, is_error=None, action="OK", ctx: Page = None, ):
    """
    :param title:
    :param msg:
    :param ctx:
    :param is_error:
    :param action:
    :return:
    """
    ctx.snack_bar = SnackBar(Column([
        Text(f"{title}", size=SUMMARY_SIZE / 1.5),
        Text(f"{msg}", size=FONT_SIZE)
    ]),
        bgcolor=snack_bar_colors.get(
            (StatusEnum.INFO if is_error is None else StatusEnum.ERROR if is_error else StatusEnum.SUCCESS).value),
        action=action)

    ctx.snack_bar.open = True
    ctx.update()

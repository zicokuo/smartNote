from typing import Callable

import flet as ft
from pydantic import BaseModel

from core.functions import _


class BulkModifyFilesBannerWidgetValuesVo(BaseModel):
    can_scale: bool = False
    scale_width: int = False


class BulkModifyFilesBannerWidget(ft.UserControl):
    """
    批量修改文件名配置通栏
    """
    banner_ctl: ft.Container
    scale_switch_ctl = ft.Switch(label=_("启用缩放"))
    scale_width_ctl = ft.TextField(label=_("宽度(px)"))

    def build(self):
        banner_ctl = ft.Container(
            ft.Column([
                ft.Row([
                    self.scale_switch_ctl])
            ])
        )

        return banner_ctl

    @property
    def submit_data(self):
        """
        获取data
        @return:
        """
        vo = BulkModifyFilesBannerWidgetValuesVo(
            can_scale=self.scale_switch_ctl.value,
            scale_width=self.scale_switch_ctl.value or 0
        )

        return vo

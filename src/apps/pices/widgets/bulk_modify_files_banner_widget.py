import flet as ft
from pydantic import BaseModel

from core.functions import _


class BulkModifyFilesBannerWidgetValuesVo(BaseModel):
    can_scale: bool = False
    scale_width: int = False


class BulkModifyFilesBannerWidget(ft.UserControl):
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

    def get_data(self):
        vo = BulkModifyFilesBannerWidgetValuesVo(
            can_scale=self.scale_switch_ctl.value,
            scale_width=self.scale_switch_ctl.value or 0
        )

        return vo
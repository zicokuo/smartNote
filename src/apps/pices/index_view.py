import os
import sys
from shutil import copyfile
from typing import List

from arrow import Arrow

from apps.pices.widgets.bulk_modify_files_banner_widget import BulkModifyFilesBannerWidget, \
    BulkModifyFilesBannerWidgetValuesVo

if sys.platform == 'darwin':
    from PIL import Image as PilImage
else:
    from third.pillow import Image as PilImage

import flet as ft
from pydantic import BaseModel

from core.functions import _
from styles import FONT_SIZE, UNIT_SIZE, SUMMARY_SIZE

selected_files = ft.Text(expand=1)


class FolderItemVo(BaseModel):
    """
    文件夹Vo
    """
    name: str
    path: str
    is_dir: bool


class FileItemVo(BaseModel):
    """
    文件Vo
    """
    name: str
    path: str
    ext: str
    size: str


def drag_will_accept(e):
    e.control.content.border = ft.border.all(
        2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
    )
    e.control.width = 100
    e.control.height = 100

    e.control.update()


def drag_accept(e):
    src = page.get_control(e.src_id)
    e.control.content.bgcolor = src.content.bgcolor
    e.control.content.border = None
    e.control.update()


def drag_leave(e):
    e.control.content.border = None
    e.control.width = 0
    e.control.height = 0
    e.control.update()


def on_banner_sure_event(e: ft.ControlEvent):
    """
    批量修改文件名通栏确认事件
    @param e:
    @return:
    """
    data: BulkModifyFilesBannerWidgetValuesVo = banner_ref.current.content.submit_data
    print(data)
    pass


def on_banner_close_event(e: ft.ControlEvent):
    banner_ref.current.open = not banner_ref.current.open
    banner_ref.current.update()


def on_bulk_modify_filename_show_event(e: ft.ControlEvent):
    inner_ctl = BulkModifyFilesBannerWidget()

    # 通栏
    banner_ref.current.content = inner_ctl
    banner_ref.current.open = not banner_ref.current.open
    banner_ref.current.update()


def on_sure_bulk_modify_files_event(e: ft.ControlEvent):
    """
    批量修改文件名
    @param e:
    @return:
    """
    global folder_tree_selected_ctl
    if folder_tree_selected_ctl:
        # 当前文件夹路径
        cur_path: str = folder_tree_selected_ctl.data.path
        # 当前备份文件夹路径
        cur_backup_path: str = os.path.join(cur_path, f'origin_{Arrow.now().format("YYYYMMDDHHmmss")}')

        os.makedirs(os.path.join(cur_backup_path))

        folder_name = os.path.basename(cur_path)
        idx = 0
        for filename in os.listdir(cur_path):  # 获取当前目录下的所有文件名
            if filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.jpg'):  # 判断文件名

                # 读取文件大小
                file_path = os.path.join(cur_path, filename)
                # 备份源文件
                copyfile(file_path, os.path.join(cur_backup_path, filename))
                img = PilImage.open(file_path)

                addition = ""

                if img.height == 1200:
                    addition = "WP"
                elif 1600 >= img.height < 2000:
                    addition = "PLUS"
                elif img.height == 2000:
                    addition = "TW"

                img.close()

                os.rename(file_path,
                          f"{cur_path}/{folder_name}-{addition}{'{:0>2d}'.format(idx)}.{filename.split('.')[-1]}")
                idx += 1

    # 修改之后刷新列表
    selected_folder_vo and load_files_by_path(selected_folder_vo.path)


def on_pice_hover_event(e: ft.ControlEvent):
    e.control.border = ft.border.all(1, ft.colors.BLACK38) if e.control.border is None else None
    e.control.update()


def load_files_by_path(cur_path):
    file_list: List[FileItemVo] = []
    if cur_path:
        for file in os.scandir(cur_path):
            if file.is_file():
                file_list.append(FileItemVo(
                    name=file.name,
                    size=file.stat().st_size,
                    ext=os.path.splitext(file.name)[1],
                    path=os.path.join(cur_path, file.name)
                ))

    files_area_ref.current.controls = list(
        ft.Container(
            ft.Column([
                ft.Image(
                    src=f"{file.path}",
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    aspect_ratio=1,
                    data=file,
                    semantics_label=f"{file.name}",
                    expand=1
                ),
                ft.Text(f"{file.name}", size=SUMMARY_SIZE, text_align=ft.TextAlign.CENTER, no_wrap=False)
            ], aspect_ratio=1, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=FONT_SIZE,
            on_hover=on_pice_hover_event,
            margin=FONT_SIZE,
        )
        for file in file_list
    )
    files_area_ref.current.update()


def on_folder_click_event(e: ft.ControlEvent):
    """
    点击文件夹
    :param e:
    :return:
    """
    global folder_tree_selected_ctl
    global selected_folder_vo
    selected_folder_vo = e.control.data
    folder_tree_selected_ctl = e.control

    for folder_ctl in folder_tree_ref.current.folder_list_ctl.controls:
        folder_ctl: ft.ListTile
        if folder_ctl.data.is_dir:
            if folder_ctl.data.path == e.control.data.path:
                folder_ctl.selected = True
                folder_ctl.leading = ft.Icon(ft.icons.FOLDER_OPEN, color=ft.colors.PRIMARY)
            else:
                folder_ctl.selected = False
                folder_ctl.leading = ft.Icon(ft.icons.FOLDER, color=ft.colors.SECONDARY)

        folder_ctl.update()

    # 扫描文件
    cur_path = e.control.data.path
    load_files_by_path(cur_path)
    folder_tree_ref.current.update()
    e.page.update()


def load_root_folder_by_path(cur_path: str):
    root_folder_path_input_ref.current.value = os.path.abspath(cur_path)
    # 读取文件目录
    folder_list = []
    for folder in os.scandir(cur_path):
        folder_list.append(FolderItemVo(
            name=folder.name,
            path=os.path.join(cur_path, folder.name),
            is_dir=folder.is_dir())) if folder.is_dir() else None

    parent_folder_path: str = os.path.dirname(cur_path)
    folder_tree_ref.current.folder_list_ctl.controls = [ft.ListTile(
        data=FolderItemVo(
            name=parent_folder_path,
            path=parent_folder_path,
            is_dir=False,
        ),
        dense=True,
        leading=ft.Icon(ft.icons.TURN_LEFT, color=ft.colors.PRIMARY),
        title=ft.Text(_(f"..")),
        content_padding=UNIT_SIZE,
        on_click=lambda _: load_root_folder_by_path(parent_folder_path)
    ), ] + list(ft.ListTile(
        data=folder,
        dense=True,
        leading=ft.Icon(ft.icons.FOLDER, color=ft.colors.SECONDARY),
        trailing=ft.IconButton(data=folder, icon=ft.icons.KEYBOARD_TAB, on_click=on_folder_item_go_event
                               ),
        title=ft.Text(_(f"{folder.name}")),
        content_padding=UNIT_SIZE,
        on_click=on_folder_click_event,
    ) for folder in folder_list)

    # log.debug("目录树")
    # log.debug(folder_list)

    folder_tree_ref.current.update()
    root_folder_path_input_ref.current.update()


def on_pick_files_result_event(e: ft.FilePickerResultEvent):
    """
    选择文件路径事件
    @param e:
    @return:
    """
    if e.files:
        cur_path = os.path.dirname(e.files[0].path)
        load_root_folder_by_path(cur_path)


def on_root_folder_path_submit_event(e: ft.ControlEvent):
    load_root_folder_by_path(e.control.value)


def on_folder_item_go_event(e: ft.ControlEvent):
    load_root_folder_by_path(e.control.data.path)


class FolderTree(ft.UserControl):
    """
    文件树
    """
    toolbar_ctl = ft.Row(height=FONT_SIZE * 2, alignment=ft.MainAxisAlignment.END)
    folder_list_ctl = ft.Column(scroll=True, expand=1)

    def build(self):
        # self.toolbar_ctl.controls = [
        #     selected_files,
        #     IconButton(icons.FOLDER, tooltip=_("选择根目录"), on_click=lambda _: pick_files_dialog.pick_files(
        #     ))
        # ]

        return self.folder_list_ctl

    def update(self):
        self.folder_list_ctl.update()
        super().update()


# 目录树
folder_tree_ref = ft.Ref[FolderTree]()
# 文件选择器
pick_files_dialog = ft.FilePicker(on_result=on_pick_files_result_event)
# 根目录路径输入
root_folder_path_input_ref = ft.Ref[ft.TextField]()
# 文件操作区域
files_area_ref = ft.Ref[ft.GridView]()
# 文件夹树单项
folder_tree_selected_ctl: ft.ListTile = None
selected_folder_vo = None
# 通栏
banner_ref = ft.Ref[ft.Banner]()


def page(ctx: ft.Page, route: str):
    """
    改图工具
    :param ctx:
    :param route:
    :return:
    """
    v = ft.View(route, [
        ft.AppBar(title=ft.Text(_(f"改图工具 - alpha")), bgcolor=ft.colors.BLACK12,
                  actions=[
                      ft.IconButton(icon=ft.icons.TEXT_ROTATION_NONE,
                                    tooltip=_("文件名批量修改"),
                                    on_click=on_bulk_modify_filename_show_event)
                  ]),
        ft.Row([
            ft.TextField(ref=root_folder_path_input_ref, label=_("文件夹路径"), dense=True, content_padding=UNIT_SIZE,
                         on_submit=on_root_folder_path_submit_event),
            ft.IconButton(icon=ft.icons.FOLDER_OPEN, on_click=lambda _: pick_files_dialog.pick_files())
        ]),
        ft.Row([
            ft.Container(
                FolderTree(ref=folder_tree_ref, ),
                width=ctx.width / 5,
                bgcolor=ft.colors.BLACK12, margin=0
            ),
            ft.Column([ft.GridView(
                ref=files_area_ref,
                spacing=UNIT_SIZE,
                expand=1,
                runs_count=UNIT_SIZE,
                child_aspect_ratio=1.0,
                run_spacing=UNIT_SIZE,
                padding=UNIT_SIZE,
            )], width=ctx.width / 4, auto_scroll=True, expand=1)
        ], expand=1, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
    ])

    ctx.overlay.append(pick_files_dialog)
    ctx.banner = ft.Banner(ref=banner_ref, open=False, actions=[
        ft.TextButton(_("确定"), on_click=on_banner_sure_event),
        ft.TextButton(_("取消"), on_click=on_banner_close_event)
    ])
    return v

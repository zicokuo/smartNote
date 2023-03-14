import os
from typing import List

import pydash
from flet_core import Page, View, Text, AppBar, colors, Row, UserControl, IconButton, icons, Ref, Column, ListTile, \
    MainAxisAlignment, Container, FilePicker, FilePickerResultEvent, TextField, Card, GridView, ControlEvent, Icon, \
    Image, ImageFit, ImageRepeat, border_radius, Border, border, Draggable, DragTarget
from pydantic import BaseModel

from core.functions import _, log
from styles import FONT_SIZE, UNIT_SIZE

selected_files = Text(expand=1)


class FolderItemVo(BaseModel):
    name: str
    path: str
    is_dir: bool


class FileItemVo(BaseModel):
    name: str
    path: str
    ext: str
    size: str


def drag_will_accept(e):
    e.control.content.border = border.all(
        2, colors.BLACK45 if e.data == "true" else colors.RED
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


def on_folder_click_event(e: ControlEvent):
    """
    点击文件夹
    :param e:
    :return:
    """
    e.control.selected = True
    # 扫描文件
    cur_path = e.control.data.path
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

    pics_area_ref.current.controls = list(
        Draggable(
            group="pices",
            content=Column([Container(
                Image(
                    src=f"{file.path}",
                    fit=ImageFit.CONTAIN,
                    repeat=ImageRepeat.NO_REPEAT,
                    border_radius=border_radius.all(FONT_SIZE),
                    data=file,
                ), border=border.all(1, colors.BLACK38)
            ), Text(f"{file.name}")

            ]),
            content_feedback=Container(Image(
                tooltip=f"{file.name}",
                src=f"{file.path}",
                fit=ImageFit.CONTAIN,
                repeat=ImageRepeat.NO_REPEAT,
                border_radius=border_radius.all(FONT_SIZE),
                data=file,
                width=64,
            ), border=border.all(1, colors.BLACK38)),
        )
        for file in file_list
    )
    pics_area_ref.current.update()


def on_pick_files_result_event(e: FilePickerResultEvent):
    # selected_files.value = (
    #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
    # )
    # selected_files.update()
    if e.files:
        cur_path = os.path.dirname(e.files[0].path)
        file_path_input_ref.current.value = cur_path
        # 读取文件目录
        folder_list = []
        for folder in os.scandir(cur_path):
            folder_list.append(FolderItemVo(
                name=folder.name,
                path=os.path.join(cur_path, folder.name),
                is_dir=folder.is_dir())) if folder.is_dir() else None
        file_tree_ref.current.folder_list_ctl.controls = list(
            ListTile(
                data=folder,
                dense=True,
                leading=Icon(icons.FOLDER_OPEN, color=colors.PRIMARY),
                title=Text(_(f"{folder.name}")),
                content_padding=UNIT_SIZE,
                on_click=on_folder_click_event
            ) for folder in folder_list
        )

        log.debug("目录树")
        log.debug(folder_list)

        file_tree_ref.current.folder_list_ctl.update()
        file_path_input_ref.current.update()


class FileTree(UserControl):
    """
    文件树
    """
    toolbar_ctl = Row(height=FONT_SIZE * 2, alignment=MainAxisAlignment.END)
    folder_list_ctl = Column(scroll=True)

    def build(self):
        # self.toolbar_ctl.controls = [
        #     selected_files,
        #     IconButton(icons.FOLDER, tooltip=_("选择根目录"), on_click=lambda _: pick_files_dialog.pick_files(
        #     ))
        # ]

        return self.folder_list_ctl


file_tree_ref = Ref[FileTree]()
pick_files_dialog = FilePicker(on_result=on_pick_files_result_event)
file_path_input_ref = Ref[TextField]()
pics_area_ref = Ref[GridView]()


def page(ctx: Page, route: str):
    """
    改图工具
    :param ctx:
    :param route:
    :return:
    """
    v = View(route, [
        AppBar(title=Text(_(f"改图工具 - alpha")), bgcolor=colors.BLACK12),
        Row([
            TextField(ref=file_path_input_ref, label=_("文件夹路径"), dense=True, content_padding=UNIT_SIZE),
            IconButton(icon=icons.FOLDER_OPEN, on_click=lambda _: pick_files_dialog.pick_files())
        ]),
        Row([
            Container(FileTree(ref=file_tree_ref, ), width=ctx.width / 5, bgcolor=colors.BLACK12, margin=0),
            Column([GridView(
                ref=pics_area_ref,
                spacing=UNIT_SIZE,
                expand=1,
                runs_count=UNIT_SIZE,
                child_aspect_ratio=1.0,
                run_spacing=UNIT_SIZE,
                padding=UNIT_SIZE,
            )], width=ctx.width / 4, auto_scroll=True, expand=1)
        ], expand=1)
    ])

    ctx.overlay.append(pick_files_dialog)
    return v

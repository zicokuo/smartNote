import os
from typing import List

import pydash
from third.pillow import Image as PilImage
from flet_core import Page, View, Text, AppBar, colors, Row, UserControl, IconButton, icons, Ref, Column, ListTile, \
    MainAxisAlignment, Container, FilePicker, FilePickerResultEvent, TextField, GridView, ControlEvent, Icon, \
    Image, ImageFit, ImageRepeat, border, TextAlign, CrossAxisAlignment
from pydantic import BaseModel

from core.functions import _, log
from styles import FONT_SIZE, UNIT_SIZE, SUMMARY_SIZE

selected_files = Text(expand=1)


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


def on_bulk_modify_filename_event(e: ControlEvent):
    """
    批量修改文件名
    @param e:
    @return:
    """
    global folder_tree_selected_ctl
    if folder_tree_selected_ctl:
        cur_path: str = folder_tree_selected_ctl.data.path
        folder_name = os.path.basename(cur_path)
        idx = 0
        for filename in os.listdir(cur_path):  # 获取当前目录下的所有文件名
            if filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.jpg'):  # 判断文件名
                # 读取文件大小
                file_path = os.path.join(cur_path, filename)
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


def on_pice_hover_event(e: ControlEvent):
    e.control.border = border.all(1, colors.BLACK38) if e.control.border is None else None
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
        Container(
            Column([
                Image(
                    src=f"{file.path}",
                    fit=ImageFit.CONTAIN,
                    repeat=ImageRepeat.NO_REPEAT,
                    aspect_ratio=1,
                    data=file,
                    semantics_label=f"{file.name}",
                    expand=1
                ),
                Text(f"{file.name}", size=SUMMARY_SIZE, text_align=TextAlign.CENTER, no_wrap=False)
            ], aspect_ratio=1, tight=True, horizontal_alignment=CrossAxisAlignment.CENTER),
            padding=FONT_SIZE,
            on_hover=on_pice_hover_event,
            margin=FONT_SIZE,
        )
        for file in file_list
    )
    files_area_ref.current.update()


def on_folder_click_event(e: ControlEvent):
    """
    点击文件夹
    :param e:
    :return:
    """
    global folder_tree_selected_ctl, selected_folder_vo
    selected_folder_vo = e.control.data
    folder_tree_selected_ctl = e.control
    # 扫描文件
    cur_path = e.control.data.path
    load_files_by_path(cur_path)
    folder_tree_ref.current.folder_list_ctl.update()


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
    folder_tree_ref.current.folder_list_ctl.controls = [ListTile(
        data=FolderItemVo(
            name=parent_folder_path,
            path=parent_folder_path,
            is_dir=True,
        ),
        dense=True,
        leading=Icon(icons.TURN_LEFT, color=colors.PRIMARY),
        title=Text(_(f"..")),
        content_padding=UNIT_SIZE,
        on_click=lambda _: load_root_folder_by_path(parent_folder_path)
    ), ] + list(ListTile(
        data=folder,
        dense=True,
        leading=Icon(
            icons.FOLDER_OPEN if pydash.get(selected_folder_vo, 'path') == folder.path else icons.FOLDER,
            color=colors.PRIMARY),
        trailing=IconButton(
            data=folder,
            icon=icons.KEYBOARD_TAB,
            on_click=on_folder_item_go_event
        ),
        title=Text(_(f"{folder.name}")),
        content_padding=UNIT_SIZE,
        on_click=on_folder_click_event,
    ) for folder in folder_list)

    log.debug("目录树")
    log.debug(folder_list)

    folder_tree_ref.current.update()
    root_folder_path_input_ref.current.update()


def on_pick_files_result_event(e: FilePickerResultEvent):
    # selected_files.value = (
    #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
    # )
    # selected_files.update()
    if e.files:
        cur_path = os.path.dirname(e.files[0].path)
        load_root_folder_by_path(cur_path)


def on_root_folder_path_submit_event(e: ControlEvent):
    load_root_folder_by_path(e.control.value)


def on_folder_item_go_event(e: ControlEvent):
    load_root_folder_by_path(e.control.data.path)


class FolderTree(UserControl):
    """
    文件树
    """
    toolbar_ctl = Row(height=FONT_SIZE * 2, alignment=MainAxisAlignment.END)
    folder_list_ctl = Column(scroll=True, expand=1)

    def build(self):
        # self.toolbar_ctl.controls = [
        #     selected_files,
        #     IconButton(icons.FOLDER, tooltip=_("选择根目录"), on_click=lambda _: pick_files_dialog.pick_files(
        #     ))
        # ]

        return self.folder_list_ctl


folder_tree_ref = Ref[FolderTree]()
pick_files_dialog = FilePicker(on_result=on_pick_files_result_event)
root_folder_path_input_ref = Ref[TextField]()
files_area_ref = Ref[GridView]()
folder_tree_selected_ctl: ListTile = None
selected_folder_vo = None


def page(ctx: Page, route: str):
    """
    改图工具
    :param ctx:
    :param route:
    :return:
    """
    v = View(route, [
        AppBar(title=Text(_(f"改图工具 - alpha")), bgcolor=colors.BLACK12,
               actions=[
                   IconButton(icon=icons.TEXT_ROTATION_NONE, tooltip=_("文件名批量修改"),
                              on_click=on_bulk_modify_filename_event)
               ]),
        Row([
            TextField(ref=root_folder_path_input_ref, label=_("文件夹路径"), dense=True, content_padding=UNIT_SIZE,
                      on_submit=on_root_folder_path_submit_event),
            IconButton(icon=icons.FOLDER_OPEN, on_click=lambda _: pick_files_dialog.pick_files())
        ]),
        Row([
            Container(
                FolderTree(ref=folder_tree_ref, ),
                width=ctx.width / 5,
                bgcolor=colors.BLACK12, margin=0
            ),
            Column([GridView(
                ref=files_area_ref,
                spacing=UNIT_SIZE,
                expand=1,
                runs_count=UNIT_SIZE,
                child_aspect_ratio=1.0,
                run_spacing=UNIT_SIZE,
                padding=UNIT_SIZE,
            )], width=ctx.width / 4, auto_scroll=True, expand=1)
        ], expand=1, vertical_alignment=CrossAxisAlignment.STRETCH)
    ])

    ctx.overlay.append(pick_files_dialog)
    return v

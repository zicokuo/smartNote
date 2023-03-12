import uuid
from hashlib import sha256
from typing import Optional

import pydash
from flet_core import Column, TextField, icons, ElevatedButton, ControlEvent

from core.database import db
from core.functions import _, log
from prisma_client import Prisma
from prisma_client.models import User

# 账号输入框
account_input_ctl = TextField(prefix_icon=icons.FAVORITE, hint_text=_("Input your account"))
# 密码输入框
password_input_ctl = TextField(prefix_icon=icons.FAVORITE, hint_text=_("Input your password"))


def login_form_widget():
    """
    登录表单
    @return:
    """
    ctl = Column([
        account_input_ctl,
        password_input_ctl,
        ElevatedButton(_("登录"), on_click=on_login_click)
    ])

    return ctl


async def on_login_click(e: ControlEvent):
    await db.connect()
    account = account_input_ctl.value
    password = password_input_ctl.value

    user: Optional[User] = db.user.find_first(where={'account': account})

    if pydash.is_empty(user):
        # 新注册
        new_user_salt: str = uuid.uuid4().hex
        new_user = db.user.create(data={
            'account' : f"{account}",
            'password': sha256(f'{password}:{new_user_salt}'.encode()).hexdigest(),
            'nickname': f"{account}", 'salt': new_user_salt
        })
        return new_user

    # 验证密码
    if user.password == sha256(f'{password}:{user.salt}'.encode()).hexdigest():
        return user

    # 验证不通过
    log.error(_("用户密码错误"))

import uuid
from hashlib import sha256
from typing import Optional

import pydash
from flet_core import Column, TextField, icons, ElevatedButton, ControlEvent, ButtonStyle

from core.database import db, db_this
from core.functions import _, log
from core.widgets import dynamic_msg_show, StatusEnum
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


@db_this
def on_login_click(e: ControlEvent, db: Prisma):
    account = account_input_ctl.value
    password = password_input_ctl.value

    log.debug(_(f"用户输入account:{account},password:{password}"))

    user: Optional[User] = db.user.find_first(where={'account': account})

    if pydash.is_empty(user):
        # 新注册
        new_user_salt: str = uuid.uuid4().hex
        new_user = db.user.create(data={
            'account': f"{account}",
            'password': sha256(f'{password}:{new_user_salt}'.encode()).hexdigest(),
            'nickname': f"{account}", 'salt': new_user_salt
        })
        dynamic_msg_show(_("创建用户"), f"{new_user.account}")
        return new_user

    # 验证密码
    elif user.password is not None and user.password == sha256(f'{password}:{user.salt}'.encode()).hexdigest():
        dynamic_msg_show(_("用户登录"), f"{user.account}", False)
        e.page.client_storage.set("login_account",user.account)
        e.page.session.set('login_account', user)
        e.page.go("/dashboard")
        return user

    # 验证不通过
    dynamic_msg_show(_("用户登录失败"), _(f"用户{account}密码错误"), True)

from typing import Dict, Optional, Any

import flet
from pydantic import BaseModel, Field

from core.functions import _


class RouteItemVo(BaseModel):
    """
    路由实体
    """
    route: str = Field(title=_("路由路径,以/开头"))
    filename: str = Field(title=_("路由page_view文件路径,以/src/pages/目录下"))


class BootCtxVo(BaseModel):
    """
    全局缓存实体
    """
    ctx:Any = None
    routers: Dict[str, RouteItemVo] = {}

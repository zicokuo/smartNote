# SmartNote
`v 0.1.0`
`MIT`

> 一款采用flet框架进行开发的本地个人笔记桌面应用

## 开发
项目采用了 `Poetry` 作为依赖管理环境进行开发;

```shell
# 安装 poetry
pip install poetry

# 修改poetry 默认配置(仅第一次)
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

# 安装项目依赖
poetry install
```

开发采用HotReload模式进行监听文件变更自动更新
```shell
flet run ./src/main.py -r
```

## 打包
项目采用 pyInstaller 进行打包, 多平台通用
```shell
flet pack ./src/main.py --name SmartNote --add-data "assets;assets" --add-data "src;." 
```
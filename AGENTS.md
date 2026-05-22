# AGENTS.md

## 交流与代码约定

1. 尽量用中文与用户交流。
2. 生成代码时变量名必须用英文。
3. 代码注释使用中文，且只在逻辑不够直观时添加。
4. 用户环境是 Windows 11 + PowerShell 7，当前仓库路径位于 WSL UNC 路径下。
5. 不要在回答末尾额外总结“做了什么”。

## 项目概览

- 这是一个 Python Telegram bot。
- 入口文件是 `main.py`。
- 配置集中在 `config.py`，敏感配置通过环境变量读取。
- 依赖锁定在 `requirements.txt`。
- Docker 运行入口由 `Dockerfile` 和 `docker-compose.yml` 提供。

## 运行相关

- Telegram token 来自 `TG_BOT_TOKEN`。
- PushBullet token 来自 `PUSH_BULLET_TOKEN`。
- PushBullet push URL 来自 `PUSH_BULLET_PUSH_URL`。
- 本地 Windows 环境会在 `config.py` 中自动设置 `127.0.0.1:10808` 代理。
- Linux 环境按生产环境处理，不自动设置代理。

## 工作方式

- 修改前先检查现有文件和未提交变更，避免覆盖用户改动。
- 优先做最小、聚焦的改动。
- 如果需要安装依赖、访问网络或执行可能受沙箱限制的命令，先按工具权限流程请求确认。
- 对 Python 改动，优先使用现有依赖和项目风格；没有测试框架时，不为了小改动引入额外框架。

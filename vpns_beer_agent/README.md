# vpns.beer 代理平台登录自动化

把 vpns.beer 代理后台的登录过程自动化：拿 token、保存会话、给 Playwright / Playwright MCP 复用。凭据与 token 是明文，只在本机使用。

## 目标网站

- 登录页：https://vpns.beer/agent/
- 登录接口：`POST /api/agent/login`，请求体 `{"username": "...", "password": "..."}`，返回体含 `token`
- 登录态：`localStorage` / `sessionStorage` 中的 `covs_agent_session_token`，后续请求用 `Authorization: Bearer <token>`
- 站点不使用 Cookie 做登录态；Cookie 只在会话文件里用来记录新鲜期（脚本自写入，30 天有效）

## 目录

下表路径都相对于本目录（`vpns_beer_agent/`）：

```
scripts/agent_login.py            登录 / 校验 / 保存会话。已保存账号时默认无头自动登录，token 失效自动重新登录
scripts/agent_login_keep.py       只读查看器，用已保存的 token 打开浏览器窗口并保持，可直接操作
scripts/agent_session_helper.py   把脚本转到交互桌面会话（RustDesk 所在）运行；--session 查看会话信息
config/agent_session.json         账号密码 + token + localStorage（明文，已 gitignore）
config/agent_storage_state.json   标准 Playwright storageState，给其它脚本 / Playwright MCP 复用
config/mcp_playwright_config.json Playwright MCP 配置，让 MCP 浏览器自动加载 storageState
```

仓库根的 `temp/` 放临时文件（页面快照、下载内容、窗口日志、`agent_login_triggers.py` 启动钩子），无需清理。

## 用法

在 RustDesk 能看到的桌面（会话 1）里打开 PowerShell 或 CMD：

```powershell
cd C:/Users/Administrator/Documents/Token_Platform

# 打开已登录的浏览器窗口并保持，可直接在上面操作；关掉窗口即退出
python vpns_beer_agent/scripts/agent_login_keep.py

# 只校验已保存的 token 是否还有效（无头）
python vpns_beer_agent/scripts/agent_login.py --check

# 手动重新登录并覆盖保存（会弹出登录窗口）
python vpns_beer_agent/scripts/agent_login.py --save

# 更新保存的密码
python vpns_beer_agent/scripts/agent_login.py --password "新密码"
```

在 Claude Code 的工具进程里执行 `python vpns_beer_agent/scripts/agent_login_keep.py --save` 这类需要弹窗的命令时，脚本会自动转到交互桌面会话再启动，日志写到 `temp/login_window.log`。

依赖：`pip install playwright && python -m playwright install chromium`

## Playwright MCP 自动登录

MCP 服务器启动时加上 `--config vpns_beer_agent/config/mcp_playwright_config.json`，浏览器会带着 storageState 里的 token 打开页面。token 过期时先跑一次 `python vpns_beer_agent/scripts/agent_login.py` 刷新。

## 安全提醒

`config/agent_session.json` 里是明文账号密码和 token，`config/agent_storage_state.json` 里是 token。只在本机使用，不要提交 git、不要发给别人或贴到聊天记录里。2026-10-09 随「Claude 无限卡官网」一起搬到公开备份仓库 `github.com/futianren/claude-unlimited-site` 时，仓库根的 `.gitignore` 已按新路径排除这三个文件；push 前用 `git check-ignore vpns_beer_agent/config/agent_session.json` 再确认一次。

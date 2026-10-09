# aiprimetech.io 全站页面分析

- 站点：https://aiprimetech.io/
- 分析日期：2026-10-08
- 数据来源：sitemap.xml 共 475 个 URL（英文 256 个，多语言版本 219 个），逐页抓取正文并逐页撰写中文摘要
- 产物目录：`temp/aiprimetech_site/`
  - `pages/` 每页正文 Markdown（274 个文件，含中文/日文/俄文/德文抽样）
  - `batches/b1..b8_summary.md` 各板块中文摘要
  - `all_summaries.md` 254 个英文页摘要合集
  - `page_index.txt` 全站标题/描述/字数索引
  - `crawl_site.py` `recrawl_order.py` `make_batches.py` `merge_summaries.py` 抓取与合并脚本

## 站点性质

AI Prime Tech 是一个第三方 API 中转网关（不是 Anthropic 官方），卖点是"一个 Key 打通 Claude、GPT、Gemini、MiniMax"，按 token 计费宣称比官方低最多 87%，另有不限量套餐，支持加密货币与刷卡支付。站点面向开发者，程序化 SEO 特征极强：每个板块都有大量结构高度雷同的中英文/多语言页面（德/西/法/意/日/韩/俄/越/中），内容多为模板套壳加少量场景话术。

## 板块规模

| 板块 | 英文页数 | 高价值页 | 主要内容 |
|---|---|---|---|
| /blog/ | 70 | 45 | Claude Code 用法与新功能、模型发布速报、成本控制、提示注入等 |
| /learn/ | 46 | 21 | 各类客户端接入教程（IDE、CLI、框架）与 Claude API 基础概念 |
| /docs/ | 52 | 28 | API 参考、计费、SDK、迁移与排错 |
| /claude-code/ | 39 | 19 | Claude Code 专站：安装、命令、hooks、MCP、subagents、11 个错误排查页 |
| /models/ | 31 | 多数 | 31 个模型的上下文窗口、定价、选型建议 |
| /tools/ | 4 | 4 | 成本计算器、限流说明、模型选择器 |
| /plans/ + /topup/ | 11 | 1 | 不限量套餐与充值页 |
| 首页 | 1 | 1 | 接入三步、折扣主张、信任背书 |
| 中文页（/claude-code/zh/、/zh/learn/ 等） | 抽样 | — | 与英文版同源的中文内容 |

## 内容质量判断

- 值得读：/blog/ 的 Claude Code 实战与成本控制长文、/claude-code/errors/ 的错误排查页、/docs/guides/ 的 API 最佳实践与上下文管理、/tools/ 的模型选择与限流说明。
- 价值有限：/plans/、/topup/ 各档位页、/models/ 单模型页、多语言翻译页。它们主要由同一模板生成，重复度高。
- 注意事项：所有页面都带本站的推广段落与联盟链接；作者自述文章由 AI 辅助起草，部分版本信息需自行核对官方文档。

## 详细摘要

见 `temp/aiprimetech_site/all_summaries.md`。

## 配套产物：可勾选的页面精选清单

- `docs/claude_code_页面精选清单.html`：87 行页面，按我们写什么分六类：上手与日常 A（5）、原理解释 B（10）、成本控制 C（8）、配置与扩展 D（18）、排错手册 E（17）、速查参考 F（16）、可跳过 S（13）。每行一行：英文原标题（可点击）、中文标记、路径、可切入的文章角度、板块、勾选框、备注框（留空即全篇）。可按主题与中文版筛选，勾选与备注存在浏览器 localStorage，可导出 CSV。编辑部索引风格，暖纸底配墨黑与暗红，跟随系统浅色/深色模式。
- `scripts/build_selection_html.py`：生成该 HTML 的脚本，依赖 `temp/aiprimetech_site/all_summaries.md`。
- `temp/aiprimetech_site/aiprimetech_selection_light.png` / `_dark.png`：浅色与深色预览截图。
- `temp/aiprimetech_site/temp_ui_check.py`：用本机 playwright 对清单做端到端验证（渲染、筛选、勾选、备注持久化、CSV、清空、横向溢出）。

## 关于站点语言切换

首页页脚有语言切换（Deutsch / Español / Français / Italiano / Português / Русский / 日本語 / 한국어 / 中文 / Tiếng Việt），head 里有 12 条 hreflang。中英文对应关系是 `/claude-code/zh/` ↔ `/claude-code/`、`/zh/learn/<slug>/` ↔ `/learn/<slug>/`。`/claude-code/errors/` 与 `/docs/` 没有中文版。

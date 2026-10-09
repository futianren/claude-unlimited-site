# -*- coding: utf-8 -*-
"""生成可勾选、带备注、按写作主题分类排序的单页 HTML：docs/claude_code_页面精选清单.html

设计：编辑部索引卡片风格，暖纸底 + 墨黑 + 暗红；一行一条，可按主题筛选、可勾选、可写备注、可导出 CSV。
分类用于规划"我们要写什么文章"，每行给出可切入的文章角度。
"""
import os, re, json

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp", "aiprimetech_site")
os.chdir(BASE)
S = open("all_summaries.md", encoding="utf-8").read()
secs = {}
for blk in re.split(r"^### ", S, flags=re.M)[1:]:
    lines = blk.rstrip().split("\n")
    url = "/" + lines[0].strip().strip("/") + "/"
    d = {}
    for ln in lines[1:]:
        m = re.match(r"^- ([^:：]+)[：:]\s*(.*)$", ln.strip())
        if m:
            d[m.group(1).strip()] = m.group(2).strip()
    secs[url] = d


def get(u, *keys):
    d = secs.get(u, {})
    for k in keys:
        if k in d:
            return d[k]
    return ""


def zh_mirror(u):
    """站点的中文镜像只在 /zh/learn/ 下有"""
    m = re.match(r"^/learn/([a-z0-9-]+)/$", u)
    return "/zh/learn/%s/" % m.group(1) if m else None


# ---------------- 写作主题分类 ----------------
# key: (编号, 名称, 一句话说明, 颜色序号[0-4])
THEMES = [
    ("A", "上手与日常", "命令、会话、工作流，读者装好就能用", 0),
    ("B", "原理解释", "把黑箱打开：上下文、token、缓存、限流到底怎么回事", 1),
    ("C", "成本控制", "账单从哪来、怎么量、怎么压", 2),
    ("D", "配置与扩展", "hooks、subagents、skills、MCP、模型切换", 3),
    ("E", "排错手册", "按报错信息查，一次一个问题", 4),
]
THEME_MAP = {
    # A 上手与日常
    "/claude-code/tutorial/": ("A", "从安装到计划模式的完整上手"),
    "/claude-code/zh/": ("A", "中文版专站总入口：安装、配置、价格、教程四个子页"),
    "/blog/claude-code-agents-md-support/": ("D", "AGENTS.md 与 CLAUDE.md：多个工具共用一份项目约定"),
    "/claude-code/zh/tutorial/": ("A", "中文版上手流程，可直接改写成中文文章"),
    "/blog/claude-code-auto-mode-vs-dangerously-skip-permissions/": ("A", "什么时候放手让 The 自己跑"),
    "/blog/claude-code-plan-mode/": ("A", "计划模式的适用场景"),
    # B 原理解释
    "/docs/guides/context-management/": ("B", "上下文窗口：N 轮对话为什么是 N² 成本，工具结果为什么是主要元凶"),
    "/blog/claude-code-token-overhead-startup/": ("B", "启动时 33k token 的构成：工具 schema、环境上下文、内置技能"),
    "/learn/claude-code-api-costs/": ("B", "为什么 The 比聊天更烧 token：每轮重发全文"),
    "/learn/how-to-reduce-claude-token-usage/": ("B", "先测量再优化：看到底发了什么"),
    "/blog/agent-cost-control/": ("B", "agent 循环如何让成本非线性增长"),
    "/learn/openai-compatible-claude-api/": ("B", "接口形态：Messages 与 Chat Completions 差在哪"),
    "/learn/anthropic-compatible-api/": ("B", "兼容接口到底兼容了什么，切换前验哪几项"),
    "/learn/use-claude-api-with-langchain/": ("B", "框架怎么把请求送到自定义端点"),
    "/learn/anthropic-python-sdk/": ("B", "官方 SDK 的调用链条"),
    "/learn/use-claude-api-with-vercel-ai-sdk/": ("B", "Vercel AI SDK 的 provider 配置"),
    # C 成本控制
    "/docs/guides/cost-control/": ("C", "输出 token 比输入贵 4 到 5 倍，四个真正有效的杠杆"),
    "/docs/guides/prompt-caching/": ("C", "缓存：稳定前缀以折扣价重读，怎么标记和验证"),
    "/blog/prompt-caching-explained/": ("C", "缓存命中规则与 TTL 的通俗版"),
    "/learn/cheapest-way-to-use-claude-api/": ("C", "降本方法汇总：选模型、缓存、限输出、治理用量"),
    "/learn/claude-api-pricing-explained/": ("C", "按 token 计费的构成与估算方法"),
    "/learn/unlimited-claude-code-usage/": ("C", "不限量与按量付费的切换阈值"),
    "/tools/claude-api-cost-calculator/": ("C", "成本计算器的算法逻辑"),
    "/learn/claude-api-vs-subscription/": ("C", "按量、订阅、不限量三种付费的取舍"),
    # D 配置与扩展
    "/claude-code/hooks/": ("D", "钩子：在工具调用前后插入自己的逻辑"),
    "/claude-code/subagents/": ("D", "子代理：把独立任务分给专门角色"),
    "/claude-code/skills/": ("D", "技能：按触发规则加载的说明书"),
    "/claude-code/mcp/": ("D", "MCP：接外部工具与数据源"),
    "/blog/claude-code-mcp-servers-setup-guide/": ("D", "MCP 服务器实操与权限收紧"),
    "/blog/claude-code-router/": ("D", "让 The 跑在其他模型上"),
    "/blog/claude-code-persistent-memory-across-sessions/": ("D", "跨会话记忆的真实机制"),
    "/blog/everything-claude-code-ecc/": ("D", "第三方增强包 ECC 做了什么"),
    "/blog/gstack-claude-code-setup-guide/": ("D", "gstack 的 23 智能体工作流"),
    "/learn/use-claude-api-with-cline/": ("D", "Cline 接入配置与常见报错"),
    "/learn/use-claude-api-with-roo-code/": ("D", "Roo Code 接入配置"),
    "/learn/use-claude-api-with-aider/": ("D", "Aider 接入与 architect 模式"),
    "/learn/use-claude-api-with-opencode/": ("D", "OpenCode 的 provider 配置"),
    "/learn/use-claude-api-with-codex/": ("D", "codex CLI 自定义 provider"),
    "/learn/use-claude-api-with-github-copilot/": ("D", "Copilot 自定义端点与 agent 模式"),
    "/learn/use-claude-api-with-jetbrains/": ("D", "JetBrains 通过 Continue 接入"),
    "/learn/use-claude-api-with-vscode/": ("D", "VS Code 扩展接入"),
    # E 排错手册
    "/claude-code/errors/usage-limit-reached/": ("E", "各类限额提示各对应哪个计量窗口"),
    "/claude-code/errors/prompt-too-long/": ("E", "上下文超限：窗口被什么填满，先看 /context 再处理"),
    "/claude-code/errors/overloaded-529/": ("E", "529 过载与 429 限流的区别"),
    "/claude-code/errors/api-error-500/": ("E", "服务端 500 的排查路径"),
    "/claude-code/errors/connection-lost/": ("E", "连接中断的原因与恢复"),
    "/claude-code/errors/claude-code-hangs/": ("E", "命令卡住不动时怎么办"),
    "/claude-code/errors/rate-limits/": ("E", "限流分类与退避重试"),
    "/learn/claude-api-errors-troubleshooting/": ("E", "400、429、500、529 四类错误的生产级重试逻辑"),
    # 参考（查阅用，不一定写成文章）
    "/claude-code/errors/auth-401-403/": ("E", "鉴权失败：key 没设、设错或没生效"),
    "/claude-code/errors/claude-ai-not-working/": ("E", "The 服务不可用时怎么判断是自己的问题"),
    "/claude-code/errors/oauth-error/": ("E", "登录态过期与重新登录"),
    "/claude-code/errors/process-exited-code-1/": ("E", "进程异常退出"),
    "/claude-code/errors/api-error-400/": ("E", "400 坏请求的常见触发"),
    "/docs/getting-started/base-urls/": ("E", "各种 SDK 各该填哪个 base URL，404 形态反推错误"),
    "/docs/getting-started/authentication/": ("E", "鉴权方式与密钥管理"),
    "/docs/guides/api-key-configuration/": ("E", "key 配置位置与泄露防范"),
    "/docs/guides/troubleshooting/": ("E", "通用排错流程"),
    # 选型与速查
    "/tools/claude-model-selector/": ("F", "按任务选 Opus、Sonnet 还是 Haiku"),
    "/models/": ("F", "各模型上下文窗口与价格速查"),
    "/learn/claude-api-models-compared/": ("F", "模型家族对比与适用场景"),
    "/blog/claude-code-max-output-tokens/": ("F", "输出上限参数的影响"),
    "/tools/claude-api-rate-limits/": ("F", "RPM、TPM、并发三个维度"),
    "/blog/rate-limits-and-retries/": ("F", "客户端重试与退避实现细节"),
    "/blog/streaming-api-guide/": ("F", "流式响应要点与坑"),
    "/blog/reduce-llm-token-usage/": ("F", "更广义的 token 削减策略"),
    "/blog/claude-code-system-prompt-lessons/": ("F", "从系统提示词提炼的 agent 设计经验"),
    "/docs/api-reference/messages/": ("F", "Messages API 参数参考"),
    "/docs/api-reference/streaming/": ("F", "流式接口参数参考"),
    "/docs/api-reference/tool-use/": ("F", "工具调用参数参考"),
    "/docs/guides/best-practices/": ("F", "可靠、成本、安全、可观测的官方清单"),
    "/docs/guides/claude-code/": ("F", "The 指向自定义端点的两行配置"),
    "/docs/guides/mcp-servers/": ("F", "网关侧 MCP 配置"),
    "/learn/claude-api-vs-anthropic-direct/": ("F", "网关与官方直连的差异"),
}
# 主题 F 没有字母条目名，单独处理
THEME_NAME = {"A": "上手与日常", "B": "原理解释", "C": "成本控制", "D": "配置与扩展", "E": "排错手册", "F": "速查参考", "S": "可跳过"}
THEME_DESC = {k: d for k, _, d, _ in THEMES}
THEME_DESC["F"] = "速查表与参数参考，写文章时按需引用"
THEME_DESC["S"] = "模板化售卖页，只有价格不同"

# 可跳过：售卖与商务页
SKIP = [
 ("/plans/", "不限量套餐总览。"),
 ("/plans/unlimited-claude-api-1-hour/", "一美元一小时档。"),
 ("/plans/unlimited-claude-api-24-hours/", "十美元一天档。"),
 ("/plans/unlimited-claude-api-1-week/", "四十九美元一周档。"),
 ("/plans/unlimited-claude-api-15-days/", "八十九美元十五天档。"),
 ("/topup/", "充值首页。"),
 ("/topup/claude-api-credits-38-usd/", "五美元充值页。"),
 ("/topup/claude-api-credits-76-usd/", "十美元充值页。"),
 ("/topup/claude-api-credits-192-usd/", "二十五美元充值页。"),
 ("/topup/claude-api-credits-384-usd/", "五十美元充值页。"),
 ("/topup/claude-api-credits-769-usd/", "一百美元充值页。"),
 ("/business/", "企业账户介绍。"),
 ("/partner/", "联盟与分销计划。"),
]
# all_summaries.md 里的摘要缺失或不适合展示，手工给标题
FILL_TITLE = {
    "/claude-code/errors/rate-limits/": ("速率限制与重试", "429 限流的退避重试策略"),
    "/claude-code/errors/auth-401-403/": ("鉴权失败 401 / 403", "key 没设、设错或没生效"),
    "/claude-code/errors/claude-ai-not-working/": ("Claude 服务不可用", "怎么判断是自己的问题还是上游的问题"),
    "/claude-code/errors/oauth-error/": ("登录态 OAuth 错误", "登录过期与重新登录"),
    "/claude-code/errors/process-exited-code-1/": ("进程异常退出", "退出码 1 的排查"),
    "/claude-code/errors/api-error-400/": ("API 错误 400", "坏请求的常见触发"),
    "/business/": ("企业账户", "企业版账户介绍与商务条款"),
    "/partner/": ("联盟与分销计划", "推广返佣与经销商规则"),
}
# 中文镜像：站点上的中文版专站入口
ZH_PAGES = {"/claude-code/zh/": "中文版 Claude Fable 5.1 专站：安装、教程、配置与价格四章"}

THEME_ORDER = ["A", "B", "C", "D", "E", "F", "S"]

items = []
for u, (t, angle) in sorted(THEME_MAP.items(), key=lambda kv: (THEME_ORDER.index(kv[1][0]), kv[0])):
    # 摘要里的「标题」是各页 H1 原文（英文），「中文标题」是抓取脚本生成的中译；清单统一用原文，便于我们自己写中文文章时对照
    title = FILL_TITLE[u][0] if u in FILL_TITLE else (get(u, "标题") or ZH_PAGES.get(u, ""))
    zh = zh_mirror(u)
    if zh and not os.path.exists("pages/%s.md" % zh.replace("/", "__").strip("_")):
        zh = None
    slug = u.strip("/").split("/")
    topic = slug[0] if len(slug) > 1 else "首页"
    items.append(dict(theme=t, url=u, title=title, angle=angle, zh=zh or "", topic=topic,
                      key="p%03d" % (len(items) + 1)))
for u, angle in SKIP:
    title = FILL_TITLE[u][0] if u in FILL_TITLE else (get(u, "标题") or angle)
    items.append(dict(theme="S", url=u, title=title, angle=angle, zh="", topic=u.strip("/").split("/")[0],
                      key="p%03d" % (len(items) + 1)))

missing = [i["url"] for i in items if not i["title"]]
print("条目数:", len(items), "缺标题:", missing)
for t in THEME_ORDER:
    print("  主题", t, THEME_NAME[t], sum(1 for i in items if i["theme"] == t), "页")
zh_count = sum(1 for i in items if i["zh"])

data = json.dumps(items, ensure_ascii=False)
tpl = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude Code 页面精选清单 · aiprimetech.io</title>
<style>
:root{
  --paper:#F5F1E8; --paper2:#EFE9DC; --card:#FFFDF8; --ink:#1F1B15; --ink2:#6E6455; --line:#E1D8C6;
  --accent:#7A2E1C; --t-a:#7A2E1C; --t-b:#2F4E6E; --t-c:#6E4C1C; --t-d:#3D5A44; --t-e:#6B2F5E; --t-f:#4A4F57; --t-s:#8A2F2F;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Songti SC","Noto Serif SC",Georgia,serif;
  --sans:"Avenir Next","PingFang SC","Microsoft YaHei",system-ui,sans-serif; --mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){
  :root{--paper:#17150F; --paper2:#1D1A13; --card:#211E16; --ink:#EDE6D6; --ink2:#9B917E; --line:#373226; --accent:#E08A5F;
    --t-a:#E08A5F; --t-b:#8FB4D9; --t-c:#D9B05A; --t-d:#8FBF9F; --t-e:#D9A0CE; --t-f:#AEB3BC; --t-s:#D98F8F}
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);background-image:radial-gradient(rgba(120,90,40,.10) 1px,transparent 1px);background-size:22px 22px;color:var(--ink);font:15px/1.65 var(--sans)}
a{color:var(--accent)}
.wrap{max-width:980px;margin:0 auto;padding:0 20px 80px}
header{padding:44px 0 18px;border-bottom:2px solid var(--ink)}
.kicker{font:600 11px/1 var(--mono);letter-spacing:.28em;text-transform:uppercase;color:var(--accent)}
h1{font:700 clamp(28px,4vw,42px)/1.12 var(--serif);margin:12px 0 8px;letter-spacing:.01em}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:var(--ink2);max-width:62ch}
.meta{margin-top:14px;font:12px var(--mono);color:var(--ink2)}
.razor{margin-top:10px;padding:8px 12px;border:1px dashed var(--line);border-radius:8px;background:color-mix(in srgb,var(--card) 70%,transparent);font-size:12.5px;color:var(--ink2)}
.razor b{color:var(--ink)}
.bar{position:sticky;top:0;z-index:20;display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:10px 0;background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);margin-bottom:22px}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink2);border-radius:999px;padding:4px 11px;font-size:12px;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:5px}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip .dot{width:8px;height:8px;border-radius:2px;background:var(--c,var(--ink2))}
.chip[aria-pressed=true]{background:var(--c,var(--accent));border-color:var(--c,var(--accent));color:#fff}
.chip[aria-pressed=true] .dot{background:#fff}
.spacer{flex:1}
.count{font:12px var(--mono);color:var(--ink2)}
.export{border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:6px;padding:5px 12px;font-size:12px;cursor:pointer;letter-spacing:.05em}
.export.out{background:transparent;color:var(--accent)}
.tier{margin:30px 0 10px;display:flex;align-items:baseline;gap:10px;border-top:1px solid var(--line);padding-top:14px}
.tier .tag{font:700 11px var(--mono);letter-spacing:.2em;color:#fff;background:var(--c);padding:2px 7px;border-radius:3px}
.tier h2{font:700 18px var(--serif);margin:0}
.tier p{margin:0;color:var(--ink2);font-size:13px}
.tier .n{margin-left:auto;font:12px var(--mono);color:var(--ink2);white-space:nowrap}
.row{display:grid;grid-template-columns:24px minmax(0,1fr) 150px;gap:4px 12px;align-items:center;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--c);border-radius:10px;padding:9px 12px;margin-bottom:6px;transition:.15s;animation:rise .4s ease both}
.row:hover{border-color:var(--accent);border-left-color:var(--c);transform:translateY(-1px);box-shadow:0 4px 14px rgba(60,40,10,.08)}
.row.sel{background:color-mix(in srgb,var(--accent) 6%,var(--card));border-color:var(--accent);border-left-color:var(--c)}
@keyframes rise{from{opacity:0;transform:translateY(6px)}}
.check{appearance:none;width:17px;height:17px;border:1.5px solid var(--ink2);border-radius:4px;cursor:pointer;display:grid;place-content:center;transition:.12s}
.check:hover{border-color:var(--accent)}
.check:checked{background:var(--accent);border-color:var(--accent)}
.check:checked::after{content:"✓";color:#fff;font-size:11px;font-weight:700}
.t1line{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;line-height:1.4}
.title{font:600 15.5px/1.4 var(--serif)}
.title a{text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
.title a:hover{border-bottom-color:var(--accent)}
.num{font:11px var(--mono);color:var(--ink2)}
.path{font:12px var(--mono);color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.line2{display:flex;align-items:center;gap:8px;margin-top:2px;min-width:0}
.blurb{font-size:13.5px;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1 1 auto;min-width:0}
.badge{font:10.5px var(--mono);letter-spacing:.06em;border:1px solid var(--line);border-radius:4px;padding:0 5px;color:var(--ink2);white-space:nowrap;flex:none}
.badge.zh{border-color:var(--t-d);color:var(--t-d);text-decoration:none;position:relative;top:-5px}
.badge.zh:hover{background:var(--t-d);color:var(--paper)}
.noteBox{display:flex;flex-direction:column;gap:3px;min-width:0}
.noteBox label{font:10.5px var(--mono);letter-spacing:.1em;color:var(--ink2)}
.noteBox textarea{width:100%;height:40px;resize:vertical;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink);padding:4px 6px;font:12px/1.4 var(--sans)}
.noteBox textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 15%,transparent)}
.hide{display:none!important}
footer{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--ink2);font-size:12.5px}
.toast{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:var(--ink);color:var(--paper);padding:8px 16px;border-radius:999px;font-size:13px;opacity:0;pointer-events:none;transition:.25s}
.toast.on{opacity:1;bottom:22px}
@media(max-width:760px){.row{grid-template-columns:24px 1fr;align-items:start}.noteBox{grid-column:2}.line2{flex-wrap:wrap}.blurb{white-space:normal}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="kicker">aiprimetech.io · 页面索引 · 2026-10-08 抓取</div>
  <h1>Claude Code 页面<em>精选清单</em></h1>
  <div class="sub">从 475 个 URL 里挑出 <b id="total"></b> 个页面，按"我们要写什么文章"分成六类：上手与日常、原理解释、成本控制、配置与扩展、排错手册、速查参考。每行给出可切入的文章角度。勾选你想精读的行，写下只要哪一段，留空即整篇。</div>
  <div class="razor"><b>分类思路</b> · A 到 E 是按读者目的分的五个内容区：先学会用，再看懂原理，再省钱，再扩展，最后兜底排错。F 是写文章时的速查材料，不必单独成文。原理类（B）与成本类（C）最值得写成系列：前者解释"为什么"，后者给出"怎么做"。</div>
  <div class="meta" id="meta"></div>
</header>

<div class="bar" id="bar">
  <button class="chip" data-filter="all" aria-pressed="true">全部</button>
  <button class="chip" data-filter="zh" aria-pressed="false"><span class="dot" style="--c:var(--t-d)"></span>仅中文版</button>
  <span class="spacer"></span>
  <span class="count" id="cnt"></span>
  <button class="export" id="expSel">导出已勾选 CSV</button>
  <button class="export out" id="expAll">导出全部</button>
  <button class="export out" id="clear">清空</button>
</div>

<div id="rows"></div>

<footer>
  内容说明：所有页面均为第三方 API 网关站 aiprimetech.io 的内容，每页末尾带该站推广段落；作者自述文章由 AI 辅助起草，版本信息请对照官方文档核对。中文版路径规则：<span style="font-family:var(--mono)">/claude-code/zh/</span> 与 <span style="font-family:var(--mono)">/zh/learn/&lt;slug&gt;/</span>。
</footer>
</div>
<div class="toast" id="toast"></div>

<script>
const DATA = __DATA__;
const KEY = "aiprimetech.selection.v3";
const $ = s => document.querySelector(s);
const esc = s => (s||"").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { state = {}; }
let filter = "all";
const T = {A:["A","上手与日常","命令、会话、工作流，读者装好就能用"],B:["B","原理解释","把黑箱打开：上下文、token、缓存、限流到底怎么回事"],C:["C","成本控制","账单从哪来、怎么量、怎么压"],D:["D","配置与扩展","hooks、subagents、skills、MCP、模型切换"],E:["E","排错手册","按报错信息查，一次一个问题"],F:["F","速查参考","速查表与参数参考，写文章时按需引用"],S:["S","可跳过","模板化售卖页，只有价格不同"]};
const ORDER = ["A","B","C","D","E","F","S"];
$("#total").textContent = DATA.length;
$("#meta").textContent = "共 " + DATA.length + " 行 · " + DATA.filter(x=>x.zh).length + " 行有现成中文版 · /claude-code/errors/ 与 /docs/ 无中文版";
document.querySelector(".bar .chip[data-filter=all]").insertAdjacentHTML("afterend", ORDER.map(t => '<button class="chip" data-filter="'+t+'" aria-pressed="false"><span class="dot" style="--c:var(--t-'+t.toLowerCase()+')"></span>'+T[t][1]+'</button>').join(""));

$("#rows").innerHTML = ORDER.map(t => {
  const head = '<div class="tier" data-theme="'+t+'" style="--c:var(--t-'+t.toLowerCase()+')"><span class="tag">'+t+'</span><h2>'+T[t][1]+'</h2><p>'+T[t][2]+'</p><span class="n"></span></div>';
  const rows = DATA.map((it, idx) => { if (it.theme !== t) return "";
    const zh = it.zh ? '<a class="badge zh" href="https://aiprimetech.io'+it.zh+'" target="_blank" rel="noopener">中文</a>' : '';
    return '<div class="row" data-theme="'+t+'" data-key="'+it.key+'" style="--c:var(--t-'+t.toLowerCase()+');animation-delay:'+Math.min(idx,40)*12+'ms">'
      + '<input type="checkbox" class="check" id="'+it.key+'_c" aria-label="选择 '+esc(it.url)+'">'
      + '<div><div class="t1line"><a class="title" href="https://aiprimetech.io'+it.url+'" target="_blank" rel="noopener">'+esc(it.title||it.url)+'</a>'
      + zh + '<span class="path">'+esc(it.url)+'</span><span class="num">'+String(idx+1).padStart(2,'0')+'</span></div>'
      + '<div class="line2"><span class="blurb">'+esc(it.angle)+'</span><span class="badge">'+esc(it.topic)+'</span></div></div>'
      + '<div class="noteBox"><label for="'+it.key+'_n">备注 · 留空即全篇</label><textarea id="'+it.key+'_n" placeholder="例如：只看第 3 节"></textarea></div>'
      + '</div>';
  }).join("");
  return head + rows;
}).join("");

function save(){ localStorage.setItem(KEY, JSON.stringify(state)); }
function applyFilter(){
  let shown = 0; const themes = {};
  document.querySelectorAll(".row").forEach(r => {
    const it = DATA.find(x => x.key === r.dataset.key);
    const ok = filter === "all" ? true : filter === "zh" ? !!it.zh : r.dataset.theme === filter;
    r.classList.toggle("hide", !ok); if (ok) shown++;
    if (ok) themes[r.dataset.theme] = (themes[r.dataset.theme]||0) + 1;
  });
  document.querySelectorAll(".tier").forEach(t => { const n = t.querySelector(".n"); if (n) n.textContent = (themes[t.dataset.theme]||0) + " 页"; t.classList.toggle("hide", !themes[t.dataset.theme]); });
  let sel = 0; for (const it of DATA) if (state[it.key] && state[it.key].checked) sel++;
  $("#cnt").textContent = "显示 " + shown + " / " + DATA.length + " 行 · 已勾选 " + sel;
}
function sync(){
  for (const it of DATA){
    const s = state[it.key] || {};
    const c = $("#"+it.key+"_c"), t = $("#"+it.key+"_n");
    if (c.checked !== !!s.checked) c.checked = !!s.checked;
    if (t.value !== (s.note||"")) t.value = s.note || "";
    c.closest(".row").classList.toggle("sel", !!s.checked);
  }
  applyFilter();
}
document.addEventListener("change", e => { if (e.target.classList.contains("check")){ const k = e.target.closest(".row").dataset.key; state[k] = Object.assign(state[k]||{}, {checked:e.target.checked}); save(); sync(); }});
document.addEventListener("input", e => { if (e.target.tagName === "TEXTAREA"){ const k = e.target.closest(".row").dataset.key; state[k] = Object.assign(state[k]||{}, {note:e.target.value}); save(); }});
document.querySelectorAll(".chip[data-filter]").forEach(b => b.onclick = () => { filter = b.dataset.filter; document.querySelectorAll(".chip[data-filter]").forEach(x => x.setAttribute("aria-pressed", x === b)); applyFilter(); });
$("#clear").onclick = () => { if (confirm("清空所有勾选与备注？")){ state = {}; save(); sync(); toast("已清空"); } };
function toast(m){ const t = $("#toast"); t.textContent = m; t.classList.add("on"); setTimeout(() => t.classList.remove("on"), 1600); }
function csv(only){
  const rows = [["序号","主题","标题","页面地址","中文镜像","可切入的文章角度","板块","勾选","备注"]];
  DATA.forEach((it, i) => { const s = state[it.key]||{}; if (only && !s.checked) return;
    rows.push([i+1, T[it.theme][1], it.title, "https://aiprimetech.io"+it.url, it.zh?"https://aiprimetech.io"+it.zh:"", it.angle, it.topic, s.checked?"是":"", s.note||""]); });
  const text = "﻿" + rows.map(r => r.map(v => '"'+String(v).replace(/"/g,'""')+'"').join(",")).join("\r\n");
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], {type:"text/csv;charset=utf-8"}));
  a.download = "claude_code_页面清单" + (only ? "_已勾选" : "_全部") + ".csv"; a.click(); toast(only ? "已导出已勾选行" : "已导出全部行");
}
$("#expSel").onclick = () => csv(true);
$("#expAll").onclick = () => csv(false);
sync();
</script>
</body>
</html>
'''
# 正式输出到项目 docs/；temp/aiprimetech_site/docs/ 只是同一份副本
docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
os.makedirs(docs_dir, exist_ok=True)
os.makedirs(os.path.join(BASE, "docs"), exist_ok=True)
html = tpl.replace("__DATA__", data).replace("ZHCOUNT", str(zh_count))
open(os.path.join(docs_dir, "claude_code_页面精选清单.html"), "w", encoding="utf-8").write(html)
open(os.path.join(BASE, "docs", "claude_code_页面精选清单.html"), "w", encoding="utf-8").write(html)
print("written:", os.path.join(docs_dir, "claude_code_页面精选清单.html"), os.path.getsize(os.path.join(docs_dir, "claude_code_页面精选清单.html")), "bytes; 含中文镜像:", zh_count)
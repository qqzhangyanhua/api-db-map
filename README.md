# api-db-map

从后端代码里追踪「接口查了哪些表、改了哪些表、字段怎么关联」，再画出架构图、字段关系图和时序图。

> Trace backend APIs to the tables and fields they read or write, then render architecture, field-relation, and sequence diagrams.

这是一个 **Agent Skill**（显式调用）：只有你直接说出 `api-db-map` / 「用 api-db-map」时，Agent 才会跑这套流程。提到表、接口或 schema 不会自动触发。

## 安装

不发 npm。把仓库推到公开 GitHub 后，用 [Skills CLI](https://github.com/vercel-labs/skills) 安装：

```bash
npx skills add qqzhangyanhua/api-db-map
```

```bash
# 装到本机全局（所有项目都能用）
npx skills add qqzhangyanhua/api-db-map -g -y

# 只装到 Cursor
npx skills add qqzhangyanhua/api-db-map -a cursor -g -y

# 更新已安装版本
npx skills update api-db-map
```

也可以手工拷到 Agent 的 skills 目录：

- Cursor：`~/.cursor/skills/api-db-map/` 或项目内 `.cursor/skills/api-db-map/`
- Claude Code：`~/.claude/skills/api-db-map/` 或项目内 `.claude/skills/api-db-map/`

## 能回答什么

带着证据回答，不编造表名、字段或外键：

- 深追的每个 HTTP 接口读了哪些表、写了哪些表
- 读/写落到了哪些字段
- 表之间的关联来自 FK、JOIN，还是代码里推断出来的
- 哪些访问证据不足，需要人看一眼

## 产出

默认写到目标仓库的 `./api-db-map-out/`（也可指定路径）。多次分析会增量追加，不覆盖历史结果。

```
api-db-map-out/
├── index.html                          ← 入口：按路径 / 表名搜索
├── registry.json                       ← 全局索引
├── GET__api__orders__-id-/
│   ├── 2026-09-13.html                 ← 该接口的三视图
│   ├── 2026-09-13.json
│   └── 2026-09-13.md
├── POST__api__orders/
│   └── 2026-09-13.html
└── _project_overview/                  ← 深追多个接口时额外生成
    └── 2026-09-13.html
```

目录名：`METHOD` + 路径，`/` → `__`，`{id}` → `-id-`。同一接口同一天再分析，文件名追加时分（`2026-09-13T14-30.html`）。

入口页 `index.html` 支持按路径关键词、表名搜索，按 HTTP 方法 / uncertain / 最近一周筛选。卡片跳到该接口最新 HTML，可切换历史版本。

HTML 必须用 `scripts/render_html.py` 生成，不要手写。渲染时会自动更新 `registry.json` 和 `index.html`。

三张图：

- **T·01 影响架构图** — 左边接口，右边表，箭头标 SQL 动词（虚线读、实线写）
- **T·02 表与字段关系** — 表卡片带字段，边从 FK 字段连到被引用 PK
- **T·03 接口时序图** — Client → Controller → Service → 表，消息带方法和列

## 怎么用

装好之后，在目标后端仓库里对 Agent 说：

```text
用 api-db-map 分析这个项目
```

可选范围：

- 单个路由：`GET /api/orders/{id}`
- 某个模块 / 包
- 一份 OpenAPI / Swagger
- 只读的线上库 URL（仅做 schema 对照，禁止写库）

没给过滤条件时，先清单全部接口，再深追最多 12 个（写操作优先），其余列入未追踪，汇报时问要不要扩。

## 支持的栈

检测脚本会先认框架和 ORM，再只加载对应 playbook：

| 语言 | 框架 | ORM / 访问层 |
|------|------|----------------|
| Java | Spring | JPA、MyBatis / MyBatis-Plus |
| Python | FastAPI、Django | SQLAlchemy、SQLModel、Django ORM |
| TypeScript / JS | Nest、Express / Fastify / Koa | Prisma、TypeORM、Drizzle、Sequelize |
| Go | Gin | GORM |

任意栈都会额外扫裸 SQL / mapper XML。识别不准时会先问一句框架 + ORM，再按文件名和 SQL 字符串继续，而不是卡住。

Schema 来源按可信度取第一份能给出表、列、主键的结果：线上库（只读）→ migrations / DDL → ORM 模型 → SQL 字符串推断。缺外键或字段注释时继续往后补。

## 本地脚本

Python 3（命令用 `python3`，别用 `python`），无强制第三方依赖。装了 `sqlglot` 解析复杂 SQL 更准，没装则退化到正则，脚本自报的 `confidence` 不会给到 `high`。

脚本要按 skill 自己所在的目录调用，不是被分析的项目目录：

```bash
cd /path/to/api-db-map        # 或用绝对路径，见 SKILL.md「Running the scripts」

# 识别语言 / 框架 / ORM
python3 scripts/detect_stack.py /path/to/backend

# 从 SQL 字符串或 MyBatis XML 抽出表、操作、字段
python3 scripts/extract_sql.py --file mapper/OrderMapper.xml
python3 scripts/extract_sql.py --sql "SELECT id, status FROM orders WHERE id = 1"

# 把 IR 渲染成 HTML（默认用仓库里的样例数据）
python3 scripts/render_html.py assets/sample-ir.json -o /tmp/api-db-map.html --no-index

# 从 registry.json 重建入口页
python3 scripts/render_index.py api-db-map-out/

# 冒烟测试：渲染样例 IR 并检查产物结构
python3 scripts/smoke_test.py
```

想先看看图长什么样，用上面第三条命令渲染 `assets/sample-ir.json` 然后打开产物即可。

## 目录

```
api-db-map/
├── SKILL.md                      # Agent 工作流（范围 → 抽 schema → 追接口 → 渲染）
├── scripts/
│   ├── detect_stack.py
│   ├── extract_sql.py
│   ├── render_html.py
│   ├── render_index.py           # registry → index.html
│   └── smoke_test.py             # 渲染冒烟测试
├── references/
│   ├── ir-schema.md              # api-db-map.json 结构
│   ├── stack-patterns.md         # 各栈抽取配方
│   ├── raw-sql.md                # 裸 SQL / 动态 SQL
│   └── visualization.md          # 三视图视觉规范
└── assets/
    ├── diagram.template.html     # 三视图模板
    ├── index.template.html       # 入口页模板
    └── sample-ir.json            # 样例 IR，配合 render_html.py 预览
```

## 原则

- 代码证明不了的访问标成 `uncertain`，继续往下做，不猜表名
- 每条表访问都带 `file:line` 证据
- 线上库只允许 `SELECT` 级 schema 探查，禁止 INSERT / UPDATE / DELETE / DDL
- 拼接 SQL、MyBatis `${table}`、反射、动态数据源一律 `uncertain`
- 默认可深追 12 个接口；点名模块或路由则只做范围内；未追踪的 id 写进 coverage，再问要不要扩

## 许可

[MIT](LICENSE)

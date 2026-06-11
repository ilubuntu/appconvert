# iOS 到 HarmonyOS NEXT 多 Agent 迁移工作流

## 设计目标

迁移链路较长，不能依赖一个对话上下文从头记到尾。工作流采用"agent 身份配置 + agent runner（如 opencode run / codex exec 等工具）阶段执行 + 本地文件交接"的方式。

核心目标：

- 降低单个 agent 的上下文压力。
- 每个阶段只读取必要输入，不重复读取全工程。
- 阶段之间通过明确文件交接，而不是通过对话记忆交接。
- 每个阶段有进入条件、输出产物和验收门禁。
- 全量迁移，不按 V1/V2 切范围。
- iOS 分析必须达到工程、模块、文件、类型、函数级，输出结构化 JSON specs。
- 平台能力适配必须基于 JSON specs 和参考库输出可执行的适配策略、实现指导和风险清单。
- Harmony 生成必须按模块拆给多个子 agent，不能由一个 agent 写出单页壳工程。
- 汇总 agent 必须按 `functions.json` 反查 Harmony 覆盖情况，目标是总体工程接近 iOS 1:1 复制。

## 总体结构

用户入口：

```text
通过 ios-to-harmony-workflow 执行 <iOS工程目录> 的 iOS 工程转换，输出到 <Harmony工程目录>
```

内部结构：

```text
workflow runner
  ├─ agent runner: iOS工程分析
  ├─ agent runner: 平台能力适配
  ├─ agent runner: Harmony模块实现计划
  ├─ agent runner: Harmony核心服务实现
  ├─ agent runner: Harmony页面UI实现
  ├─ agent runner: Harmony平台能力实现
  ├─ agent runner: Harmony集成汇总
  └─ agent runner: Harmony视觉验收
```

## Skill 与 Agent 的关系

- agent 配置定义阶段身份，agent runner 是执行单元。
- skill 是操作手册，约束某类 agent 怎么做。
- `ios-to-harmony-workflow` 是面向用户的总入口。
- runner 不直接承担所有细节，只负责编排、检查文件、推进阶段。
- 每个阶段执行只接收必要文件路径、目标和输出契约。
- 具体 agent 定义、调用模板和读写边界见 `agent设计.md`。

对应关系：

| 阶段 | 使用 Skill | 主要职责 |
| --- | --- | --- |
| 迁移总控 runner | `ios-to-harmony-workflow` | 编排阶段、维护状态、检查门禁 |
| iOS工程分析阶段 | `ios-analyze` | 分析 iOS 工程、截图、输出 JSON specs |
| 平台能力适配阶段 | `platform-adaptation` | 基于 JSON specs 和参考库输出适配策略、实现指导和风险 |
| Harmony模块实现计划阶段 | `harmony-generate` | 初始化 Harmony 工程骨架 + 根据 iOS JSON specs 和平台适配产物拆分 Harmony 模块任务 |
| Harmony核心服务阶段 | `harmony-generate` | 实现 models/services/stores 和真实数据链路 |
| Harmony页面UI阶段 | `harmony-generate` | 按 iOS 截图实现 ArkUI 页面和组件 |
| Harmony平台能力阶段 | `harmony-generate` | 按 implementation-guidance.json 实现平台适配层 |
| Harmony集成汇总阶段 | `harmony-generate` | 汇总模块实现，按 functions.json 补齐缺口 |
| Harmony视觉验收阶段 | `build-harmony-project`、`harmonyos-live-preview` | 构建、截图、对比、修复 |

## 上下文控制规则

### 默认不传完整上下文

每个阶段通过 agent runner 从 prompt 文件启动，不继承当前聊天上下文。

只传递：

- 工作目录。
- 必要输入文件路径。
- 具体目标。
- 必须输出的文件。
- 不允许做的事。

这样可以避免把整个聊天历史、源码分析、截图说明全部带入下一阶段。

### 什么时候才使用会话内子 agent

只有在以下情况下才考虑会话内子 agent：

- 子任务很短。
- 子任务强依赖当前对话刚刚产生的细节。
- 不希望重新整理输入文件。

对于 iOS 到 HarmonyOS NEXT 迁移这种长链路任务，默认用 runner + agent runner。

## 文件交接契约

所有阶段都通过本地文件交接，不通过自然语言上下文交接。

### 全局状态文件

`output/workflow/迁移状态.md`

用途：

- 当前阶段。
- 已完成阶段。
- 待完成阶段。
- 阻塞项。
- 最近一次构建/截图/验收结果。
- 下一步建议。

示例：

```md
# 迁移状态

当前阶段：平台能力适配

已完成：
- iOS工程分析（specs/*.json）

待完成：
- 平台能力适配
- Harmony 模块实现计划
- Harmony 核心服务
- Harmony 页面 UI
- Harmony 平台能力
- Harmony 集成汇总
- Harmony 视觉验收

阻塞：
- 无

下一步：
- 运行 platform-adaptation skill，生成适配策略和实现指导。
```

### iOS 工程分析阶段输出

输入：

- `NewsMobile/`
- iOS 模拟器和构建环境

输出：

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `output/ios-analyze/reports/ios工程分析.md`
- `output/ios-analyze/reports/ios功能摘要.md`
- `output/ios-analyze/reports/ios界面摘要.md`
- `output/ios-analyze/assets/`（资源归档）
- `output/ios-analyze/screenshots/png/`（如采集截图）

门禁：

- iOS 工程可以构建或至少能解释构建阻塞。
- 每个 Swift 文件都进入 `specs/project.json` 或 `specs/functions.json`。
- 每个 feature 有稳定 id、三级结构、source_refs、acceptance。
- JSON 之间能通过稳定 id 相互引用。
- 核心功能截图齐全（如采集）。
- 模块结构必须包含模块职责、对外接口和依赖关系。

### 平台能力适配阶段输出

输入：

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `skills/platform-adaptation/references/platform-capabilities.json`

输出：

- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `output/platform-adaptation/reports/平台能力适配摘要.md`

门禁：

- `capabilities.json` 中每个能力都出现在 `capability-coverage.json` 的 items 或 unmapped。
- 每个 high/medium priority feature 有关联 capability 时出现在 `feature-adaptation.json`。
- `implementation-guidance.json` 包含目标文件边界和 public API 草案。
- 每条风险有 `recommended_action`。
- 不做基础 UI 控件映射。

### Harmony 模块实现计划阶段输出

输入：

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/screens.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `skills/harmony-generate/references/project-template/`

输出：

- `NewsMobileHarmony/`（工程骨架，如果不存在）
- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`

门禁：

- 每个 iOS 模块都有 Harmony 目录或替代层。
- 每个 iOS 类型/函数都有迁移动作：独立实现、合并、替代、删除并说明原因。
- 后续子 agent 任务清晰拆分到核心服务、页面 UI、平台能力、集成汇总。

### Harmony 核心服务阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.json`
- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/platform-adaptation/implementation-guidance.json`

输出：

- `NewsMobileHarmony/entry/src/main/ets/models/`
- `NewsMobileHarmony/entry/src/main/ets/services/`
- `NewsMobileHarmony/entry/src/main/ets/stores/`
- `output/harmony-generate/harmony全量实现追踪.md`

门禁：

- 新闻、搜索、收藏、设置、订阅源、趋势、聚类、TTS/Web/通知/定位/后台/卡片/本地 API 相关数据接口都有模型或服务。
- 每个 Harmony 文件能追溯到 iOS 文件、类型和函数。
- 真实数据优先，fixture 只做兜底。

### Harmony 页面 UI 阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/screenshots/png/`
- `output/harmony-generate/harmony全量实现追踪.md`

输出：

- `NewsMobileHarmony/entry/src/main/ets/pages/`
- `NewsMobileHarmony/entry/src/main/ets/components/`
- `output/harmony-generate/harmony全量实现追踪.md`

门禁：

- 主 Tab、首页、详情、搜索、收藏、设置等页面有实质内容、状态和交互。
- 页面以 iOS 截图为主要约束，争取信息层级、字号、颜色、卡片、间距、圆角、顶部导航、底部 Tab 高度一致。
- 不能只实现简单框架 UI。

### Harmony 平台能力阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `output/harmony-generate/harmony全量实现追踪.md`

输出：

- `NewsMobileHarmony/entry/src/main/ets/platform/`
- `NewsMobileHarmony/entry/src/main/module.json5`
- `output/harmony-generate/harmony全量实现追踪.md`

门禁：

- Web、TTS、通知、定位、后台刷新、Widget/Card、云同步、本地 API、网络权限、持久化等能力有工程侧实现或适配入口。
- 需要外部配置的能力必须记录配置项，但不能因此不实现工程入口。
- 按 `implementation-guidance.json` 的 `platform_modules` 实现。

### Harmony 集成汇总阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/screens.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/implementation-guidance.json`

输出：

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/workflow/迁移状态.md`

门禁：

- Harmony 工程能构建，或失败原因明确。
- 每个 iOS 类型/函数都有 Harmony 去向。
- 每个 Harmony 模块能追溯到 `specs/modules.json`。
- 每个页面能追溯到 `specs/features.json` 和 `specs/screens.json`。
- 每个系统能力能追溯到 `platform-adaptation/capability-coverage.json`。
- 首屏不能空白，必须有 fixture 兜底数据。

### Harmony 视觉验收阶段输出

输入：

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/screenshots/png/`

输出：

- 构建结果。
- Harmony 截图。
- iOS/Harmony 页面差异记录。
- 修复后的工程。
- 更新后的 `output/harmony-generate/harmony全量实现追踪.md` 和 `output/workflow/迁移状态.md`。

门禁：

- HAP 构建成功。
- 主 Tab、首页、详情、搜索、收藏、设置可用。
- Web、TTS、通知、定位、卡片、云同步、后台刷新、本地 API、NLP 均有实现、入口或配套适配层。
- 关键页面可和 iOS 截图对齐说明。

## Runner 编排规则

workflow runner 只做以下事情：

1. 检查当前阶段和 `output/workflow/迁移状态.md`。
2. 检查本阶段输入文件是否存在。
3. 渲染阶段 prompt。
4. 通过 agent runner 启动阶段执行。
5. 检查输出是否满足门禁。
6. 更新 `output/workflow/迁移状态.md`。
7. 推进下一阶段或报告阻塞。

workflow runner 不应该：

- 反复读取整个 iOS 工程。
- 在多个阶段重复做同一份分析。
- 把完整聊天上下文传给阶段执行进程。
- 用自然语言总结替代文件产物。

## 阶段 Prompt 模板

### iOS 工程分析阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 ios-analyze skill 分析 NewsMobile iOS 工程。

必须读取：
- NewsMobile/

必须输出：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- output/ios-analyze/reports/ios工程分析.md
- output/ios-analyze/reports/ios功能摘要.md
- output/ios-analyze/reports/ios界面摘要.md

约束：
- 不生成 Harmony 工程。
- 不做平台能力适配。
- 必须按 ios-analyze skill 的内部编排流程执行。
- features.json 是核心产物，必须按三级功能结构组织。
- JSON 之间必须通过稳定 id 互相引用。
- 截图不能人工点击。
- 必须逐文件读取 Swift 源码，不能只用 README 或扫描结果总结。
```

### 平台能力适配阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 platform-adaptation skill 生成平台能力适配策略。

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- skills/platform-adaptation/references/platform-capabilities.json

必须输出：
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/feature-adaptation.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json
- output/platform-adaptation/reports/平台能力适配摘要.md

约束：
- 不生成 Harmony 工程。
- 不做基础 UI 控件映射。
- capabilities.json 中每个能力都必须进入 capability-coverage.json 的 items 或 unmapped。
- high/medium priority feature 有关联 capability 时必须进入 feature-adaptation.json。
- implementation-guidance.json 是后续 Harmony 代码生成的主输入，必须包含目标文件边界和 public API 草案。
- risks.json 每条风险必须有 recommended_action。
```

### Harmony 模块实现计划阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 harmony-generate skill 初始化 Harmony 工程并生成模块实现计划。

第一步：工程初始化
如果 NewsMobileHarmony/ 不存在：
1. 从 skills/harmony-generate/references/project-template/ 复制模板到 NewsMobileHarmony/。
2. 替换占位符（bundleName、vendor、app_name）。
3. 创建迁移目录（models/services/stores/pages/components/platform/cards/fixtures/support）。
4. 删除 oh-package-lock.json5。

第二步：生成计划
必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json

必须输出：
- output/harmony-generate/harmony模块实现计划.json
- output/harmony-generate/harmony全量实现追踪.md

约束：
- 本阶段只做工程初始化和计划，不写业务代码。
- 每个 iOS 类型/函数都必须有 Harmony 处置。
- 必须拆出后续子 agent 任务：核心服务、页面 UI、系统能力、集成汇总。
```

### Harmony 子模块实现阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
按 output/harmony-generate/harmony模块实现计划.json 分别执行核心服务、页面 UI、平台能力、集成汇总阶段。

必须读取：
- output/harmony-generate/harmony模块实现计划.json
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json

必须输出：
- NewsMobileHarmony/
- output/harmony-generate/harmony全量实现追踪.md
- output/workflow/迁移状态.md

约束：
- 每个 Harmony 文件必须追溯到 iOS 文件、类型和函数。
- 不能只实现简单 UI 框架。
- 每个子阶段都必须构建验证或明确失败原因。
```

### Harmony 视觉验收阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
构建 NewsMobileHarmony，对照 iOS 截图和实现追踪表验收并修复问题。

必须读取：
- NewsMobileHarmony/
- output/harmony-generate/harmony全量实现追踪.md
- output/ios-analyze/specs/screens.json
- output/ios-analyze/screenshots/png/

必须输出：
- 构建结果
- 修复说明
- 更新后的 output/harmony-generate/harmony全量实现追踪.md
- 更新后的 output/workflow/迁移状态.md

约束：
- 不扩大迁移范围。
- 不删除配套服务能力入口。
- 构建失败必须给出具体错误和下一步。
```

## 推荐执行顺序

1. 创建或更新 `output/workflow/迁移状态.md`。
2. runner 检查是否已有 iOS 分析产物。
3. 缺 iOS 分析产物时，执行 iOS 工程分析阶段。
4. iOS 分析通过门禁后，执行平台能力适配阶段。
5. 适配通过门禁后，执行 Harmony 模块实现计划阶段。
6. 计划通过门禁后，依次执行核心服务、页面 UI、平台能力阶段。
7. 模块阶段完成后，执行 Harmony 集成汇总阶段。
8. Harmony 构建通过后，执行 Harmony 视觉验收阶段。
9. 每阶段完成后更新 `output/workflow/迁移状态.md`。

## 当前 NewsMobile 状态

已完成：

- `output/ios-analyze/specs/*.json`（7 个 JSON specs）
- `output/ios-analyze/scan/*.json`（扫描中间产物）
- `output/ios-analyze/reports/*.md`（3 个人工摘要）
- `output/ios-analyze/assets/`（资源归档）

当前建议阶段：

- 运行平台能力适配阶段，生成 `output/platform-adaptation/*.json`。
- 然后执行 Harmony 模块实现计划阶段，基于 JSON specs 和平台适配产物拆分 Harmony 模块任务。

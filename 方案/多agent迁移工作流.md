# iOS 到 HarmonyOS NEXT 多 Agent 迁移工作流

## 设计目标

迁移链路较长，不能依赖一个对话上下文从头记到尾。工作流采用“agent 身份配置 + `codex exec` 阶段执行 + 本地文件交接”的方式。

核心目标：

- 降低单个 agent 的上下文压力。
- 每个阶段只读取必要输入，不重复读取全工程。
- 阶段之间通过明确文件交接，而不是通过对话记忆交接。
- 每个阶段有进入条件、输出产物和验收门禁。
- 全量迁移，不按 V1/V2 切范围。
- iOS 分析必须达到工程、模块、文件、类型、函数级，不能只产出粗略功能描述。
- Harmony 生成必须按模块拆给多个子 agent，不能由一个 agent 写出单页壳工程。
- 汇总 agent 必须按 iOS 函数级清单反查 Harmony 覆盖情况，目标是总体工程接近 iOS 1:1 复制。

## 总体结构

用户入口：

```text
通过 ios-to-harmony-workflow 执行 <iOS工程目录> 的 iOS 工程转换，输出到 <Harmony工程目录>
```

内部结构：

```text
workflow runner
  ├─ codex exec: iOS工程分析
  ├─ codex exec: iOS能力映射
  ├─ codex exec: Harmony模块实现计划
  ├─ codex exec: Harmony核心服务实现
  ├─ codex exec: Harmony页面UI实现
  ├─ codex exec: Harmony平台能力实现
  ├─ codex exec: Harmony集成汇总
  └─ codex exec: Harmony视觉验收
```

## Skill 与 Agent 的关系

- agent 配置定义阶段身份，`codex exec` 是执行单元。
- skill 是操作手册，约束某类 agent 怎么做。
- `ios-to-harmony-workflow` 是面向用户的总入口。
- runner 不直接承担所有细节，只负责编排、检查文件、推进阶段。
- 每个 `codex exec` 阶段只接收必要文件路径、目标和输出契约。
- 具体 agent 定义、调用模板和读写边界见 `agent设计.md`。

对应关系：

| 阶段 | 使用 Skill | 主要职责 |
| --- | --- | --- |
| 迁移总控 runner | `ios-to-harmony-workflow` | 编排阶段、维护状态、检查门禁 |
| iOS工程分析阶段 | `ios-analyze` | 分析 iOS 工程、截图、输出 iOS 规格 |
| iOS能力映射阶段 | `ios-map` | 将 iOS 能力映射到 HarmonyOS NEXT |
| Harmony模块实现计划阶段 | `harmony-generate` | 根据 iOS 模块/函数清单拆分 Harmony 模块任务 |
| Harmony核心服务阶段 | `harmony-generate` | 实现 models/services/stores 和真实数据链路 |
| Harmony页面UI阶段 | `harmony-generate` | 按 iOS 截图实现 ArkUI 页面和组件 |
| Harmony平台能力阶段 | `harmony-generate` | 实现 Web/TTS/通知/定位/后台/卡片/云同步/本地 API 等适配 |
| Harmony集成汇总阶段 | `harmony-generate` | 汇总模块实现，按 iOS 函数级清单补齐缺口 |
| Harmony视觉验收阶段 | `build-harmony-project`、`harmonyos-live-preview` | 构建、截图、对比、修复 |

## 上下文控制规则

### 默认不传完整上下文

每个阶段通过 `codex exec` 从 prompt 文件启动，不继承当前聊天上下文。

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

对于 iOS 到 HarmonyOS NEXT 迁移这种长链路任务，默认用 runner + `codex exec`。

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

当前阶段：Harmony工程生成

已完成：
- iOS模块结构
- iOS功能清单
- iOS界面截图
- iOS能力映射

待完成：
- 拆分 Harmony models/services/pages
- 接入 RSS
- 接入 Preferences
- 接入 Web/TTS/Notification/Location
- 接入卡片/云同步/后台刷新/本地 API/NLP

阻塞：
- 无

下一步：
- 调用 Harmony工程生成 agent，读取 output/ios-analyze/ios模块结构.md 和 output/ios-map/ios-harmony-kit映射.md 拆分工程结构。
```

### iOS 工程分析阶段输出

输入：

- `NewsMobile/`
- iOS 模拟器和构建环境

输出：

- `output/ios-analyze/ios源码索引.md`
- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios函数级清单.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-analyze/ios特性清单.md`
- `output/ios-analyze/ios模块结构.draft.md`
- `output/ios-analyze/screenshots/png/*.png`
- `output/ios-analyze/screenshots/png/screenshots-manifest.json`

门禁：

- iOS 工程可以构建或至少能解释构建阻塞。
- 每个 Swift 文件都进入 `output/ios-analyze/ios源码索引.md`。
- 每个类型、关键属性、函数、`body`、异步任务、回调、delegate、extension 都进入 `output/ios-analyze/ios函数级清单.md`。
- 每个功能都能追溯到具体文件、类型、函数和截图。
- 截图不能依赖人工点击。
- 主要页面截图齐全。
- 模块结构必须包含模块职责、对外接口和依赖关系。

### iOS 能力映射阶段输出

输入：

- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios特性清单.md`

输出：

- `output/ios-map/ios-harmony-kit映射.md`

门禁：

- 每个 iOS 能力都有 HarmonyOS NEXT 落点。
- 每项能力标记为 `平台直迁`、`等价替代` 或 `配套服务`。
- 不能把能力标记为不做或排除出当前迁移目标。

### Harmony 模块实现计划阶段输出

输入：

- `output/ios-analyze/ios源码索引.md`
- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios函数级清单.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-map/ios-harmony-kit映射.md`
- `output/ios-analyze/screenshots/png/`

输出：

- `output/harmony-generate/harmony模块实现计划.md`
- `output/harmony-generate/harmony全量实现追踪.md`

门禁：

- 每个 iOS 模块都有 Harmony 目录或替代层。
- 每个 iOS 类型/函数都有迁移动作：独立实现、合并、替代、删除并说明原因。
- 后续子 agent 任务清晰拆分到核心服务、页面 UI、平台能力、集成汇总。

### Harmony 核心服务阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.md`
- `output/ios-analyze/ios源码索引.md`
- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios函数级清单.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-map/ios-harmony-kit映射.md`

输出：

- `NewsMobileHarmony/entry/src/main/ets/models/`
- `NewsMobileHarmony/entry/src/main/ets/services/`
- `NewsMobileHarmony/entry/src/main/ets/stores/`
- `output/harmony-generate/harmony全量实现追踪.md`
- 构建产物或构建失败日志

门禁：

- 新闻、搜索、收藏、设置、订阅源、趋势、聚类、TTS/Web/通知/定位/后台/卡片/本地 API 相关数据接口都有模型或服务。
- 每个 Harmony 文件能追溯到 iOS 文件、类型和函数。
- 真实数据优先，固定样例数据 只做兜底。
- Harmony 工程能构建，或失败原因明确。

### Harmony 页面 UI 阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/screenshots/png/`
- `output/harmony-generate/harmony全量实现追踪.md`

输出：

- `NewsMobileHarmony/entry/src/main/ets/pages/`
- `NewsMobileHarmony/entry/src/main/ets/components/`
- `output/harmony-generate/harmony全量实现追踪.md`
- 构建产物或构建失败日志

门禁：

- 主 Tab、首页、详情、搜索、收藏、设置等页面有实质内容、状态和交互。
- 页面以 iOS 截图为主要约束，争取信息层级、字号、颜色、卡片、间距、圆角、顶部导航、底部 Tab 高度一致。
- 不能只实现简单框架 UI。
- Harmony 工程能构建，或失败原因明确。

### Harmony 平台能力阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.md`
- `output/ios-analyze/ios特性清单.md`
- `output/ios-map/ios-harmony-kit映射.md`
- `output/harmony-generate/harmony全量实现追踪.md`

输出：

- `NewsMobileHarmony/entry/src/main/ets/platform/`
- `NewsMobileHarmony/entry/src/main/module.json5`
- `output/harmony-generate/harmony全量实现追踪.md`
- 构建产物或构建失败日志

门禁：

- Web、TTS、通知、定位、后台刷新、Widget/Card、云同步、本地 API、网络权限、持久化等能力有工程侧实现或适配入口。
- 需要外部配置的能力必须记录配置项，但不能因此不实现工程入口。
- Harmony 工程能构建，或失败原因明确。

### Harmony 集成汇总阶段输出

输入：

- `output/harmony-generate/harmony模块实现计划.md`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/ios源码索引.md`
- `output/ios-analyze/ios函数级清单.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-map/ios-harmony-kit映射.md`

输出：

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/workflow/迁移状态.md`
- 构建产物或构建失败日志

门禁：

- Harmony 工程能构建，或失败原因明确。
- 每个 iOS 类型/函数都有 Harmony 去向。
- 每个 Harmony 模块能追溯到 `output/ios-analyze/ios模块结构.md`。
- 每个页面能追溯到 `output/ios-analyze/ios功能清单.md` 和 `output/ios-analyze/ios界面清单.md`。
- 每个系统能力能追溯到 `output/ios-map/ios-harmony-kit映射.md`。
- 首屏不能空白，必须有 固定样例数据兜底数据。

### Harmony 视觉验收阶段输出

输入：

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/ios界面清单.md`
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
4. 调用 `codex exec`。
5. 检查输出是否满足门禁。
6. 更新 `output/workflow/迁移状态.md`。
7. 推进下一阶段或报告阻塞。

workflow runner 不应该：

- 反复读取整个 iOS 工程。
- 在多个阶段重复做同一份分析。
- 把完整聊天上下文传给阶段执行进程。
- 用自然语言总结替代文件产物。

## `codex exec` 阶段 Prompt 模板

### iOS 工程分析阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 ios-analyze skill 分析 NewsMobile iOS 工程。

必须读取：
- NewsMobile/

必须输出：
- output/ios-analyze/ios源码索引.md
- output/ios-analyze/ios模块结构.md
- output/ios-analyze/ios函数级清单.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/ios界面清单.md
- output/ios-analyze/ios特性清单.md
- output/ios-analyze/screenshots/png/screenshots-manifest.json

约束：
- 不生成 Harmony 工程。
- 不做 iOS 到 Harmony Kit 映射。
- 截图不能人工点击。
- 必须按 工程 -> Target/模块 -> 文件 -> 类型 -> 函数/属性 的颗粒度分析。
```

### iOS 能力映射阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 ios-map skill 生成 iOS 到 HarmonyOS NEXT 能力映射。

必须读取：
- output/ios-analyze/ios模块结构.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/ios特性清单.md

必须输出：
- output/ios-map/ios-harmony-kit映射.md

约束：
- 不读取完整 iOS 源码，除非文档证据不足。
- 不生成 Harmony 工程。
- 所有能力都进入迁移目标。
```

### Harmony 模块实现计划阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 harmony-generate skill 为 NewsMobileHarmony 生成模块实现计划。

必须读取：
- output/ios-analyze/ios源码索引.md
- output/ios-analyze/ios模块结构.md
- output/ios-analyze/ios函数级清单.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/ios界面清单.md
- output/ios-map/ios-harmony-kit映射.md
- output/ios-analyze/screenshots/png/

必须输出：
- output/harmony-generate/harmony模块实现计划.md
- output/harmony-generate/harmony全量实现追踪.md

约束：
- 本阶段只做计划和追踪表初始化，不大规模改 Harmony 代码。
- 每个 iOS 类型/函数都必须有 Harmony 处置。
```

### Harmony 子模块实现阶段

```text
工作目录：/Users/bb/work/appConvert

任务：
按 output/harmony-generate/harmony模块实现计划.md 分别执行核心服务、页面 UI、平台能力、集成汇总阶段。

必须读取：
- output/harmony-generate/harmony模块实现计划.md
- output/ios-analyze/ios源码索引.md
- output/ios-analyze/ios函数级清单.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/ios界面清单.md
- output/ios-map/ios-harmony-kit映射.md

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
- output/ios-analyze/ios界面清单.md
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
4. iOS 分析通过门禁后，执行 iOS 能力映射阶段。
5. 映射通过门禁后，执行 Harmony 模块实现计划阶段。
6. 计划通过门禁后，依次执行核心服务、页面 UI、平台能力阶段。
7. 模块阶段完成后，执行 Harmony 集成汇总阶段。
8. Harmony 构建通过后，执行 Harmony 视觉验收阶段。
9. 每阶段完成后更新 `output/workflow/迁移状态.md`。

## 当前 NewsMobile 状态

已完成：

- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-analyze/ios特性清单.md`
- `output/ios-map/ios-harmony-kit映射.md`
- `output/ios-analyze/screenshots/png/*.png`
- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`

当前建议阶段：

- 回到 iOS 工程分析阶段，补齐 `output/ios-analyze/ios源码索引.md` 和 `output/ios-analyze/ios函数级清单.md`。
- 再执行 Harmony 模块实现计划阶段，把当前集中在 `Index.ets` 的实现拆为正式模块：`models/`、`services/`、`stores/`、`platform/`、`components/`、`pages/`、`cards/`。

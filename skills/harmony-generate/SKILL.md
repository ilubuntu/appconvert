---
name: harmony-generate
description: 当 iOS 工程分析和 iOS 到 HarmonyOS NEXT 能力映射完成后使用。本 skill 负责根据迁移规格生成或修改 HarmonyOS NEXT ArkTS/ArkUI 工程，实现页面和服务，接入存储、网络和系统能力，并验证构建。它不重新从头理解 iOS 原工程。
---

# HarmonyOS NEXT 工程辅助生成

## 职责边界

输入：

- `output/01-ios-analyze/ios功能清单.md`
- `output/01-ios-analyze/ios模块结构.md`
- `output/01-ios-analyze/ios源码索引.md`
- `output/01-ios-analyze/ios函数级清单.md`
- `output/01-ios-analyze/ios界面清单.md`
- `output/02-ios-map/ios-harmony-kit映射.md`
- 截图产物

输出：

- HarmonyOS NEXT 工程或工程改动
- ArkTS 数据模型、服务和页面
- 真实数据加载链路和 fixture 兜底
- 参照 iOS 截图实现的高保真 ArkUI 页面
- 构建/测试结果摘要
- 全量实现追踪表和外部配套要求

除非规格不完整或互相矛盾，否则不要回到 iOS 工程重新作为主要信息源。

## 工作流

1. 读取已分析完成的 iOS 规格、源码索引、函数级清单、模块结构和能力映射。
2. 生成模块实现计划，按 iOS 模块拆分 Harmony models/services/stores/pages/components/platform。
3. 逐模块实现 ArkTS 模型和服务，每个文件必须追溯到 iOS 类型或函数。
4. 接入真实数据源，新闻流真实数据优先，fixture 只做网络失败、解析失败或截图稳定性兜底。
5. 按 `output/01-ios-analyze/ios界面清单.md` 和截图实现 ArkUI 页面，不允许只实现信息不完整的框架 UI。
6. 按 `output/02-ios-map/ios-harmony-kit映射.md` 接入平台能力或工程侧适配层。
7. 生成集成追踪表，明确每个 iOS 类型/函数的 Harmony 去向。
8. 使用本地 HarmonyOS 工具链构建，并用精确文件和命令报告失败。

## 实现规则

- 每个页面必须能追溯到 `output/01-ios-analyze/ios功能清单.md`。
- 每个 Harmony 模块必须能追溯到 `output/01-ios-analyze/ios模块结构.md`。
- 每个 Harmony 文件必须能追溯到 `output/01-ios-analyze/ios源码索引.md`。
- 每个核心函数必须能追溯到 `output/01-ios-analyze/ios函数级清单.md`。
- 每个系统能力必须能追溯到 `output/02-ios-map/ios-harmony-kit映射.md`。
- 每个 UI 决策必须能追溯到 `output/01-ios-analyze/ios界面清单.md` 或截图产物。
- 真实数据接入属于本 skill 的职责，不能留给单独后置阶段。
- 不允许只写 mock、fixture 或 `example.com` 假数据来冒充迁移完成。
- RSS/Atom 网络请求和 XML 解析必须有可运行链路；fixture 只能兜底。
- 页面实现必须以 iOS 截图为视觉基准，争取高度还原。
- 必须复刻或合理替代顶栏、底部 Tab、卡片、分类 chip、设置列表、空态、详情页操作区等主要 UI。
- 如果 ArkUI 原生控件无法和 iOS 截图一致，优先使用自定义 ArkUI 组件复刻。
- 如果必须采用 HarmonyOS 设计替代，必须记录替代原因、替代组件和保留的交互语义。
- 不按版本切范围；规格里的功能都进入迁移目标。
- 对需要云服务、卡片、后台策略或系统权限的能力，先实现工程侧入口和接口，再记录外部配套要求。
- 优先写简单、可构建、但不能低保真的 ArkTS，不做过度抽象。

## 多 Agent 分工规则

当通过 workflow runner 执行时，本 skill 可以被多个生成阶段复用，但每个阶段只能负责自己的模块范围：

| 子阶段 | 主要输出 | 禁止事项 |
| --- | --- | --- |
| 模块计划 | `output/03-harmony-generate/harmony模块实现计划.md` | 不写大段业务代码 |
| 核心服务 | `models/`、`services/`、`stores/` | 不改页面视觉 |
| 页面 UI | `pages/`、`components/` | 不重新设计数据模型 |
| 系统能力 | `platform/`、权限、卡片、后台、TTS、Web、本地 API | 不删减功能 |
| 集成汇总 | 构建、追踪表、缺口修复 | 不跳过未映射函数 |

每个子阶段都要更新 `output/03-harmony-generate/harmony全量实现追踪.md`，新增或修改的每一项至少包含：

```md
| iOS 文件 | iOS 类型/函数 | Harmony 文件 | Harmony 类型/函数 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- |
```

状态只能使用：

- `已实现`
- `等价替代`
- `工程侧入口已实现，需外部配置`
- `待修复`

不能使用“后续再做”“暂不实现”“不适用”来规避迁移。

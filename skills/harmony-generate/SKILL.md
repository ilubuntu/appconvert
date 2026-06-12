---
name: harmony-generate
description: 当 iOS 工程分析和平台能力适配完成后使用。本 skill 负责根据迁移规格生成或修改 HarmonyOS NEXT ArkTS/ArkUI 工程，实现页面和服务，接入存储、网络和系统能力，并验证构建。它不重新从头理解 iOS 原工程。
---

# HarmonyOS NEXT 工程辅助生成

## 职责边界

输入：

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- 截图产物

输出：

- HarmonyOS NEXT 工程或工程改动
- ArkTS 数据模型、服务和页面
- 真实数据加载链路和 fixture 兜底
- 参照 iOS 截图实现的高保真 ArkUI 页面
- 构建/测试结果摘要
- 全量实现追踪表和外部配套要求

除非规格不完整或互相矛盾，否则不要回到 iOS 工程重新作为主要信息源。

## 工程模板

### 模板位置

```
skills/harmony-generate/references/project-template/
```

### 工程初始化

1. 复制 `references/project-template/` 到目标 Harmony 工程目录，替换占位符（bundleName、vendor、应用名称等）。
2. 工程目录结构由模型根据 iOS 分析产物自行组织，不硬编码。
3. 必须同步维护：每新增 page 更新 `main_pages.json`，按平台能力需求更新 `module.json5`（权限、extensionAbilities 等）。

### module.json5 扩展规则

迁移过程中需要扩展 `module.json5`：

- 新增页面 → 更新 `pages` 字段指向 `$profile:main_pages`（已默认），然后在 `main_pages.json` 添加路由。
- 新增权限 → 在 `module` 下添加 `requestPermissions` 数组。
- 新增后台任务 → 在 `module` 下添加 `extensionAbilities`。
- 新增卡片 → 在 `module` 下添加 `extensionAbilities`（type: "form"）。

### 关键配置文件说明

**`build-profile.json5`（根级）**：
- `signingConfigs`：签名配置，迁移阶段可留空。
- `targetSdkVersion` / `compatibleSdkVersion`：SDK 版本，当前模板为 `"6.0.2(22)"`。
- `products`：构建产物配置。
- `modules`：注册的模块列表，默认只有 `entry`。

**`entry/build-profile.json5`**：
- `apiType: "stageMode"`：Stage 模型（必须）。
- `obfuscation`：混淆开关，默认关闭。

**`entry/src/main/module.json5`**：
- `abilities`：主 Ability 声明（入口页面、图标、label）。
- `extensionAbilities`：备份、卡片等扩展能力。
- `requestPermissions`：运行时权限声明（网络、定位、通知等）。

## 工作流

1. 读取已分析完成的 iOS JSON specs 和平台适配产物。
2. 在 **模块实现计划阶段** 执行工程初始化：如果目标 Harmony 工程不存在，从 `project-template/` 复制模板、替换占位符（bundleName、vendor、app_name）、创建迁移目录（models/services/stores/pages/components/platform/cards/fixtures/support）。
3. 生成模块实现计划（JSON），按 iOS 模块拆分 Harmony models/services/stores/pages/components/platform，每个 iOS 类型/函数映射到 Harmony 文件和迁移动作。
4. 逐模块实现 ArkTS 模型和服务，每个文件必须追溯到 iOS 类型或函数。
5. 接入真实数据源，新闻流真实数据优先，fixture 只做网络失败、解析失败或截图稳定性兜底。
6. 按 `specs/screens.json` 和截图实现 ArkUI 页面，不允许只实现信息不完整的框架 UI。
7. 按 `implementation-guidance.json` 的 `platform_modules` 接入平台能力适配层。
8. 生成集成追踪表，明确每个 iOS 类型/函数的 Harmony 去向。
9. 使用本地 HarmonyOS 工具链构建，并用精确文件和命令报告失败。

### 阶段与职责映射

| 阶段 | 按模块 | 职责 |
|---|---|---|
| 模块计划 | — | 从模板创建工程 + 生成 JSON 计划 + 初始化追踪表 |
| 基础层 | models + stores | 所有数据模型 + PersistenceStore |
| 新闻核心 | services/news + services/rss + services/search + services/weather + pages + components | 新闻浏览全链路 |
| 搜索收藏 | pages/Search + pages/Saved | 搜索页 + 收藏页 |
| ML/分析 | services/nlp + services/ai + services/personalization + pages/ForYou + pages/StoryCluster | 情绪分析 + 聚类 + 趋势 + 个性化推荐 |
| 设置模块 | pages/Settings + pages/KeywordAlerts + pages/CustomFeeds + pages/LocalNews + pages/LocationPicker | 所有设置和配置页面 |
| 平台能力 | platform/* + cards + services/audio/background/notification/sync/localapi + pages/AudioBriefing + module.json5 | 所有平台适配层 + 卡片 + 音频播报 |
| 集成构建 | SnapshotSupport + main_pages.json + 缺口修复 | 入口组装 + 路由注册 + 全量检查 + 构建 |

## 实现规则

### 强制：ArkTS 严格模式编码规范

HarmonyOS NEXT 的 ArkTS 使用严格模式，以下 TypeScript/JavaScript 语法**禁止使用**，违反会导致编译失败：

1. **禁止 `any`、`unknown` 类型** — 必须用具体类型。
2. **禁止对象展开 `{...obj}`** — 必须逐字段赋值或写 helper 函数。
3. **禁止解构声明 `const {a, b} = obj`** — 必须逐个赋值。
4. **禁止索引访问 `obj[key]`** — 必须用具体字段名或 `Map`。
5. **禁止对象字面量作类型声明 `Array<{...}>`** — 必须先声明 `interface`，再用 `Array<InterfaceName>`。
6. **禁止无类型对象字面量** — 必须用 `as Type` 或声明 interface。
7. **禁止函数隐式返回类型** — 必须显式标注 `: ReturnType`。
8. **装饰器必须用 V2 版本** — `@ComponentV2`（不是 `@Component`）、`@ObservedV2`（不是 `@Observed`）、`@Trace`（不是 `@Prop`/`@Link`）、`@Local`（组件内部状态）、`@Param`（父传子）、`@Provider`/`@Consumer`（跨层级共享）、`@Event`（子传父回调）。
9. **Store 必须用 `@ObservedV2 + @Trace`** — 这是 SwiftUI `ObservableObject + @Published` 的等价机制。Store 用普通 class 会导致异步数据到达后 UI 永远不刷新。
10. **页面组件用 `@Local` 持有 Store** — Store 属性变化自动触发 build() 重新渲染。
11. **不允许 barrel export（index.ets）** — ArkTS 不支持，必须直接 import 具体文件路径。
12. **RegExp 是独立类型** — 不能赋值给 `string` 变量。

### 强制：按功能清单全量实现

`specs/features.json` 中的每一个 feature 都必须实现，不允许跳过、标记"后续再做"或降级为占位符。实现追踪表中每个 feature 的状态只能是 `已实现` 或 `等价替代`，不能出现 `暂不实现`、`不在范围内`、`占位` 等规避状态。

实现顺序和完整性检查：
1. 读取 `specs/features.json`，列出全部 feature（一级功能→二级功能→三级功能点）。
2. 每个三级功能点必须有对应的 Harmony 文件和代码。
3. 对照 `specs/functions.json`，每个 iOS 函数都有 Harmony 等价实现。
4. 对照 `specs/screens.json`，每个页面都有 ArkUI 实现。
5. 对照 `capability-coverage.json`，每个平台能力都有适配层入口。
6. 缺口必须在集成汇总阶段补齐，不能以"总结"代替实现。

### 追溯规则

### 追溯规则

- 每个页面必须能追溯到 `specs/features.json` 中的 feature。
- 每个 Harmony 模块必须能追溯到 `specs/modules.json` 中的模块。
- 每个 Harmony 文件必须能追溯到 `specs/functions.json` 中的 iOS 函数。
- 每个系统能力必须能追溯到 `capability-coverage.json` 中的能力。
- 每个 UI 决策必须能追溯到 `specs/screens.json` 或截图产物。
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
| 模块计划 | Harmony 工程初始化 + `harmony模块实现计划.json` + `harmony全量实现追踪.md` | 不写业务代码 |
| 基础层 | `models/`、`stores/` | 不写页面和 UI |
| 新闻核心 | `services/news/`、`services/rss/`、`services/search/`、`services/weather/`、`pages/HomePage`、`pages/ArticleDetailPage`、`pages/ArticleWebPage`、`pages/MainPage`、`components/` | 不写设置页、ML、平台适配 |
| 搜索收藏 | `pages/SearchPage`、`pages/SavedPage` | 不重新实现搜索/收藏服务（依赖基础层和新闻核心） |
| ML/分析 | `services/nlp/`、`services/ai/`、`services/personalization/`、`pages/ForYouPage`、`pages/StoryClusterPage` | 不依赖 NLP Kit（用启发式） |
| 设置模块 | `pages/SettingsPage`、`pages/KeywordAlertsPage`、`pages/CustomFeedsPage`、`pages/LocalNewsPage`、`pages/LocationPickerPage` | 不重新设计数据模型 |
| 平台能力 | `platform/`、`cards/`、`services/audio/`、`services/background/`、`services/notification/`、`services/sync/`、`services/localapi/`、`pages/AudioBriefingPage`、`module.json5` | 不删减功能 |
| 集成构建 | `SnapshotSupport`、`main_pages.json`、缺口修复、构建验证 | 不跳过未映射函数 |

每个子阶段都要更新 `output/harmony-generate/harmony全量实现追踪.md`，新增或修改的每一项至少包含：

```md
| iOS 文件 | iOS 类型/函数 | Harmony 文件 | Harmony 类型/函数 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- |
```

状态只能使用：

- `已实现`
- `等价替代`
- `工程侧入口已实现，需外部配置`
- `待修复`

不能使用"后续再做""暂不实现""不适用"来规避迁移。

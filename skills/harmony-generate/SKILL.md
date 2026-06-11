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

### 模板结构

基于标准 HarmonyOS NEXT 空工程（DevEco Studio 生成），结构如下：

```text
project-template/
├── .gitignore
├── AppScope/
│   ├── app.json5                          # 应用包名、版本、图标、名称
│   └── resources/base/
│       ├── element/string.json            # app_name
│       └── media/                         # background.png, foreground.png, layered_image.json
├── build-profile.json5                    # 全局构建配置（SDK 版本、签名、模块注册）
├── hvigorfile.ts                          # 根级 hvigor 入口
├── hvigor/hvigor-config.json5             # hvigor 构建工具配置
├── oh-package.json5                       # 根级依赖
├── oh-package-lock.json5                  # 依赖锁定
└── entry/
    ├── .gitignore
    ├── build-profile.json5                # entry 模块构建配置
    ├── hvigorfile.ts                      # entry hvigor 入口
    ├── obfuscation-rules.txt              # 混淆规则
    ├── oh-package.json5                   # entry 依赖
    └── src/main/
        ├── module.json5                   # 模块声明（abilities、pages、权限）
        ├── ets/
        │   ├── common/LayoutPolicy.ets    # 响应式布局策略
        │   ├── entryability/EntryAbility.ets      # 主 Ability 生命周期
        │   ├── entrybackupability/EntryBackupAbility.ets  # 备份扩展
        │   └── pages/Index.ets           # 首页
        └── resources/
            ├── base/
            │   ├── element/{color,float,string}.json
            │   ├── media/{background,foreground,startIcon}.png, layered_image.json
            │   └── profile/{main_pages.json, backup_config.json}
            └── dark/element/color.json
```

### 从模板创建工程的步骤

1. 复制 `project-template/` 整个目录到目标 Harmony 工程目录。
2. 替换以下占位符：

| 文件 | 原始值 | 替换为 |
|---|---|---|
| `AppScope/app.json5` | `bundleName: "com.example.empty_hos_project"` | 目标包名，如 `com.example.newsmobile` |
| `AppScope/app.json5` | `vendor: "example"` | 实际 vendor |
| `AppScope/resources/base/element/string.json` | `value: "empty_hos_project"` | 应用显示名 |
| `entry/src/main/resources/base/element/string.json` | `EntryAbility_label` / `EntryAbility_desc` | 对应实际值 |

3. 在 `entry/src/main/ets/` 下创建迁移目录：

```text
ets/
├── models/          # 数据模型（对应 iOS Models/）
├── services/        # 业务服务（对应 iOS Services/）
├── stores/          # 状态管理 + 持久化
├── pages/           # 页面（对应 iOS Views/）—— 模板已有 Index.ets
├── components/      # 可复用 UI 组件
├── platform/        # 平台适配层（按 implementation-guidance.json 的 platform_modules）
├── cards/           # 卡片/Widget
├── fixtures/        # fixture 兜底数据
├── common/          # 通用工具（模板已有 LayoutPolicy.ets）
├── entryability/    # Ability（模板已有）
├── entrybackupability/ # 备份（模板已有）
└── support/         # 辅助工具
```

4. 按迁移计划逐目录生成 `.ets` 文件。
5. 每新增一个 page，同步更新 `entry/src/main/resources/base/profile/main_pages.json`。
6. 按平台能力需求更新 `entry/src/main/module.json5`（添加权限、extensionAbilities 等）。

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

| 阶段 | 是否初始化工程 | 职责 |
|---|---|---|
| 模块计划 | **是**（如果工程不存在） | 从模板创建工程 + 生成 JSON 计划 + 初始化追踪表 |
| 核心服务 | 否 | 实现 models/services/stores |
| 页面 UI | 否 | 实现 pages/components |
| 系统能力 | 否 | 实现 platform/ + 更新 module.json5 |
| 集成汇总 | 否 | 补缺口 + 构建 |

## 实现规则

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
| 核心服务 | `models/`、`services/`、`stores/` | 不改页面视觉 |
| 页面 UI | `pages/`、`components/` | 不重新设计数据模型 |
| 系统能力 | `platform/`、权限、卡片、后台、TTS、Web、本地 API | 不删减功能 |
| 集成汇总 | 构建、追踪表、缺口修复 | 不跳过未映射函数 |

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

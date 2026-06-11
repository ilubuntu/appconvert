---
name: ios-to-harmony-workflow
description: 当用户希望把某个 iOS Swift/SwiftUI/UIKit 工程转换为 HarmonyOS NEXT 工程时使用。该 skill 是面向用户的总入口，负责读取输入目录、维护迁移状态、按阶段调用 iOS 工程分析、平台能力适配、Harmony 工程生成和视觉验收能力；用户不需要直接创建或管理 agent。
---

# iOS 到 HarmonyOS NEXT 迁移工作流

## 用户入口

用户应该用一句话触发完整工作流：

```text
通过 ios-to-harmony-workflow 执行 <iOS工程目录> 的 iOS 工程转换，输出到 <Harmony工程目录>
```

示例：

```text
通过 ios-to-harmony-workflow 执行 /Users/bb/work/appConvert/NewsMobile 的 iOS 工程转换，输出到 /Users/bb/work/appConvert/NewsMobileHarmony
```

用户不需要说"创建 agent""启动子 agent"。agent 配置只是身份定义，实际启动由 workflow runner 完成。

## 输入

- iOS 工程目录，例如 `NewsMobile/`
- HarmonyOS NEXT 输出目录，例如 `NewsMobileHarmony/`
- 可选：是否允许修改 iOS 工程以增加截图模式
- 可选：是否只生成规格，不生成 Harmony 工程

## 输出

必须输出或更新：

- `output/workflow/迁移状态.md`
- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/harmony-visual-verify/界面对齐.md`
- HarmonyOS NEXT 工程目录
- 构建验证结果

## 执行阶段

### 1. 状态检查

读取或创建 `output/workflow/迁移状态.md`。

检查已有产物：

- iOS 分析 JSON specs 是否存在。
- iOS 截图是否存在。
- 平台能力适配产物是否存在。
- Harmony 工程是否存在。
- 最近一次构建是否通过。

### 2. iOS 工程分析

使用 `ios-analyze` skill。

产物：

- `output/ios-analyze/specs/*.json`（7 个 JSON 规格）
- `output/ios-analyze/reports/*.md`（3 个报告）
- `output/ios-analyze/screenshots/png/`

### 3. 平台能力适配

使用 `platform-adaptation` skill。

产物：

- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`

### 4. Harmony 工程生成

使用 `harmony-generate` skill。

产物：

- HarmonyOS NEXT 工程目录
- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`

要求：

- 工程初始化：从模板创建工程骨架、替换占位符、创建迁移目录。
- 每个 Harmony 模块追溯到 `output/ios-analyze/specs/modules.json`。
- 每个页面追溯到 `output/ios-analyze/specs/features.json` 和 `output/ios-analyze/specs/screens.json`。
- 每个系统能力追溯到 `output/platform-adaptation/implementation-guidance.json`。
- 真实数据接入在本阶段完成，新闻流真实数据优先，固定样例数据 只做兜底。
- UI 以 iOS 截图为视觉基准，顶栏、Tab、卡片、字号、颜色、间距、状态都要争取高度还原。

### 5. 视觉验收和构建

使用 `harmony-visual-verify` skill 和 `build-harmony-project` skill。

需要时使用 `harmonyos-live-preview` skill 做 UI 预览和截图。

要求：

- 读取 `output/ios-analyze/specs/screens.json` 和 iOS 截图、Harmony 截图逐页对比。
- 输出 `output/harmony-visual-verify/界面对齐.md`。
- 差异明显时修复 ArkUI 实现。
- 构建 HAP。
- 更新 `output/workflow/迁移状态.md`。
- 更新 `output/harmony-generate/harmony全量实现追踪.md`。
- 如果失败，记录具体错误和下一步。

## 内部执行策略

工作流优先使用外部 runner 串联多个阶段。

默认规则：

- 用户不直接管理 agent。
- `[agents.*]` 只定义身份，不负责启动。
- 每个阶段只读取本阶段需要的本地文件。
- 阶段之间通过文件交接，不通过对话记忆交接。

## 用户可见行为

用户只关心最终结果：

- Harmony 工程是否生成。
- 是否构建通过。
- 哪些功能已实现。
- 哪些外部配套还需要配置。
- 产物在哪里。

回答时不要要求用户理解或操作 agent。

## 推荐最终回复格式

```text
已完成 <iOS工程目录> 到 <Harmony工程目录> 的转换。

关键产物：
- ...

构建结果：
- ...

仍需外部配置：
- ...
```

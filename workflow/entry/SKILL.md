---
name: ios-to-harmony-workflow
description: 当用户希望把某个 iOS Swift/SwiftUI/UIKit 工程转换为 HarmonyOS NEXT 工程时使用。该 skill 是面向用户的总入口，负责读取输入目录、维护迁移状态、按阶段调用 iOS 工程分析、iOS 能力映射、Harmony 工程生成和视觉验收能力；用户不需要直接创建或管理 agent。
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

用户不需要说“创建 agent”“启动子 agent”。agent 配置只是身份定义，实际启动由 workflow runner 或 `codex exec` 完成。

## 输入

- iOS 工程目录，例如 `NewsMobile/`
- HarmonyOS NEXT 输出目录，例如 `NewsMobileHarmony/`
- 可选：是否允许修改 iOS 工程以增加截图模式
- 可选：是否只生成规格，不生成 Harmony 工程

## 输出

必须输出或更新：

- `output/workflow/迁移状态.md`
- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-analyze/ios特性清单.md`
- `output/ios-map/ios-harmony-kit映射.md`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/harmony-visual-verify/界面对齐.md`
- HarmonyOS NEXT 工程目录
- 构建验证结果

## 执行阶段

### 1. 状态检查

读取或创建 `output/workflow/迁移状态.md`。

检查已有产物：

- iOS 分析文档是否存在。
- iOS 截图是否存在。
- 能力映射是否存在。
- Harmony 工程是否存在。
- 最近一次构建是否通过。

### 2. iOS 工程分析

使用 `ios-analyze` skill。

产物：

- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios界面清单.md`
- `output/ios-analyze/ios特性清单.md`
- `output/ios-analyze/`
- `output/ios-analyze/screenshots/png/`

### 3. iOS 能力映射

使用 `ios-map` skill。

产物：

- `output/ios-map/ios-harmony-kit映射.md`

要求：

- 所有能力都进入迁移目标。
- 只能标记为 `平台直迁`、`等价替代` 或 `配套服务`。

### 4. Harmony 工程生成

使用 `harmony-generate` skill。

产物：

- HarmonyOS NEXT 工程目录
- `output/harmony-generate/harmony全量实现追踪.md`

要求：

- 每个 Harmony 模块追溯到 `output/ios-analyze/ios模块结构.md`。
- 每个页面追溯到 `output/ios-analyze/ios功能清单.md` 和 `output/ios-analyze/ios界面清单.md`。
- 每个系统能力追溯到 `output/ios-map/ios-harmony-kit映射.md`。
- 真实数据接入在本阶段完成，新闻流真实数据优先，固定样例数据 只做兜底。
- UI 以 iOS 截图为视觉基准，顶栏、Tab、卡片、字号、颜色、间距、状态都要争取高度还原。

### 5. 视觉验收和构建

使用 `harmony-visual-verify` skill 和 `build-harmony-project` skill。

需要时使用 `harmonyos-live-preview` skill 做 UI 预览和截图。

要求：

- 读取 iOS 截图和 Harmony 截图逐页对比。
- 输出 `output/harmony-visual-verify/界面对齐.md`。
- 差异明显时修复 ArkUI 实现。
- 构建 HAP。
- 更新 `output/workflow/迁移状态.md`。
- 更新 `output/harmony-generate/harmony全量实现追踪.md`。
- 如果失败，记录具体错误和下一步。

## 内部执行策略

工作流优先使用外部 runner 串联多个 `codex exec` 阶段。

默认规则：

- 用户不直接管理 agent。
- `[agents.*]` 只定义身份，不负责启动。
- 每个 `codex exec` 阶段只读取本阶段需要的本地文件。
- 阶段之间通过文件交接，不通过对话记忆交接。

如果未来 Codex 暴露稳定命名 agent 启动 API，可将 runner 的阶段启动方式切换过去。

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

---
name: ios-analyze
description: 分析 iOS Swift/SwiftUI/UIKit 工程，先采集程序化证据，再读取源码生成迁移可消费的 ios-spec.json。用于冻结 iOS 侧工程事实、功能清单、页面规格、系统能力和资源清单；不做 Harmony 代码生成或平台能力映射。
---

# iOS 工程分析

## 目标

把一个 iOS 工程转换成迁移流程稳定消费的“任务索引”。

本 skill 的核心不是截图，也不是大段说明文档，而是从源码中抽取结构化规格：

```text
iOS 工程源码
  -> 源码索引
  -> 模块结构
  -> 功能清单
  -> 页面 / 函数 / 系统能力 / 资源补全
  -> Harmony 迁移可消费的 JSON specs
```

## 职责边界

本 skill 只负责冻结 iOS 侧事实，输出迁移流程可直接消费的结构化规格。

**输入**：iOS 工程源码。

**公共输出**：`ios-spec.json`。

**不做**：Harmony Kit 映射、ArkTS/ArkUI 代码生成、Harmony 模块重组决策。

**关键约束**：

- 对外消费契约是 `ios-spec.json`；`scan/`、`runtime-ui/`、`screenshots/` 只作为内部工作区。
- SwiftSyntax、运行时 UI 树和截图都是内部证据，必须折叠进 `ios-spec.json.screens`。
- Markdown 只给人快速审阅，不作为事实来源。

```text
output_{{PROJECT_NAME}}/ios-analyze/
  ios-spec.json
  assets/
    ios/
    symbols/
    crops/
```

`ios-spec.json` 顶层结构固定为：

```json
{
  "schema_version": "1.0",
  "project": {},
  "modules": [],
  "features": [],
  "functions": [],
  "screens": [],
  "capabilities": [],
  "resources": []
}
```

## 内部编排流程

必须按下面顺序执行。不要跳过前置步骤直接写总结。

### Step 1. 程序化证据采集

**分析范围**：只分析主 App target。以下内容排除，不进入分析：

- **Test target**（`*Tests`、`*UITests`）：单元测试、UI 测试。
- **Widget / Extension target**（`*Widget`、`*Extension`、`*IntentHandler`）：小组件、Siri Intent、Share Extension 等。Widget 的功能如果主 App 也有入口，从主 App 侧分析即可。
- **辅助工具**（SnapshotSupport、XCUITest helper）：测试辅助代码。

这些排除项不进入 modules.json、features.json、functions.json、screens.json。Widget/Extension 迁移作为单独扩展任务处理。

先运行工具采集事实证据，不要让 LLM 先主观总结。采集内容包括：

- 工程结构、target、入口、依赖、源码文件索引。
- `Info.plist`、entitlements、imports、系统 framework 使用情况。
- `Assets.xcassets`、图片、颜色、AppIcon、SF Symbol 使用情况。
- SwiftSyntax / SwiftParser 解析出的 SwiftUI View Tree。
- 按“运行时 UI 树和动态截图采集细则”尝试采集 XCUITest Accessibility Tree；失败不阻塞，但必须把失败原因写入 `screens.json`。
- 截图采集是按需项；只有用户明确要求或任务要求视觉复刻时，才按采集细则执行。

运行扫描脚本生成初始素材：

```bash
python3 skills/ios-analyze/scripts/inspect_ios_project.py \
  --project-root {{IOS_PROJECT}} \
  --output-dir output_{{PROJECT_NAME}}/ios-analyze
```

脚本生成内部索引，不能当作最终结论，也不能成为下游输入契约：

```text
output_{{PROJECT_NAME}}/ios-analyze/scan/
  project.scan.json
  source_index.json
  module_hints.json
  ui_hints.json
  capability_hints.json
  swiftui_view_tree.json
```

其中 `swiftui_view_tree.json` 必须由 SwiftSyntax / SwiftParser 解析 SwiftUI body 得到，是生成 `ios-spec.json.screens.layout_spec` 的首要结构证据。Python 扫描脚本里的正则结果只能作为文件索引和 hints，不能替代 SwiftSyntax View Tree。最终可消费的信息必须进入 `ios-spec.json.screens.source_evidence`、`layout_spec` 和 `component_specs`。

### Step 2. LLM 基于证据读取源码

LLM 必须基于 Step 1 的证据和关键源码生成结构化 specs。扫描结果只能辅助，不能代替源码阅读；SwiftSyntax/UI 树/截图也不能替代源码里的业务逻辑、数据流和 action 分析。

必须读取并核对：

1. `README.md`：产品说明、功能入口。
2. `Package.swift`、`Podfile`、`.xcodeproj`、`.xcworkspace`：依赖和 target。
3. `*App.swift`、`AppDelegate`、`SceneDelegate`：启动入口、依赖注入、生命周期。
4. 根 View / 根 Controller：Tab、导航、路由、全局状态。
5. `Views/`、`Screens/`、`Controllers/`：页面、组件、交互。
6. `Models/`、`Services/`、`Stores/`、`ViewModels/`：数据模型、业务服务、状态管理。
7. `.entitlements`、`Info.plist`、imports：iOS 系统能力。
8. `Assets.xcassets`、图片、颜色：UI 资源。

输出 `ios-spec.json.project`。

### Step 3. 按 iOS 项目结构抽模块

先保留 iOS 原工程结构，不要按 Harmony 主观拆分。

输出 `ios-spec.json.modules`，每个模块至少包含：

- `id`：稳定模块 id，例如 `views.home`、`services.news`。
- `name`：模块名。
- `ios_paths`：源码目录或文件。
- `responsibility`：职责。
- `public_interfaces`：对外接口或主要类型。
- `depends_on`：依赖哪些模块。
- `used_by`：被哪些模块使用。
- `source_refs`：源码引用。
- `suggested_harmony_boundary`：给迁移实现参考的边界，不是最终实现方案。

### Step 4. 抽功能清单

`ios-spec.json.features` 是本 skill 最重要的产物。

功能清单不是说明文档，而是迁移任务索引。每个功能必须能回答：

1. 用户能做什么？
2. 入口在哪里？
3. 涉及哪些页面、模块、函数、数据、资源、系统能力？
4. iOS 源码在哪里？
5. Harmony 侧做到什么才算完成？

功能按三级结构组织：

```text
一级功能 -> 二级功能 -> 三级功能
```

例如：

```text
功能大类 -> 功能子类 -> 具体功能点
```

每个 feature 必须包含：

```json
{
  "id": "",
  "level1": "",
  "level2": "",
  "level3": "",
  "name": "",
  "description": "",
  "user_value": "",
  "entry_points": [],
  "screens": [],
  "modules": [],
  "functions": [],
  "capabilities": [],
  "resources": [],
  "source_refs": [],
  "data_sources": [
    {
      "type": "network|local|database|system|fixed_sample",
      "name": "",
      "fallback": ""
    }
  ],
  "states": ["loading", "populated", "empty", "error"],
  "user_actions": [],
  "acceptance": [],
  "migration_priority": "high|medium|low"
}
```

规则：

- `id` 必须稳定，消费方按它领取任务。
- 不允许只写“首页”“搜索”这种页面名，必须写成用户可感知功能。
- 每个 feature 至少关联一个 `modules` 或 `screens`。
- 核心 feature 必须有关联源码 `source_refs` 和验收标准 `acceptance`。

### Step 5. 抽轻量函数索引

`ios-spec.json.functions` 是为了帮助消费方定位实现，不是完整函数级文档。

粒度控制为：

```text
模块 -> 类型 -> 函数/属性 -> 输入/输出/副作用/关联功能/异步模式/类型定义
```

不要逐行解释实现，不要复制源码。

每项格式：

```json
{
  "id": "",
  "module_id": "",
  "file": "",
  "type": "",
  "kind": "view|model|service|store|view_model|app|widget|extension|utility",
  "member": "",
  "inputs": [],
  "outputs": [],
  "side_effects": [],
  "used_by_features": [],
  "called_by": [],
  "migration_action": "model|service|store|arkui_component|platform_adapter|merge|delete_with_reason",
  "concurrency": "none|async_await|task_group|async_let|callback|combine|gcd|actor|async_stream|timer_publish|dispatch_async",
  "concurrency_detail": ""
}
```

`concurrency` 必须标注，枚举值为：

- `none` — 同步函数
- `async_await` — Swift async/await
- `task_group` — withTaskGroup / withThrowingTaskGroup
- `async_let` — async let 并发绑定
- `callback` — completion handler / delegate 回调
- `combine` — Combine 框架（@Published、Publisher、Sink 等）
- `gcd` — DispatchQueue.async、DispatchSemaphore 等 GCD API
- `actor` — Swift actor 隔离的方法
- `async_stream` — AsyncStream / AsyncSequence
- `timer_publish` — Timer.publish / Timer.scheduledTimer / CADisplayLink
- `dispatch_async` — DispatchQueue.main.asyncAfter / DispatchQueue.main.async

`concurrency_detail` 填具体参数。示例：
- task_group 有并发上限：`"maxConcurrency=5"`
- timer 有间隔：`"interval=1s, repeatForever"`
- dispatch_async 有延迟：`"delay=5s, queue=main"`
- gcd 指定队列：`"queue=global(qos:.background)"`
- actor 隔离上下文：`"isolated by MyActor"`

`kind=model` 且为 enum 或 struct 时，必须用 `type_definition` 列出所有 case 及其关联属性（颜色、描述、rawValue 等），不可省略。

`migration_action` 只能使用：

- `model`
- `service`
- `store`
- `arkui_component`
- `platform_adapter`
- `merge`
- `delete_with_reason`

### Step 6. 抽页面清单

输出 `ios-spec.json.screens`。

页面清单服务于功能清单，必须通过 `feature_ids` 关联功能。

每个 screen 至少包含：

```json
{
  "id": "",
  "name": "",
  "ios_view": "",
  "feature_ids": [],
  "route": "",
  "states": ["loading", "populated", "empty", "error"],
  "key_controls": [],
  "layout_notes": [],
  "layout_confidence": "high|medium|low",
  "source_evidence": [],
  "runtime_ui_tree_evidence": [],
  "screenshot_evidence": [],
  "visual_notes": [],
  "layout_spec": {
    "container": "NavigationStack > ScrollView",
    "sections": []
  },
  "component_specs": {},
  "resource_refs": [],
  "screenshot": "",
  "source_refs": [],
  "navigates_to": [
    {
      "target": "",
      "trigger": "",
      "style": "navigation_push|sheet|full_screen_cover|popover|overlay",
      "source_ref": ""
    }
  ],
  "interactions": [
    {
      "type": "pull_to_refresh",
      "modifier": ".refreshable",
      "source_ref": ""
    }
  ]
}
```

#### layout_spec 提取规则

`layout_spec` 是本 skill 最重要的 UI 产出。它将 SwiftUI body 的 View hierarchy 逐层结构化为 JSON 树，使 `harmony-generate` 不依赖"看截图猜布局"就能精确还原 UI。

`layout_spec` 的生成证据优先级固定为：

1. `scan/swiftui_view_tree.json`：SwiftSyntax 解析出的 SwiftUI AST / View Tree，作为布局结构主证据。
2. `runtime-ui/*.json`：XCUITest Accessibility Tree，作为运行时 UI 结构证据，确认真实渲染的文本、按钮、Tab、输入框、frame、enabled/selected 等。
3. Swift 源码核对：用于确认跨文件状态、数据源、导航目标、effect 消费侧和自定义组件展开。
4. `screenshots/png/`：用于补充真实视觉效果、运行态分支和系统控件样式。

运行时 UI 树和截图不能替代 SwiftSyntax 或源码核对。UI 树只能说明“运行时渲染出了哪些可访问元素”，截图只能说明“运行时看起来如何”，它们都不能单独决定功能边界、数据来源、模块职责、平台能力或控件 action 的真实业务效果。它们的有效信息必须写入同一个 screen 条目的 `runtime_ui_tree_evidence`、`screenshot_evidence` 和 `visual_notes`。

**必须从 SwiftUI 源码逐层提取**：

1. **容器层级**：`NavigationStack > ScrollView > VStack(spacing: 16)` → 记为 `container`。
2. **视觉分区**：每个 VStack 子视图、条件块（`if`）、`Section` 作为一个 section。
3. **元素属性**：font（size + weight）、foregroundStyle/fill、padding、cornerRadius、spacing、lineLimit。
4. **条件渲染**：`if let`/`if !isEmpty` → `condition` 字段或 `optional: true`。
5. **子组件**：独立的 `struct XxxView: View` 提取到 `component_specs`，主页面用 `content_ref` 引用。
6. **导航栏**：`.navigationTitle` → `navigation_bar.title`，`.toolbar` → `navigation_bar.trailing_items/leading_items`。
7. **Tab 栏**：TabView 的 tab items → `tab_bar`（仅在根 TabView 所在页面）。
8. **颜色**：优先提取 hex 值（如 `Color(hex: "AABBCC")` → `"#AABBCC"`），系统色写语义名（如 `"secondary"`）。
9. **数据绑定**：`Text(item.title)` → `source: "item.title"`，`Image(systemName: item.icon)` → `source: "item.icon"`。

`layout_spec` 的完整 schema 和示例见 `references/output-templates.md`。

#### UI 置信度规则

每个 screen 必须写 `layout_confidence`：

- `high`：SwiftSyntax 解析成功，源码核对通过，并有对应截图验证关键视觉。
- `medium`：SwiftSyntax 解析成功并源码核对通过，有运行时 UI 树或截图中的至少一种证据。
- `low`：SwiftSyntax 失败、View Tree 缺失，或只能靠人工源码概括。

如果 `swiftui_view_tree.json` 缺失或解析失败，不能假装高精度；必须在 `screens.json.source_evidence`、`visual_notes` 和 `reports/ios分析摘要.md` 中标记“布局结构低置信度”。

如果运行时 UI 树采集失败，必须在 `runtime_ui_tree_evidence` 中标记失败原因；这不阻断功能清单，但不能声称已完成运行态结构核对。

**禁止**：
- 只写概述性描述（如 `"一个列表"`）而不展开元素。
- 省略 font/spacing/padding/cornerRadius 等视觉参数。
- 把整个页面合并为一个 section。

如果页面 Swift 源码中有 Extracted View（private var / private struct），必须展开到 layout_spec 中，不能只写 `content_ref` 然后跳过内容。

#### 快捷操作入口提取规则（关键主线流程，最易丢失）

页面的 `.toolbar {}`、`.navigationBarItems()`、右上角/左上角的快捷按钮（+添加、详情介绍、编辑、分享、刷新等）是主线用户流程的入口。这些控件不在主 body 的 VStack/HStack 中，而是在 toolbar 修饰符中，**极易被遗漏**，导致用户无法到达核心功能页。

**必须逐个提取**以下位置的每个按钮/控件：

1. **`.toolbar { ToolbarItem(placement: .navigationBarTrailing) { ... } }`** → `navigation_bar.trailing_items[]`
2. **`.toolbar { ToolbarItem(placement: .navigationBarLeading) { ... } }`** → `navigation_bar.leading_items[]`
3. **`.navigationBarItems(trailing: ..., leading: ...)`**（旧 API）→ 同上
4. **Sheet/FullScrrenCover 的触发按钮**（不在 NavigationLink 中，而是 `Button { showSheet = true }`）→ 记录到 `navigates_to` 并标记 trigger 为该按钮
5. **列表中的 `.overlay` 悬浮按钮**（如右下角 FAB）→ 记录为 `layout_spec.sections[]` 中 `type: "floating_button"` 的 section

每个 toolbar item 必须记录：

```json
{
  "type": "button|navigation_link|menu|edit_button|add_button|info_button|share_button",
  "icon": "SF Symbol 名（如 plus、info.circle、square.and.arrow.up）",
  "label": "按钮文字（如果有）",
  "action": "点击后的行为描述",
  "navigates_to": "如果点击后跳转页面，填目标 screen id",
  "triggers_sheet": "如果点击后弹出 sheet，填 sheet 内容描述",
  "source_ref": "Swift 源码位置"
}
```

**验证方法**：对每个页面自问——"用户在这个页面能通过 toolbar 按钮做什么？" 如果答案是"没有按钮"，检查 iOS 源码是否真的没有 `.toolbar`。如果源码有但 layout_spec 没提取，视为提取失败。

#### 功能效果链路规则

每个 UI 控件（toggle/picker/button/input）不仅有"存值入口"，还有"效果消费侧"——即这个值在哪里被读取、产生了什么行为变化。必须分析完整链路，不能只记录控件表面。

规则：
1. 对每个 toggle/picker/button，搜索整个 iOS 工程中该绑定值或动作被读取/使用的位置（不在声明该控件的 View 里，而是在其他 View / App 入口 / Service / Manager 中）。
2. 在 layout_spec 对应 element 中加 `effect` 字段，记录消费位置和效果描述。

示例：
```json
{
  "type": "toggle",
  "label": "Dark Mode",
  "binding": "settings.darkModeEnabled",
  "effect": {
    "source_ref": "{{APP_ENTRY}}.swift:34",
    "description": "应用级 preferredColorScheme 切换深色模式"
  }
}
```

3. 如果一个按钮在 iOS 中执行了多步操作（如"Sync Now" → 调用 CloudSyncManager → 更新 UI），`effect.description` 必须描述完整操作链路。
4. 如果搜索不到消费位置，`effect` 设为 `{"description": "未发现消费侧"}`，由 `harmony-generate` 标记为待确认。
5. 不允许只记录控件表面（type + label + binding）而不记录 effect。

#### navigates_to 规则

- **必须提取**：每个页面中所有 `NavigationLink`、`.sheet`、`.fullScreenCover`、`.popover`、`.overlay`、`present()` 的目标。
- `style` 枚举：`navigation_push` / `sheet` / `full_screen_cover` / `popover` / `overlay` / `tab_switch`。
- 目标必须是另一个 screen id。如果目标是动态的（如 conditional NavigationLink），用数组列出所有可能目标。
- 如果页面没有导航出口，`navigates_to` 为空数组，不要省略字段。

#### interactions 规则

- **必须提取**：所有影响用户交互的 SwiftUI modifier。
- 常见 type：`pull_to_refresh`、`search`、`swipe_action`、`toolbar`、`context_menu`、`on_disappear`、`long_press`、`drag_drop`、`share`、`confirmation_dialog`。
- 每个 interaction 必须记录 `modifier`（SwiftUI modifier 名）和 `source_ref`。
- `toolbar` 类型必须额外记录 `items` 数组（按钮列表）。
- `on_disappear` 类型必须额外记录 `behavior`（做了什么事）。
- `swipe_action` 类型必须额外记录 `direction`（`trailing` / `leading`）。

运行时 UI 树必须尝试采集，失败不阻塞。失败时字段不能简单留空，必须通过 `runtime_ui_tree_evidence` 记录 `status: "failed"`、`failure_reason` 和已尝试的命令或路径；同时通过 `layout_confidence` 降级反映证据不足。截图采集是按需项，未采集时 `screenshot_evidence` 可为空或标记 `status: "skipped"`。页面规格的对外消费入口是 `ios-spec.json.screens`。

每个 screen 还可以包含 `snapshot_arg` 字段，用于截图脚本传递启动参数。如果 iOS 工程有程序化导航到指定页面的机制（如 SnapshotScreen 枚举），则 `snapshot_arg` 设为对应的 rawValue；否则留空。

### Step 7. 抽 iOS 系统能力

输出 `ios-spec.json.capabilities`。

只记录 Apple/iOS 侧事实，不映射 Harmony Kit。

每项至少包含：

- `id`：例如 `network.urlsession`、`webview.safari`、`notification.local`。
- `capability`：iOS API / framework 名称。
- `source_refs`：源码引用。
- `runtime_behavior`：运行时行为。
- `permission_or_entitlement`：权限或 entitlement。
- `feature_ids`：关联功能。

### Step 8. 归档资源

输出 `ios-spec.json.resources`，并尽量归档到 `assets/`。

资源必须通过 `used_by_features` 或 `screen_id` 关联到功能或页面。

必须检查：

- `Assets.xcassets`、图片、颜色、AppIcon、AccentColor。
- SwiftUI `Image(systemName:)`、`Label(systemImage:)`、Tab item 图标。
- 工具栏图标、空态图标、badge/icon、关键颜色。

Tab 栏图标必须单独建资源项。Harmony 侧不能只做文字 Tab。

### 运行时 UI 树和截图采集细则

运行时 UI 树是第二层 UI 证据，优先于截图采集。它通过 XCUITest / XCTest 读取 iOS Accessibility Tree，类似 Android UIAutomator dump，用于补充 SwiftSyntax AST 无法确认的运行态结构信息。

运行时 UI 树必须尝试采集。常见失败原因包括：iOS 工程无法在模拟器启动、没有 UI Test target、无法自动导航到目标页面、登录/权限/网络状态阻塞、可访问性树信息过少。失败不阻塞 `ios-analyze`，但必须写入 `screens.json.runtime_ui_tree_evidence`。

运行时 UI 树至少应记录：

- 元素类型：button / text / image / tab / input / list / navigationBar 等。
- `label` / `value` / `identifier`。
- `frame`：x、y、width、height。
- `enabled` / `selected` / `exists`。
- 所属 screen、runtime_state、采集命令或测试入口。

内部工作文件可输出到：

```text
output_{{PROJECT_NAME}}/ios-analyze/runtime-ui/{{screen_id}}.json
```

辅助脚本：

```bash
# 1. 生成可放入 UI Test target 的 XCTest helper
python3 skills/ios-analyze/scripts/capture_ios_runtime_ui_tree.py \
  --emit-helper output_{{PROJECT_NAME}}/ios-analyze/runtime-ui/RuntimeUITreeDumpTests.swift \
  --output-dir output_{{PROJECT_NAME}}/ios-analyze/runtime-ui

# 2. 将 helper 加入 iOS 工程的 UI Test target 后，用 xcodebuild test 运行并保存日志
# 3. 从日志中解析 BEGIN_IOS_RUNTIME_UI_TREE_JSON / END_IOS_RUNTIME_UI_TREE_JSON
python3 skills/ios-analyze/scripts/capture_ios_runtime_ui_tree.py \
  --xcodebuild-log output_{{PROJECT_NAME}}/ios-analyze/runtime-ui/xcodebuild-runtime-ui.log \
  --screen-id screen.home \
  --runtime-state populated \
  --output-dir output_{{PROJECT_NAME}}/ios-analyze/runtime-ui
```

如果工程没有 UI Test target 或采集失败，不要把运行时 UI 树伪造成已采集；在 `runtime_ui_tree_evidence` 中记录失败原因。

每条运行时证据必须写入 screen 的 `runtime_ui_tree_evidence`：

```json
{
  "path": "output_{{PROJECT_NAME}}/ios-analyze/runtime-ui/screen.home.json",
  "source": "xctest_accessibility",
  "status": "captured|failed",
  "failure_reason": "",
  "runtime_state": "empty|populated|sheet|alert|error",
  "element_count": 0,
  "key_elements": [
    {
      "type": "button",
      "label": "",
      "identifier": "",
      "frame": { "x": 0, "y": 0, "width": 0, "height": 0 },
      "enabled": true,
      "selected": false
    }
  ],
  "ast_runtime_diff": "如果运行时 UI 树与 SwiftSyntax 结构不一致，在这里记录差异"
}
```

可以使用 `XCUIApplication().debugDescription` 或 XCUITest 中遍历 `XCUIElementQuery` 的方式采集。缺少 `accessibilityIdentifier` 时也要保留 label/frame 证据，并在 `visual_notes` 中标记“定位稳定性较低”。

截图是第三层辅助校验项，不是主链路。它用于补充 SwiftSyntax AST 和运行时 UI 树都无法确认的视觉信息，而不是替代源码分析。

只有用户明确要求截图，或任务要求高保真视觉复刻/视觉比对时，才采集关键页面截图。常见失败原因包括：App 启动失败、没有可用 booted simulator、无法自动进入目标页面、登录/权限弹窗阻塞、loading 未完成、截图命令失败。采集失败不阻塞 `ios-analyze`，但必须写入 `screens.json.screenshot_evidence`。

截图任务应覆盖以下页面：

- 代码无法确认视觉结构、控件密度、图标、空态或页面状态。
- 关键页面需要 UI 还原依据。
- 涉及 WebView、地图、定位、相机、相册、登录、分享、TTS、Widget/Card 等系统能力的可见界面。
- SwiftSyntax 和运行时 UI 树能识别结构，但无法确认真实视觉：图片裁剪、系统控件样式、颜色、间距、弹窗、sheet、空态/有数据态。

截图计划写入 `ios-spec.json.screens` 的 `screenshot_plan` 或 screen 条目中，不固定张数。

每条截图证据必须写入 screen 的 `screenshot_evidence`：

```json
{
  "path": "output_{{PROJECT_NAME}}/ios-analyze/screenshots/png/01-home.png",
  "status": "captured|failed|skipped",
  "failure_reason": "",
  "runtime_state": "empty|populated|sheet|alert|error",
  "supplements": ["font_hierarchy", "image_crop", "spacing", "system_control_style"],
  "ast_visual_diff": "如果截图与 SwiftSyntax 结构不一致，在这里记录差异"
}
```

如果 SwiftSyntax、运行时 UI 树和截图不一致，在同一个 screen 条目中保留三类结论：源码结构作为功能事实，UI 树作为运行态结构事实，截图作为视觉事实，并在 `visual_notes` 中标明差异。

截图不能依赖人工点击模拟器；必须通过 XCUITest、启动参数或可重复命令完成。

推荐命令：

```bash
python3 skills/ios-analyze/scripts/capture_ios_snapshots.py \
  --device booted \
  --bundle-id <bundle-id> \
  --screens-spec output_{{PROJECT_NAME}}/ios-analyze/ios-spec.json \
  --output-dir output_{{PROJECT_NAME}}/ios-analyze/screenshots/png
```

### Step 9. 写人工摘要

人工摘要是可选产物，只用于人审阅，必须从 `ios-spec.json` 派生，不要写成事实源。

输出：

- `reports/ios分析摘要.md`

`ios分析摘要.md` 建议包含四段：

1. 工程概览：App 入口、主要 target、依赖、数据来源。
2. 功能摘要：用表格展示三级功能。
3. 页面摘要：列出主要 screen、关联 feature、关键导航和交互。
4. 风险/低置信度项：列出 SwiftSyntax、运行时 UI 树、截图或源码证据不足的地方。

功能摘要表格格式：

```markdown
| 一级功能 | 二级功能 | 三级功能 | 页面 | 数据来源 | iOS 源码 | 迁移优先级 |
|---|---|---|---|---|---|---|
| {{level1}} | {{level2}} | {{level3}} | {{page}} | {{data_source}} | {{source_files}} | {{priority}} |
```

表格只是审阅视图。消费方仍然读取 `ios-spec.json`。

## 规格消费方式

消费方不应该整仓库重新猜功能，而是按 feature id 消费：

```text
实现 {{feature_id}}
读取：
- ios-spec.json.features 中该 feature
- ios-spec.json.modules 中关联模块
- ios-spec.json.functions 中 used_by_features 包含该 feature 的函数
- ios-spec.json.screens 中关联页面
- ios-spec.json.capabilities 中关联系统能力
- ios-spec.json.resources 中关联图标、颜色、图片
```

因此所有 JSON 之间必须用稳定 id 相互引用。

## 质量门槛

- `features.json` 缺少三级结构：失败。
- 核心功能没有 `source_refs`：失败。
- 核心功能没有 `acceptance`：失败。
- `functions.json` 过细到逐行解释或复制源码：失败。
- `functions.json` 中异步函数缺少 `concurrency` 标注：失败。
- `functions.json` 中 `kind=model` 的 enum/struct 缺少 `type_definition`：失败。
- `screens.json` 中页面缺少 `layout_spec` 或 `layout_spec.sections` 为空数组：失败。
- `screens.json` 中 `layout_spec` 只写概述不展开元素层级：失败。
- `screens.json` 中页面缺少 `layout_confidence`：失败。
- SwiftUI 工程未把 SwiftSyntax / SwiftParser 证据写入 `screens.json.source_evidence`，且未标记低置信度：失败。
- `screens.json` 中 `source_evidence` 为空，但页面声称来自源码或 SwiftSyntax：失败。
- `screens.json` 中缺少 `runtime_ui_tree_evidence` 字段：失败。
- 没有运行时 UI 树却声称已完成运行态结构核对：失败。
- `screens.json` 中页面缺少 `navigates_to` 字段：失败。
- `screens.json` 中页面缺少 `interactions` 字段：失败。
- `screens.json` 中 `navigation_bar.trailing_items` 或 `leading_items` 为空，但 iOS 源码中有 `.toolbar`/`.navigationBarItems`：失败。
- `screens.json` 中 toolbar item 缺少 `action` 或 `navigates_to`/`triggers_sheet`（不知道点击后做什么）：失败。
- Markdown 有功能而 JSON 没有：失败。
- JSON 之间无法通过稳定 id 关联：失败。
- 只看 README 或扫描脚本、不读 Swift 源码：失败。
- 执行截图任务时，采集失败必须在 `screenshot_evidence` 记录失败原因，但不能因此跳过功能清单。
- Test target、Widget/Extension target、SnapshotSupport 不应出现在 specs 中。如果出现，视为分析范围错误。

## 失败处理

- 实时数据为空或不稳定：记录真实数据入口，并为截图或验收补固定样例数据。
- UI Test 到不了页面：加 `accessibilityIdentifier` 或测试专用导航入口。
- 资源无法导出：记录 SF Symbols 名称、使用位置、截图裁剪和等价要求。
- 功能归属不清：回到源码调用链，优先按用户入口和状态流归类。

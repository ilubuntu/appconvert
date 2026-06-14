---
name: ios-analyze
description: 当需要读取 iOS Swift/SwiftUI/UIKit 工程，并生成后续迁移模型可消费的结构化功能清单时使用。本 skill 负责源码分析、模块关系、功能清单、轻量函数索引、页面/系统能力/资源清单和少量人工摘要；截图只是辅助证据，不是主产物。
---

# iOS 工程分析

## 目标

把一个 iOS 工程转换成后续模型稳定理解的“迁移任务索引”。

本 skill 的核心不是截图，也不是大段说明文档，而是从源码中抽取结构化规格：

```text
iOS 工程源码
  -> 源码索引
  -> 模块结构
  -> 功能清单
  -> 页面 / 函数 / 系统能力 / 资源补全
  -> 给后续 Harmony 迁移模型消费的 JSON specs
```

## 职责边界

本 skill 只产出 iOS 侧事实和证据：

- 不做 iOS 到 HarmonyOS Kit 映射。
- 不生成 ArkTS / ArkUI 代码。
- 不主观重组 Harmony 模块，只给出可参考的迁移边界。
- 不把 Markdown 表格作为后续模型主输入。

主产物必须是机器可读 JSON。Markdown 只作为人工审阅摘要。

```text
output/ios-analyze/
  specs/
    project.json
    modules.json
    features.json
    functions.json
    screens.json
    capabilities.json
    resources.json
  assets/
    ios/
    symbols/
    crops/
  screenshots/png/
  reports/
    ios工程分析.md
    ios功能摘要.md
    ios界面摘要.md
```

后续 agent 默认读取 `specs/*.json`。`reports/*.md` 只给人看，不作为唯一事实来源。

## 内部编排流程

必须按下面顺序执行。不要跳过前置步骤直接写总结。

### Step 1. 建立工程索引

**分析范围**：只分析主 App target。以下内容排除，不进入分析：

- **Test target**（`*Tests`、`*UITests`）：单元测试、UI 测试。
- **Widget / Extension target**（`*Widget`、`*Extension`、`*IntentHandler`）：小组件、Siri Intent、Share Extension 等。Widget 的功能如果主 App 也有入口，从主 App 侧分析即可。
- **辅助工具**（SnapshotSupport、XCUITest helper）：测试辅助代码。

这些排除项不进入 modules.json、features.json、functions.json、screens.json。如果后续需要迁移 Widget/Extension，作为单独的扩展任务处理。

运行扫描脚本生成初始素材：

```bash
python3 skills/ios-analyze/scripts/inspect_ios_project.py \
  --project-root {{IOS_PROJECT}} \
  --output-dir output/ios-analyze
```

脚本只生成中间索引，不能当作最终结论：

```text
output/ios-analyze/scan/
  project.scan.json
  source_index.json
  module_hints.json
  ui_hints.json
  capability_hints.json
```

然后必须读取关键源码，扫描结果只能辅助，不能代替源码阅读。

必须读取：

1. `README.md`：产品说明、功能入口。
2. `Package.swift`、`Podfile`、`.xcodeproj`、`.xcworkspace`：依赖和 target。
3. `*App.swift`、`AppDelegate`、`SceneDelegate`：启动入口、依赖注入、生命周期。
4. 根 View / 根 Controller：Tab、导航、路由、全局状态。
5. `Views/`、`Screens/`、`Controllers/`：页面、组件、交互。
6. `Models/`、`Services/`、`Stores/`、`ViewModels/`：数据模型、业务服务、状态管理。
7. `.entitlements`、`Info.plist`、imports：iOS 系统能力。
8. `Assets.xcassets`、图片、颜色：UI 资源。

输出 `specs/project.json`。

### Step 2. 按 iOS 项目结构抽模块

先保留 iOS 原工程结构，不要按 Harmony 主观拆分。

输出 `specs/modules.json`，每个模块至少包含：

- `id`：稳定模块 id，例如 `views.home`、`services.news`。
- `name`：模块名。
- `ios_paths`：源码目录或文件。
- `responsibility`：职责。
- `public_interfaces`：对外接口或主要类型。
- `depends_on`：依赖哪些模块。
- `used_by`：被哪些模块使用。
- `source_refs`：源码引用。
- `suggested_harmony_boundary`：给后续迁移参考的边界，不是最终实现方案。

### Step 3. 抽功能清单

`specs/features.json` 是本 skill 最重要的产物。

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
新闻浏览 -> 首页信息流 -> 新闻列表加载与展示
```

每个 feature 必须包含：

```json
{
  "id": "feature.news.home_feed",
  "level1": "新闻浏览",
  "level2": "首页信息流",
  "level3": "新闻列表加载与展示",
  "name": "首页新闻流",
  "description": "用户打开 App 后看到新闻列表，支持分类切换、刷新、进入详情页。",
  "user_value": "快速浏览最新新闻",
  "entry_points": ["ContentView", "HomeView"],
  "screens": ["screen.home.feed"],
  "modules": ["views.home", "services.news", "models.article"],
  "functions": ["services.news.fetchArticles"],
  "capabilities": ["network.urlsession"],
  "resources": ["tab.home", "color.accent"],
  "source_refs": [
    "MyApp/Views/HomeView.swift",
    "MyApp/Services/NewsService.swift"
  ],
  "data_sources": [
    {
      "type": "network",
      "name": "NewsService.fetchTopStories"
    }
  ],
  "states": ["loading", "populated", "empty", "error"],
  "user_actions": ["切换分类", "下拉刷新", "点击新闻卡片进入详情"],
  "acceptance": [
    "首页启动后不能空白",
    "有数据态展示标题、来源、时间和摘要或图片",
    "点击列表项能进入详情页",
    "网络失败时展示固定样例数据或错误态"
  ],
  "migration_priority": "high"
}
```

规则：

- `id` 必须稳定，后续模型按它领取任务。
- 不允许只写“首页”“搜索”这种页面名，必须写成用户可感知功能。
- 每个 feature 至少关联一个 `modules` 或 `screens`。
- 核心 feature 必须有关联源码 `source_refs` 和验收标准 `acceptance`。

### Step 4. 抽轻量函数索引

`specs/functions.json` 是为了帮助后续模型定位实现，不是完整函数级文档。

粒度控制为：

```text
模块 -> 类型 -> 函数/属性 -> 输入/输出/副作用/关联功能/异步模式/类型定义
```

不要逐行解释实现，不要复制源码。

每项格式：

```json
{
  "id": "services.news.fetchArticles",
  "module_id": "services.news",
  "file": "MyApp/Services/NewsService.swift",
  "type": "NewsService",
  "kind": "service",
  "member": "fetchArticles(category:)",
  "inputs": ["category"],
  "outputs": ["Article[]"],
  "side_effects": ["network", "state_update"],
  "used_by_features": ["feature.news.home_feed"],
  "called_by": ["HomeView.refresh"],
  "migration_action": "service",
  "concurrency": "task_group",
  "concurrency_detail": "withTaskGroup, maxConcurrency=5"
}
```

`concurrency` 必须标注，枚举值为：`none` / `async_await` / `task_group` / `async_let` / `callback` / `combine` / `gcd`。

`concurrency_detail` 填具体参数（并发数上限、调度队列、优先级等）。

`kind=model` 且为 enum 或 struct 时，必须用 `type_definition` 列出所有 case 及其关联属性（颜色、描述、rawValue 等），不可省略。

`migration_action` 只能使用：

- `model`
- `service`
- `store`
- `arkui_component`
- `platform_adapter`
- `merge`
- `delete_with_reason`

### Step 5. 抽页面清单

输出 `specs/screens.json`。

页面清单服务于功能清单，必须通过 `feature_ids` 关联功能。

每个 screen 至少包含：

```json
{
  "id": "screen.home.feed",
  "name": "首页信息流",
  "ios_view": "HomeView",
  "feature_ids": ["feature.news.home_feed"],
  "route": "root tab home",
  "states": ["loading", "populated", "empty", "error"],
  "key_controls": ["分类 Tab", "新闻卡片", "刷新入口"],
  "layout_notes": ["顶部分类横滑", "列表卡片纵向滚动"],
  "layout_spec": {
    "container": "NavigationStack > ScrollView",
    "sections": []
  },
  "component_specs": {},
  "resource_refs": ["tab.home"],
  "screenshot": "output/ios-analyze/screenshots/png/home-feed.png",
  "source_refs": ["MyApp/Views/HomeView.swift"],
  "navigates_to": [
    {
      "target": "screen.article.detail",
      "trigger": "tap article card",
      "style": "navigation_push",
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

`layout_spec` 是本 skill 最重要的 UI 产出。它将 SwiftUI body 的 View hierarchy 逐层结构化为 JSON 树，使后续 harmony-generate 不依赖"看截图猜布局"就能精确还原 UI。

**必须从 SwiftUI 源码逐层提取**：

1. **容器层级**：`NavigationStack > ScrollView > VStack(spacing: 16)` → 记为 `container`。
2. **视觉分区**：每个 VStack 子视图、条件块（`if`）、`Section` 作为一个 section。
3. **元素属性**：font（size + weight）、foregroundStyle/fill、padding、cornerRadius、spacing、lineLimit。
4. **条件渲染**：`if let`/`if !isEmpty` → `condition` 字段或 `optional: true`。
5. **子组件**：独立的 `struct XxxView: View` 提取到 `component_specs`，主页面用 `content_ref` 引用。
6. **导航栏**：`.navigationTitle` → `navigation_bar.title`，`.toolbar` → `navigation_bar.trailing_items/leading_items`。
7. **Tab 栏**：TabView 的 tab items → `tab_bar`（仅在根 TabView 所在页面）。
8. **颜色**：优先提取 hex 值（如 `Color(hex: "2ECC71")` → `"#2ECC71"`），系统色写语义名（如 `"secondary"`）。
9. **数据绑定**：`Text(article.title)` → `source: "article.title"`，`Image(systemName: category.icon)` → `source: "category.icon"`。

`layout_spec` 的完整 schema 和示例见 `references/output-templates.md`。

**禁止**：
- 只写概述性描述（如 `"一个列表"`）而不展开元素。
- 省略 font/spacing/padding/cornerRadius 等视觉参数。
- 把整个页面合并为一个 section。

如果页面 Swift 源码中有 Extracted View（private var / private struct），必须展开到 layout_spec 中，不能只写 `content_ref` 然后跳过内容。

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

截图字段可以先为空。截图是辅助证据，不是功能清单成立的前提。

每个 screen 还可以包含 `snapshot_arg` 字段，用于截图脚本传递启动参数。如果 iOS 工程有程序化导航到指定页面的机制（如 SnapshotScreen 枚举），则 `snapshot_arg` 设为对应的 rawValue；否则留空。

### Step 6. 抽 iOS 系统能力

输出 `specs/capabilities.json`。

只记录 Apple/iOS 侧事实，不映射 Harmony Kit。

每项至少包含：

- `id`：例如 `network.urlsession`、`webview.safari`、`notification.local`。
- `capability`：iOS API / framework 名称。
- `source_refs`：源码引用。
- `runtime_behavior`：运行时行为。
- `permission_or_entitlement`：权限或 entitlement。
- `feature_ids`：关联功能。

### Step 7. 归档资源

输出 `specs/resources.json`，并尽量归档到 `assets/`。

资源必须通过 `used_by_features` 或 `screen_id` 关联到功能或页面。

必须检查：

- `Assets.xcassets`、图片、颜色、AppIcon、AccentColor。
- SwiftUI `Image(systemName:)`、`Label(systemImage:)`、Tab item 图标。
- 工具栏图标、空态图标、badge/icon、关键颜色。

Tab 栏图标必须单独建资源项。后续 Harmony 侧不能只做文字 Tab。

### Step 8. 动态截图计划和辅助截图

截图是辅助校验项，不是主链路。

只有在以下情况必须截图：

- 代码无法确认视觉结构、控件密度、图标、空态或页面状态。
- 关键页面需要 UI 还原依据。
- 涉及 WebView、地图、定位、相机、相册、登录、分享、TTS、Widget/Card 等系统能力的可见界面。

截图计划写入 `specs/screens.json` 的 `screenshot_plan` 或 screen 条目中，不固定张数。

截图不能依赖人工点击模拟器；必须通过 XCUITest、启动参数或可重复命令完成。

推荐命令：

```bash
python3 skills/ios-analyze/scripts/capture_ios_snapshots.py \
  --device booted \
  --bundle-id <bundle-id> \
  --screens-spec output/ios-analyze/specs/screens.json \
  --output-dir output/ios-analyze/screenshots/png
```

### Step 9. 写人工摘要

Markdown 只用于人审阅，必须从 JSON specs 派生，不要写成唯一事实源。

输出：

- `reports/ios工程分析.md`
- `reports/ios功能摘要.md`
- `reports/ios界面摘要.md`

`ios功能摘要.md` 用表格展示三级功能：

```markdown
| 一级功能 | 二级功能 | 三级功能 | 页面 | 数据来源 | iOS 源码 | 迁移优先级 |
|---|---|---|---|---|---|---|
| 新闻浏览 | 首页信息流 | 新闻列表加载与展示 | 首页 | 网络/固定样例数据 | HomeView.swift, NewsService.swift | high |
```

表格只是审阅视图。后续模型仍然读取 `specs/features.json`。

## 后续模型消费方式

后续模型不应该整仓库重新猜功能，而是按 feature id 消费：

```text
实现 feature.news.home_feed
读取：
- specs/features.json 中该 feature
- specs/modules.json 中关联模块
- specs/functions.json 中 used_by_features 包含该 feature 的函数
- specs/screens.json 中关联页面
- specs/capabilities.json 中关联系统能力
- specs/resources.json 中关联图标、颜色、图片
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
- `screens.json` 中页面缺少 `navigates_to` 字段：失败。
- `screens.json` 中页面缺少 `interactions` 字段：失败。
- Markdown 有功能而 JSON 没有：失败。
- JSON 之间无法通过稳定 id 关联：失败。
- 只看 README 或扫描脚本、不读 Swift 源码：失败。
- 截图缺失可以标记待补，但不能因此跳过功能清单。
- Test target、Widget/Extension target、SnapshotSupport 不应出现在 specs 中。如果出现，视为分析范围错误。

## 失败处理

- 实时数据为空或不稳定：记录真实数据入口，并为截图或验收补固定样例数据。
- UI Test 到不了页面：加 `accessibilityIdentifier` 或测试专用导航入口。
- 资源无法导出：记录 SF Symbols 名称、使用位置、截图裁剪和等价要求。
- 功能归属不清：回到源码调用链，优先按用户入口和状态流归类。

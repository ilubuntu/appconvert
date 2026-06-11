---
name: ios-analyze
description: 当需要分析 iOS Swift/SwiftUI/UIKit 工程并产出迁移输入物时使用。本 skill 负责审计 iOS 工程结构、模块职责、模块对外接口、模块依赖、功能规格、Apple 能力使用情况，并要求通过 XCUITest 或启动参数直达页面的方式自动采集模拟器截图。它不负责映射 HarmonyOS NEXT Kit，也不生成鸿蒙代码。
---

# iOS 工程分析

## 职责边界

本 skill 只负责把 iOS 原应用分析成稳定的迁移证据：

- `output/01-ios-analyze/ios功能清单.md`
- `output/01-ios-analyze/ios模块结构.md`
- `output/01-ios-analyze/ios界面清单.md`
- `output/01-ios-analyze/ios特性清单.md`
- `output/01-ios-analyze/ios源码索引.md`
- `output/01-ios-analyze/ios函数级清单.md`
- iOS 自动化截图产物

不要用本 skill 决定 HarmonyOS NEXT Kit 映射。不要用本 skill 生成 ArkTS 或鸿蒙工程文件。这些属于其他独立 skill 的职责。

## 强制规则

UI 截图不能依赖人工点击模拟器。截图采集必须通过 XCUITest，或通过 `-uiSnapshotMode` / `-snapshotScreen` 启动参数直达页面，再配合 `simctl io screenshot` 自动完成。

## 工作流

### 1. 审计 iOS 工程

先运行工程扫描脚本：

```bash
python3 skills/ios-analyze/scripts/inspect_ios_project.py \
  --project-root NewsMobile \
  --output-dir output/01-ios-analyze
```

然后必须按工程真实文件逐个读取源码。不能只读 README、根 View 或脚本扫描结果后直接总结。分析颗粒度固定为：

```text
工程 -> Target/目录模块 -> Swift 文件 -> 类型(class/struct/enum/extension) -> 函数/属性 -> UI/业务/系统能力行为
```

按顺序读取这些文件：

1. `README.md`：产品级功能。
2. `*App.swift`、`AppDelegate` 或 `SceneDelegate`：应用生命周期。
3. `ContentView.swift` 等根 UI 文件：Tab 和顶层路由。
4. `Views/`：页面、导航、弹窗、工具栏、列表、表单和状态。
5. `Models/` 和 `Services/`：数据流和业务行为。
6. `.entitlements`、`Info.plist`、project settings、Swift imports：Apple 能力使用情况。

读取要求：

- 每个 `.swift` 文件都要进入 `output/01-ios-analyze/ios源码索引.md`。
- 每个声明的类型、关键属性、函数、`body`、`ViewBuilder`、异步任务、回调、delegate、extension 都要进入 `output/01-ios-analyze/ios函数级清单.md`。
- 对于只有少数 Swift 文件的工程，也不能粗略跳过单文件内的子组件；必须把同一文件内的多个 View、服务、模型拆开记录。
- 如果某个函数只是辅助格式化，也要记录其调用方和迁移处置：直迁、合并、删除或由 Harmony 标准组件替代。
- 任何功能必须能反查到具体文件、类型和函数，不能只写“首页”“服务层”这类宽泛来源。

### 2. 生成 `output/01-ios-analyze/ios源码索引.md`

源码索引用于证明 agent 已经完整读取工程，不允许只输出总结。

格式：

```md
# iOS 源码索引

| 文件 | Target/模块 | 类型清单 | 函数/属性数量 | 主要职责 | 是否迁移 | 迁移去向 |
| --- | --- | --- | --- | --- | --- | --- |
```

每个 Swift 文件后追加细节：

```md
## 文件：NewsMobile/NewsMobile/ContentView.swift

- Target：
- 所属模块：
- imports：
- 类型：
- 关键状态：
- 关键函数：
- UI 子树：
- 数据依赖：
- 系统能力：
- Harmony 迁移去向：
```

### 3. 生成 `output/01-ios-analyze/ios模块结构.md`

模块结构必须参照 iOS 项目真实结构，而不是按鸿蒙主观重组。多 target、多 package、多目录模块时，先记录 iOS 原始模块，再给 HarmonyOS NEXT 建议拆分。

每个模块至少写清楚：

```md
## 模块名称

- iOS 目录 / Target：
- 模块职责：
- 对外接口：
- 输入数据：
- 输出数据：
- 依赖模块：
- 被依赖模块：
- 使用的 Apple 能力：
- HarmonyOS NEXT 参考拆分：
- 验收点：
```

依赖关系要补一张表：

```md
| 上游模块 | 下游模块 | 依赖内容 | 依赖原因 | Harmony 迁移校验 |
| --- | --- | --- | --- | --- |
```

### 4. 生成 `output/01-ios-analyze/ios函数级清单.md`

函数级清单是后续鸿蒙模块生成的硬输入。必须包含所有 Swift 类型和函数。

格式：

```md
# iOS 函数级清单

## 文件：<path>

### 类型：<TypeName>

- 类型种类：View / Model / Service / Store / App / Widget / Extension
- 职责：
- 状态/属性：
- 依赖：
- 被调用方：

| 函数/属性 | 级别 | 输入 | 输出 | 副作用 | UI/业务行为 | 调用关系 | Harmony 迁移动作 |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

`Harmony 迁移动作` 只能使用：

- `保留为独立 ArkTS 函数`
- `迁移为 ArkUI 组件`
- `迁移为 service/store/model`
- `合并到上层组件`
- `由 Harmony Kit 替代`
- `删除，原因：...`

### 5. 生成 `output/01-ios-analyze/ios功能清单.md`

每个功能必须能追溯到源文件。使用以下格式：

```md
## 功能名称

- iOS 入口：file -> view/service/type
- 用户价值：
- UI 表现：
- 数据来源：
- 用户交互：
- 状态：loading / populated / empty / error / permission denied
- 使用的 Apple 能力：
- 证据文件：
- 证据类型：
- 证据函数：
- 关联截图：
- Harmony 模块建议：
- 验收用例：
```

对 NewsMobile，至少覆盖这些功能组：

- 首页新闻流
- 分类切换
- For You 推荐流
- 搜索
- Saved / Watch Later 收藏
- 设置
- 文章详情
- 文章 WebView
- 语音播报 / TTS
- 通知和关键词提醒
- 天气 / 定位
- 自定义订阅源
- 本地新闻
- 新闻聚类和趋势话题

### 6. 生成 `output/01-ios-analyze/ios特性清单.md`

只记录 Apple 侧能力事实，不在这里选择鸿蒙等价能力。

使用以下格式：

```md
| iOS 能力 | 源码证据 | 使用位置 | 运行时行为 | 备注 |
| --- | --- | --- | --- | --- |
```

对 NewsMobile，至少检查：

- SwiftUI 导航和布局
- URLSession
- XMLParser
- UserDefaults
- UserNotifications
- CoreLocation
- WebKit / WKWebView
- AVSpeechSynthesizer
- NaturalLanguage
- WidgetKit
- BackgroundTasks
- iCloud key-value 同步
- Network / NWListener

### 7. 添加确定性的 iOS 截图模式

如果应用还没有稳定数据和 UI 标识，需要在截图前修改 iOS 应用：

- 增加 `-uiSnapshotMode true` 启动参数支持。
- 截图模式下加载 fixture 数据，不只依赖实时网络数据。
- 启动时重置设置、收藏项和搜索状态。
- 尽量禁用或自动处理权限弹窗。
- 给 Tab、卡片、按钮、设置行和主要容器增加 `accessibilityIdentifier`。

使用 `references/xcuitest-snapshot-template.swift` 作为测试结构参考。

### 8. 自动化截图

优先使用 XCUITest。如果维护 UI Test target 的成本过高，也可以使用测试专用启动参数直达页面，再用 `simctl io screenshot` 截图。两种方式都不能依赖人工点击。

自动截图必须满足：

- 使用 `-uiSnapshotMode true` 启动应用。
- 使用 XCUITest 或 `-snapshotScreen <screen>` 到达目标页面。
- 覆盖每个必需页面状态。
- 可以通过命令行重复运行。

XCUITest 推荐命令形式：

```bash
xcodebuild test \
  -project NewsMobile/NewsMobile.xcodeproj \
  -scheme NewsMobile \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro Max' \
  -resultBundlePath output/01-ios-analyze/screenshots/NewsMobileScreenshots.xcresult
```

启动参数直达页面推荐命令形式：

```bash
python3 skills/ios-analyze/scripts/capture_ios_snapshots.py \
  --device booted \
  --bundle-id com.jordankoch.NewsMobile \
  --output-dir output/01-ios-analyze/screenshots/png
```

从 result bundle 导出截图到：

```text
output/01-ios-analyze/screenshots/png/
```

必需截图名称：

```text
01-home.png
02-home-category.png
03-article-detail.png
04-article-webview.png
05-for-you.png
06-search-empty.png
07-search-results.png
08-saved-empty.png
09-saved-with-article.png
10-settings.png
11-keyword-alerts.png
12-custom-feeds.png
13-local-news.png
14-audio-briefing.png
```

### 9. 生成 `output/01-ios-analyze/ios界面清单.md`

每张截图都要描述：

- 截图路径
- iOS 源码 View
- 页面入口路径
- 布局结构
- 关键控件
- 交互行为
- empty/loading/error 状态
- 视觉复刻备注

UI 目标是记录产品行为和信息层级，供 HarmonyOS 实现使用。

## 失败处理

- 如果实时数据为空或不稳定，为截图模式增加 fixture 数据。
- 如果 UI Test 无法到达某个页面，增加 accessibilityIdentifier 或测试专用导航入口。
- 如果权限弹窗阻塞自动化，通过测试状态启动或在测试命令中使用 `simctl privacy` 预处理。

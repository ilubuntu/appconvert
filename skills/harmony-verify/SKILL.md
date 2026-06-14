---
name: harmony-verify
description: 当 HarmonyOS NEXT 迁移工程已经生成后使用。本 skill 对照 iOS 分析产物（功能清单、页面清单、导航图、交互列表）逐项验证 Harmony 工程的迁移完整性，包括功能覆盖、导航可达、交互还原、真实数据、构建通过和视觉还原，输出结构化验收报告和缺口清单。
---

# HarmonyOS NEXT 迁移验收

## 目标

对照 ios-analyze 产出的结构化规格，逐项验证 harmony-generate 产出的 HarmonyOS 工程是否完整迁移。不是只看构建是否通过，而是验证**每个功能、每条导航、每个交互、每个数据源**都有对应的 Harmony 实现。

## 职责边界

输入：

```text
output/ios-analyze/specs/features.json
output/ios-analyze/specs/screens.json
output/ios-analyze/specs/functions.json
output/ios-analyze/specs/capabilities.json
output/platform-adaptation/interaction-adaptation.json
output/platform-adaptation/concurrency-adaptation.json
output/platform-adaptation/implementation-guidance.json
output/harmony-generate/harmony模块实现计划.json
HarmonyOS NEXT 工程
```

输出：

```text
output/harmony-verify/
  verify-report.json
  gaps.json
  reports/迁移验收摘要.md
```

不做的事：

- 不重新分析 iOS 工程。
- 不重新生成 Harmony 代码。
- 不修改工程文件（只读验证）。如果发现缺口，记入 gaps.json，由 harmony-generate 修复后重新验收。

## 验证维度

### 1. 构建验证

- Harmony 工程能否成功构建 HAP？
- 构建失败则后续维度全部跳过，直接报告失败。

### 2. 功能覆盖验证

读取 `features.json`，逐个 feature 检查：

- 是否在 Harmony 工程中找到对应实现文件。
- 对应文件中是否有实质代码（不是空函数或 TODO）。
- `acceptance` 列出的验收标准是否可从代码中推断为已实现。

每个 feature 的验证结果：`passed` / `missing` / `partial`。

### 3. 导航可达验证

读取 `screens.json` 的 `navigates_to` 和 `interaction-adaptation.json` 的 `navigation_map`，逐条检查：

- 目标页面是否在 `main_pages.json` 中注册。
- 源页面代码中是否有跳转到目标页面的代码（Navigation.pushUrl / router.pushUrl / bindSheet 等）。
- `style` 是否匹配（navigation_push 对应 pushUrl，sheet 对应 bindSheet 等）。

每条导航的验证结果：`passed` / `route_missing` / `call_missing` / `style_mismatch`。

### 4. 交互还原验证

读取 `screens.json` 的 `interactions` 和 `interaction-adaptation.json` 的 `interactions`，逐条检查：

- 页面代码中是否有对应交互的 ArkUI 实现。
- 映射关系是否正确（pull_to_refresh → Refresh 组件，search → Search 组件，toolbar → Navigation toolbarConfiguration 等）。

每个交互的验证结果：`passed` / `missing` / `wrong_component`。

### 5. 并发还原验证

读取 `concurrency-adaptation.json`，逐条检查：

- 对应的 Harmony 服务函数是否使用了正确的并发模式。
- `task_group` 映射为 Promise.all 分批，不是串行 for 循环。
- `batch_size` 是否保留。

每个并发映射的验证结果：`passed` / `degraded_to_serial` / `missing`。

### 6. 真实数据验证

读取 `functions.json` 中 `data_sources` 有 `network` 类型的函数，检查：

- Harmony 服务中是否使用相同的 URL（从 iOS 源码提取的真实 URL，不是 example.com）。
- HTTP 请求是否有正确的错误处理（不是 catch 后静默返回空数组）。
- `module.json5` 是否声明了 `ohos.permission.INTERNET`。

每个数据源的验证结果：`passed` / `url_mismatch` / `no_error_handling` / `permission_missing`。

### 7. 平台能力验证

读取 `implementation-guidance.json` 的 `platform_modules`，逐个检查：

- 目标文件是否存在。
- 是否有 public_api 中声明的接口。

### 8. layout_spec 还原验证

读取 `screens.json` 的 `layout_spec`，逐个页面检查：

- `sections` 数组中的每个 section 是否有对应的 ArkUI 代码块。
- `component_specs` 中引用的子组件是否生成。
- `navigation_bar` 的 title 和 toolbar items 是否实现。
- 关键视觉参数（font_size、corner_radius、spacing、padding）是否在代码中体现。
- 条件渲染（`condition` 字段）是否保留为 if 分支。
- **tab_bar 的每个 item 必须有 icon**。检查 `.tabBar()` 调用是否有图标参数，不能只有文字。
- **form_section 的每个 picker row 必须有 Select 组件**。不能只生成 label 文字。
- **每个 screen 必须有对应的页面文件**。screens.json 中每个 screen id 的 ios_view 必须在 Harmony 工程中有对应的 .ets 页面文件。
- **空态/错误态**：每个 screen 的 states 中如果有 `empty`/`error`，对应页面必须有空态/错误态 UI。

每个 layout_spec section 的验证结果：`passed` / `section_missing` / `component_missing` / `params_lost` / `condition_lost` / `tab_icon_missing` / `picker_missing` / `page_missing` / `state_missing`。

### 9. 视觉还原验证（可选）

如果有 iOS 截图且能采集 Harmony 截图，逐页对比。此项为可选加分项，不影响整体通过判定。

## 验证流程

```text
Step 1. 构建验证 → 失败则停止
Step 2. 读取所有输入 JSON
Step 3. 扫描 Harmony 工程所有 .ets 文件
Step 4. 逐维度验证，记录每项结果
Step 5. 输出 verify-report.json
Step 6. 汇总缺口输出 gaps.json
Step 7. 输出人工摘要
```

## 输出格式

### verify-report.json

```json
{
  "schema_version": "1.0",
  "build": { "status": "passed", "hap_path": "" },
  "summary": {
    "total_features": 25,
    "passed_features": 23,
    "total_navigations": 12,
    "passed_navigations": 10,
    "total_interactions": 20,
    "passed_interactions": 18,
    "total_concurrency": 5,
    "passed_concurrency": 4,
    "total_data_sources": 10,
    "passed_data_sources": 8,
    "total_layout_sections": 40,
    "passed_layout_sections": 36,
    "overall": "passed_with_gaps"
  },
  "features": [
    {
      "feature_id": "feature.news.home_feed",
      "status": "passed",
      "harmony_files": ["pages/HomePage.ets"],
      "acceptance_results": [
        { "criterion": "首页启动后不能空白", "status": "passed" }
      ]
    }
  ],
  "navigations": [
    {
      "from": "screen.home.feed",
      "to": "screen.article.detail",
      "trigger": "tap article card",
      "style": "navigation_push",
      "status": "passed",
      "evidence": "HomePage.ets:45 router.pushUrl"
    }
  ],
  "interactions": [
    {
      "screen_id": "screen.home.feed",
      "type": "pull_to_refresh",
      "status": "passed",
      "evidence": "HomePage.ets:78 Refresh component"
    }
  ],
  "concurrency": [
    {
      "function_id": "services.news.fetchAllNews",
      "expected": "Promise.all batched, batch_size=5",
      "actual": "Promise.all with BATCH_SIZE=5",
      "status": "passed"
    }
  ],
  "data_sources": [
    {
      "function_id": "services.news.fetchAllNews",
      "ios_urls": ["http://rss.cnn.com/rss/edition.rss", "..."],
      "harmony_urls": ["http://rss.cnn.com/rss/edition.rss", "..."],
      "status": "passed"
    }
  ],
  "layout_spec": [
    {
      "screen_id": "screen.home.feed",
      "section_id": "sec.home.trending",
      "status": "passed",
      "evidence": "HomePage.ets:52-68 TrendingBar component with horizontal Scroll"
    }
  ]
}
```

### gaps.json

```json
{
  "schema_version": "1.0",
  "gaps": [
    {
      "id": "gap.nav.saved_to_detail",
      "dimension": "navigation",
      "severity": "high",
      "description": "SavedPage 没有跳转到 ArticleDetailPage 的代码",
      "source": { "from": "screen.saved.list", "to": "screen.article.detail" },
      "suggested_fix": "在 SavedPage 的 ArticleCard 点击事件中添加 router.pushUrl 跳转"
    }
  ]
}
```

## 通过标准

- **构建通过**：必须。
- **功能覆盖** ≥ 95%：core 和 high priority feature 必须全部 passed。
- **导航可达** = 100%：每条 navigates_to 都必须有对应实现。
- **交互还原** ≥ 90%：core interaction（pull_to_refresh, toolbar, search）必须 passed。
- **并发还原** = 100%：不允许退化为串行。
- **真实数据** = 100%：必须使用与 iOS 相同的真实 URL。
- **layout_spec 还原** ≥ 90%：每个页面的主要 section 都必须有对应实现。

整体结论：`passed` / `passed_with_gaps` / `failed`。

## 质量门槛

- 构建失败时，验收结论必须是 `failed`。
- 每个维度都必须产出验证结果，不允许跳过。
- gap 必须有 `suggested_fix`，不能只写"有问题"。
- 不允许把"代码存在但未验证可运行"记为 passed。

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
output_{{PROJECT_NAME}}/ios-analyze/specs/features.json
output_{{PROJECT_NAME}}/ios-analyze/specs/screens.json
output_{{PROJECT_NAME}}/ios-analyze/specs/functions.json
output_{{PROJECT_NAME}}/ios-analyze/specs/capabilities.json
output_{{PROJECT_NAME}}/ios-analyze/specs/modules.json
output_{{PROJECT_NAME}}/ios-analyze/specs/resources.json
output_{{PROJECT_NAME}}/platform-adaptation/capability-coverage.json
output_{{PROJECT_NAME}}/platform-adaptation/feature-adaptation.json
output_{{PROJECT_NAME}}/platform-adaptation/interaction-adaptation.json
output_{{PROJECT_NAME}}/platform-adaptation/implementation-guidance.json
output_{{PROJECT_NAME}}/platform-adaptation/risks.json
output_{{PROJECT_NAME}}/harmony-generate/harmony模块实现计划.json
HarmonyOS NEXT 工程
```

输出：

```text
output_{{PROJECT_NAME}}/harmony-verify/
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

读取 `functions.json` 中所有 `concurrency` 不为 `none` 的函数，逐个检查：

- 对应的 Harmony 服务函数是否使用了正确的并发模式（查 `platform-capabilities.json` 中 `category: "concurrency"` 条目）。
- `task_group` 是否映射为 `Promise.all`（有 `maxConcurrency` 时检查分批逻辑）。
- `timer_publish` 是否映射为 `setInterval`，interval 值是否保留，组件销毁时是否 `clearInterval`。
- `dispatch_async` 是否映射为 `setTimeout`，delay 值是否保留。
- `concurrency_detail` 中的参数（interval、delay、maxConcurrency 等）是否在代码中体现。

每个并发函数的验证结果：`passed` / `degraded_to_serial` / `missing` / `pattern_mismatch`。

### 6. 真实数据验证

读取 `features.json` 中所有 feature 的 `data_sources`，筛选 `type` 为 `network` 的条目，检查：

- Harmony 服务中是否使用与 `data_sources[].url` 相同的 URL（不是 example.com）。
- HTTP 请求是否有正确的错误处理（不是 catch 后静默返回空数组）。
- `module.json5` 是否声明了 `ohos.permission.INTERNET`。

每个数据源的验证结果：`passed` / `url_mismatch` / `no_error_handling` / `permission_missing`。

### 7. 平台能力验证

读取 `implementation-guidance.json` 的 `platform_modules`，逐个检查：

- 目标文件是否存在。
- 是否有 public_api 中声明的接口。
- `implementation_tasks[]` 中的每项任务是否有对应的代码实现（不是空壳）。
- `verification[]` 中的每条验证标准是否可从代码中推断为满足。

### 7b. 能力覆盖验证

读取 `capability-coverage.json`，检查：

- `items[]` 中每个 `status` 为 `mapped` 的能力，其 Harmony 侧实现是否存在。
- `unmapped[]` 中的每个能力是否有明确的处理决策（不是静默跳过）。
- capabilities.json 中每个 iOS 能力都出现在 `items` 或 `unmapped` 中（不允许遗漏）。

每个能力的验证结果：`passed` / `mapped_but_missing` / `unmapped_no_decision` / `capability_lost`。

### 7c. 风险缓解验证

读取 `risks.json`，检查每条风险的 `recommended_action` 是否在 Harmony 工程中得到落实：

- `level: "high"` 的风险：`recommended_action` 必须有对应的代码实现或 adapter 层。
- `level: "medium"` 的风险：`recommended_action` 至少有工程侧入口或 TODO 标记。
- `level: "low"` 的风险：可接受记录但不实现。

每条风险的验证结果：`mitigated` / `not_mitigated` / `partially_mitigated`。

### 8. layout_spec 还原验证

读取 `screens.json` 的 `layout_spec`，逐个页面检查：

- `sections` 数组中的每个 section 是否有对应的 ArkUI 代码块。
- `component_specs` 中引用的子组件是否生成。
- `navigation_bar` 的 title 和 toolbar items 是否实现。
- **`navigation_bar.trailing_items` 和 `leading_items` 中的每个 item 都必须有对应的 `.menus()` @Builder 实现**。检查每个 item：
  - 是否有对应的可点击控件（Text/Image/Button）
  - 是否有 `.onClick()` 且实现了真实行为（不是空函数体）
  - 如果 `navigates_to` 非空，onClick 是否调用了 `router.pushUrl()` 跳转
  - 如果 `triggers_sheet` 非空，onClick 是否设置了 bindSheet 的 visible 状态
  - **不允许只渲染图标但没有 onClick**（即"看到了按钮但点了没用"）
- 关键视觉参数（font_size、corner_radius、spacing、padding）是否在代码中体现。
- **禁止硬编码颜色和字号**：扫描所有 .ets 文件，检查是否存在 `.fontColor('#XXXXXX')`、`.backgroundColor('#XXXXXX')`、`.color('#XXXXXX')` 等硬编码颜色值，或 `.fontSize(数字)` 等硬编码字号。颜色必须使用 `$r('app.color.xxx')`，字号必须使用 `$r('app.float.xxx')`。发现硬编码则标记为 `hardcoded_value`。
- **暗色模式资源完整性**：`resources/dark/element/color.json` 中的颜色 name 必须与 `resources/base/element/color.json` 一一对应。缺失暗色配对的资源标记为 `dark_color_missing`。
- 条件渲染（`condition` 字段）是否保留为 if 分支。
- **tab_bar 的每个 item 必须有 icon**。检查 `.tabBar()` 调用是否有图标参数，不能只有文字。
- **form_section 的每个 picker row 必须有 Select 组件**。不能只生成 label 文字。
- **每个 screen 必须有对应的页面文件**。screens.json 中每个 screen id 的 ios_view 必须在 Harmony 工程中有对应的 .ets 页面文件。
- **空态/错误态**：每个 screen 的 states 中如果有 `empty`/`error`，对应页面必须有空态/错误态 UI。

每个 layout_spec section 的验证结果：`passed` / `section_missing` / `component_missing` / `params_lost` / `condition_lost` / `tab_icon_missing` / `picker_missing` / `page_missing` / `state_missing` / `hardcoded_value` / `dark_color_missing` / **`quick_action_missing`**（toolbar 按钮未实现或 onClick 为空）。

### 8b. 快捷操作入口可达验证

对 `navigation_bar.trailing_items` 和 `leading_items` 中的每个 item，检查点击后的用户流程是否可达：

- 如果 item 的 `navigates_to` 指向另一个 screen，验证目标页面是否在 `main_pages.json` 中注册。
- 如果 item 的 `triggers_sheet` 非空，验证 bindSheet 是否绑定到正确的 visible 状态变量。
- 如果 item 的 `action` 描述了具体操作（如"添加新记录"），验证 Harmony 代码中是否实现了该操作。
- **对每个 toolbar item 自问："用户点击这个按钮后，App 会做出正确响应吗？"** 如果 onClick 为空、跳转目标不存在、或操作未实现，标记为 `quick_action_broken`。

每个快捷入口的验证结果：`passed` / `quick_action_missing` / `quick_action_broken`（onClick 存在但行为未实现）。

### 8c. 功能效果链路验证

读取 `screens.json` 的 `layout_spec` 中每个 element 的 `effect` 字段，检查：

- Toggle/Picker/Button 的绑定值是否在 Harmony 代码中产生了实际效果（不是只存了值）。
- 如果 `effect` 字段描述了"在 App 入口消费"（如深色模式），检查 EntryAbility 或根组件是否有对应代码。
- 如果 `effect` 字段描述了"在组件中消费"，检查对应组件是否读取了该值。
- **对每个控件自问："用户操作后 App 行为会变吗？"** 如果不变，标记为 `effect_not_implemented`。

每个效果链路的验证结果：`passed` / `effect_not_implemented` / `effect_partial`。

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
    "total_capability_coverage": 8,
    "passed_capability_coverage": 7,
    "total_risks": 5,
    "mitigated_risks": 4,
    "overall": "passed_with_gaps"
  },
  "features": [
    {
      "feature_id": "",
      "status": "passed",
      "harmony_files": [],
      "acceptance_results": [
        { "criterion": "", "status": "passed" }
      ]
    }
  ],
  "navigations": [
    {
      "from": "",
      "to": "",
      "trigger": "",
      "style": "navigation_push",
      "status": "passed",
      "evidence": ""
    }
  ],
  "interactions": [
    {
      "screen_id": "",
      "type": "pull_to_refresh",
      "status": "passed",
      "evidence": ""
    }
  ],
  "concurrency": [
    {
      "function_id": "",
      "ios_pattern": "timer_publish",
      "ios_detail": "interval=1s",
      "expected": "setInterval 1000ms + clearInterval on destroy",
      "actual": "",
      "status": "passed"
    }
  ],
  "data_sources": [
    {
      "function_id": "",
      "ios_urls": [],
      "harmony_urls": [],
      "status": "passed"
    }
  ],
  "layout_spec": [
    {
      "screen_id": "",
      "section_id": "",
      "status": "passed",
      "evidence": ""
    }
  ],
  "capability_coverage": [
    {
      "capability_id": "",
      "ios_module": "",
      "status": "passed",
      "evidence": ""
    }
  ],
  "risks": [
    {
      "risk_id": "",
      "capability_id": "",
      "level": "high",
      "recommended_action": "",
      "status": "mitigated",
      "evidence": ""
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
      "id": "",
      "dimension": "navigation",
      "severity": "high",
      "description": "",
      "source": { "from": "", "to": "" },
      "suggested_fix": ""
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
- **能力覆盖** ≥ 95%：`unmapped` 能力必须有明确处理决策。
- **风险缓解** = 100% (high)：所有 high 级风险的 `recommended_action` 必须落实。

整体结论：`passed` / `passed_with_gaps` / `failed`。

## 质量门槛

- 构建失败时，验收结论必须是 `failed`。
- 每个维度都必须产出验证结果，不允许跳过。
- gap 必须有 `suggested_fix`，不能只写"有问题"。
- 不允许把"代码存在但未验证可运行"记为 passed。

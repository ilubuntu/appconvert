---
name: platform-adaptation
description: 当 iOS 工程分析已经产出 ios-spec.json，需要把 iOS 原生平台能力适配为 HarmonyOS NEXT Kit/能力策略时使用。本 skill 维护可扩展的平台能力参考库，基于当前工程命中的能力输出可供 Harmony 代码生成直接消费的适配策略、风险、权限和实现任务。
---

# 平台能力适配

## 目标

把 `ios-analyze` 产出的 iOS 事实，按分类参考库转换成 HarmonyOS NEXT 可执行的适配策略。

本 skill 不生成 Harmony 代码，只输出 `platform-adaptation.json` 给 `harmony-generate` 消费。

## 职责边界

输入：

```text
output_{{PROJECT_NAME}}/ios-analyze/ios-spec.json
output_{{PROJECT_NAME}}/ios-analyze/ios-report.md
skills/platform-adaptation/references/platform-capabilities.json  # index
skills/platform-adaptation/references/system-capabilities.json
skills/platform-adaptation/references/ui-interactions.json
skills/platform-adaptation/references/concurrency-patterns.json
skills/platform-adaptation/references/data-storage.json
skills/platform-adaptation/references/media-capabilities.json
```

`ios-report.md` 只辅助理解主流程和风险；匹配和输出必须以 `ios-spec.json` 的稳定 id 为准。

输出：

```text
output_{{PROJECT_NAME}}/platform-adaptation/
  platform-adaptation.json
```

`platform-adaptation.json` 顶层结构固定为：

```json
{
  "schema_version": "1.0",
  "feature_adaptation": {},
  "implementation_guidance": {},
  "interaction_adaptation": {}
}
```

## 参考库分类

| 文件 | 放什么 | 输出到哪里 |
|---|---|---|
| `platform-capabilities.json` | index，只列分类文件 | 不放能力条目 |
| `system-capabilities.json` | 通知、定位、网络、WebView、Widget、NLP、分享、本地网络等系统能力 | `feature_adaptation`、`implementation_guidance.platform_modules` |
| `ui-interactions.json` | TabView、toolbar、sheet、refresh、search、swipe、onAppear/onDisappear 等 UI 交互 | `interaction_adaptation` |
| `concurrency-patterns.json` | async/await、TaskGroup、Combine、GCD、actor、Timer 等并发模式 | `implementation_guidance.concurrency_requirements` |
| `data-storage.json` | UserDefaults、App Groups、iCloud、Observable 状态持久化 | `feature_adaptation`、`store_requirements` |
| `media-capabilities.json` | TTS、音频、相机、相册、图片等媒体能力 | `feature_adaptation`、`platform_modules` |

边界规则：

- `ui-interactions` 不进入 `feature_adaptation`。
- `concurrency-patterns` 不是平台能力，不进入 `feature_adaptation`。
- 基础控件如 `Text/Button/List/Form` 不进参考库；只有会影响导航、位置、系统默认行为或复杂交互的控件才进 `ui-interactions`。

## 内部编排流程

### Step 1. 加载参考库

读取 `platform-capabilities.json.references[]`，再读取所有分类文件。新增能力时只改分类文件，不把条目写回 index。

### Step 2. 匹配系统/存储/媒体能力

用 `ios-spec.json.capabilities` 匹配 `system-capabilities`、`data-storage`、`media-capabilities`。

匹配优先级：

1. `capabilities[].id`
2. `capabilities[].category`
3. `capabilities[].ios_framework`
4. `capabilities[].ios_apis[]`
5. `capabilities[].permission_or_entitlement[]`

不要再从自然语言 `usage` 里猜能力类别；`usage` 只用于生成任务说明和 UI 约束。如果旧 spec 缺少 `category/ios_framework/ios_apis`，必须记录为分析规格缺口，不能静默跳过。

输出到 `feature_adaptation`：

```json
{
  "features": [
    {
      "feature_id": "",
      "adaptation_items": [
        {
          "capability_id": "notification.usernotifications",
          "strategy": "native_equivalent",
          "harmony_kit": "Notification Kit",
          "implementation_boundary": "entry/src/main/ets/platform/NotificationAdapter.ets",
          "required_permissions": [],
          "manifest_changes": [],
          "generation_tasks": [
            "Create notification permission/query adapter",
            "Create local notification publish API"
          ],
          "ui_constraints": [
            "Settings page must preserve permission request entry"
          ],
          "fallback": "If background notification trigger is unavailable, keep in-app badge and foreground alert.",
          "risk_level": "medium",
          "decision_needed": "Whether background delivery is required or foreground-only is acceptable.",
          "source_capability": {
            "category": "notification",
            "ios_framework": "UserNotifications",
            "ios_apis": ["UNUserNotificationCenter"]
          }
        }
      ]
    }
  ]
}
```

参考库缺项时，写 `strategy: "unsupported_pending_decision"`，不要静默跳过。

### Step 3. 匹配 UI 交互

用 `ios-spec.json.screens[].interactions`、`navigates_to`、`layout_spec.tab_bar` 匹配 `ui-interactions.json`。

输出到 `interaction_adaptation`：

```json
{
  "interactions": [
    {
      "screen_id": "screen.content",
      "type": "tab_bar",
      "ios_modifier": "TabView",
      "harmony_component": "Tabs",
      "position": "bottom",
      "implementation_note": "Use Tabs({ index: currentIndex, barPosition: BarPosition.End })"
    }
  ],
  "navigation_map": [],
  "symbol_map": []
}
```

根页面存在 `layout_spec.tab_bar` 时必须生成 `type: "tab_bar"` 交互项。

### Step 4. 匹配并发模式

用 `ios-spec.json.functions[].concurrency` 匹配 `concurrency-patterns.json`。

输出到 `implementation_guidance.concurrency_requirements`，不要写入 `feature_adaptation`。

```json
{
  "concurrency_requirements": [
    {
      "function_id": "",
      "source_concurrency": "task_group",
      "harmony_pattern": "Promise.all with max concurrency batching",
      "implementation_note": "",
      "source_ref": ""
    }
  ]
}
```

### Step 5. 汇总代码生成指导

输出 `implementation_guidance`：

```json
{
  "platform_modules": [],
  "manifest_requirements": [],
  "permission_requirements": [],
  "service_requirements": [],
  "store_requirements": [],
  "concurrency_requirements": []
}
```

`harmony-generate` 优先读这个文件，不重新猜 capability。

### Step 5d. SF Symbol 图标映射

SF Symbols 是 iOS 系统内置的矢量图标库（5000+ 个），不是 app 打包的图片资源。代码中只写名字（如 `"gear"`、`"house.fill"`），系统运行时渲染。HarmonyOS 有**对等的系统符号体系** `sys.symbol.*`（4000+ 个），命名规则与 SF Symbol 几乎一致，通过 `SymbolGlyph` 组件渲染，是 SF Symbol 的直接等价物。

从 `ios-spec.json.screens` 的 `layout_spec`、`component_specs` 和 `ios-spec.json.resources.symbols` 中提取所有 `system_name` / `ios_name` 字段（iOS SF Symbol 名），逐个映射。

**映射策略优先级（严格递减）**：
1. `$r('sys.symbol.xxx')` — HarmonyOS 系统符号资源（4000+ 个，命名与 SF Symbol 近似，**首选**）
2. `$r('sys.media.ohos_ic_public_xxx')` — HarmonyOS 公共图标资源（66 个，部分 private 不可用）
3. Unicode emoji — 仅当 1 和 2 都无对应时

**命名转换规则**：iOS SF Symbol 用点分隔（`star.fill`），HarmonyOS sys.symbol 用下划线分隔（`star_fill`）。转换方法：
- 将 `.` 替换为 `_`
- 个别名称有差异，见下表

**常用 SF Symbol → sys.symbol 对照表（已验证 SDK build-time 可用）**：

| iOS SF Symbol | HarmonyOS sys.symbol | 备注 |
|---|---|---|
| `magnifyingglass` | `sys.symbol.magnifyingglass` | 同名 |
| `star` / `star.fill` | `sys.symbol.star` / `sys.symbol.star_fill` | dot→underscore |
| `house` / `house.fill` | `sys.symbol.house` / `sys.symbol.house_fill` | dot→underscore |
| `gear` | `sys.symbol.gearshape` | gear → gearshape |
| `bookmark` / `bookmark.fill` | `sys.symbol.bookmark` / `sys.symbol.bookmark_fill` | dot→underscore |
| `bell` / `bell.fill` | `sys.symbol.bell` / `sys.symbol.bell_fill` | dot→underscore |
| `person` / `person.fill` | `sys.symbol.person` / `sys.symbol.person_fill` | dot→underscore |
| `trash` / `trash.fill` | `sys.symbol.trash` / `sys.symbol.trash_fill` | dot→underscore |
| `plus` / `plus.circle` / `plus.circle.fill` | `sys.symbol.plus` / `sys.symbol.plus_circle` / `sys.symbol.plus_circle_fill` | dot→underscore |
| `minus` / `minus.circle` | `sys.symbol.minus` / `sys.symbol.minus_circle` | dot→underscore |
| `xmark` / `xmark.circle` / `xmark.circle.fill` | `sys.symbol.xmark` / `sys.symbol.xmark_circle` / `sys.symbol.xmark_circle_fill` | dot→underscore |
| `checkmark` / `checkmark.circle` / `checkmark.circle.fill` | `sys.symbol.checkmark` / `sys.symbol.checkmark_circle` / `sys.symbol.checkmark_circle_fill` | dot→underscore |
| `share` | `sys.symbol.share` | 同名 |
| `pencil` | `sys.symbol.pencil_tip` | pencil → pencil_tip |
| `play` / `play.fill` | `sys.symbol.play` / `sys.symbol.play_fill` | dot→underscore |
| `pause` / `pause.fill` | `sys.symbol.pause` / `sys.symbol.pause_fill` | dot→underscore |
| `chevron.right` / `chevron.left` | `sys.symbol.chevron_right` / `sys.symbol.chevron_left` | dot→underscore |
| `arrow.clockwise` | `sys.symbol.arrow_clockwise` | dot→underscore |
| `info.circle` / `info.circle.fill` | `sys.symbol.info_circle` / `sys.symbol.info_circle_fill` | dot→underscore |
| `clock` / `clock.fill` | `sys.symbol.clock` / `sys.symbol.clock_fill` | dot→underscore |
| `envelope` / `envelope.fill` | `sys.symbol.envelope` / `sys.symbol.envelope_fill` | dot→underscore |
| `folder` / `folder.fill` | `sys.symbol.folder` / `sys.symbol.folder_fill` | dot→underscore |
| `calendar` | `sys.symbol.calendar` | 同名 |
| `wifi` | `sys.symbol.wifi` | 同名 |
| `camera` / `camera.fill` | `sys.symbol.camera` / `sys.symbol.camera_fill` | dot→underscore |
| `ellipsis.circle` | `sys.symbol.ellipsis_circle` | dot→underscore |
| `list.bullet` | `sys.symbol.list_bullet` | dot→underscore |
| `heart` / `heart.fill` | `sys.symbol.heart` / `sys.symbol.heart_fill` | dot→underscore |
| `phone` / `phone.fill` | `sys.symbol.phone` / `sys.symbol.phone_fill` | dot→underscore |
| `photo` | — 无直接对应 | 用 `sys.symbol.camera` 或 emoji |
| `mappin.and.ellipse` | `sys.symbol.mappin_and_rectangle` | 近似 |

不在表中的 SF Symbol：先将 `.` 替换为 `_` 查找 sys.symbol，若无对应再用 emoji。

输出追加到 `platform-adaptation.json.interaction_adaptation`：

```json
{
  "symbol_map": [
    {
      "ios_symbol": "gear",
      "harmony_resource": "sys.symbol.gearshape",
      "mapping_type": "sys_symbol",
      "usage": "tab_bar.settings"
    },
    {
      "ios_symbol": "magnifyingglass",
      "harmony_resource": "sys.symbol.magnifyingglass",
      "mapping_type": "sys_symbol",
      "usage": "tab_bar.search"
    },
    {
      "ios_symbol": "house.fill",
      "harmony_resource": "sys.symbol.house_fill",
      "mapping_type": "sys_symbol",
      "usage": "tab_bar.main"
    }
  ]
}
```

规则：
- layout_spec、component_specs 和 `resources.symbols` 中出现的每个 `system_name` / `ios_name` 都必须出现在 `symbol_map` 中。
- tab_bar.items[].icon 必须被映射。
- `mapping_type` 取值：`sys_symbol`（首选）、`sys_media`（备选）、`emoji`（最后手段）。
- `harmony_resource` 写法：sys_symbol 和 sys_media 写 `sys.symbol.xxx` / `sys.media.ohos_ic_public_xxx`（**不含** `$r()` 包装，harmony-generate 负责包装）；emoji 写 Unicode 转义字符串。
- `harmony-generate` 必须在代码中使用 `symbol_map` 中的映射值，不允许丢弃图标。

**质量门槛**：symbol_map 中 `mapping_type=emoji` 的条目占比超过 30% 时，必须回头逐个查找 sys.symbol/sys.media 对应图标。sys.symbol 有 4000+ 符号，绝大多数 SF Symbol 都有对应。

### Step 6. 写人工摘要

人工摘要是可选产物，只用于人审阅：

```text
output_{{PROJECT_NAME}}/platform-adaptation/reports/平台能力适配摘要.md
```

摘要只给人看，必须引用 JSON 文件路径。

## 策略枚举

`strategy` 只能使用：

- `native_equivalent`：Harmony 有明确原生能力。
- `api_replacement`：能力可替代，但 API 模型不同。
- `product_degradation`：产品行为需要降级。
- `custom_service`：需要自建服务或业务层模拟。
- `unsupported_pending_decision`：当前缺少明确落地方案，必须人工决策。

## 质量门槛

- 当前工程 `ios-spec.json.capabilities` 中每个能力都必须出现在 `platform-adaptation.json.feature_adaptation` 的某个 `adaptation_items[]` 中，或标注 `strategy: "unsupported_pending_decision"`。
- 每个 high/medium priority feature 如果有关联 capability，必须出现在 `platform-adaptation.json.feature_adaptation`。
- `platform-adaptation.json.implementation_guidance` 必须给出目标文件边界和 public API 草案。
- `risk_level: "high"` 的 adaptation_item 必须写明确的 `fallback`。
- 不允许把基础 UI 控件映射塞进平台能力库。
- `ios-spec.json.screens` 中所有页面的 `interactions` 必须出现在 `platform-adaptation.json.interaction_adaptation` 中。
- `ios-spec.json.screens` 中所有 `navigates_to` 条目必须聚合到 `platform-adaptation.json.interaction_adaptation` 的 `navigation_map` 中。
- `ios-spec.json.screens` 的 `layout_spec`、`component_specs` 和 `ios-spec.json.resources.symbols` 中出现的每个图标必须出现在 `platform-adaptation.json.interaction_adaptation` 的 `symbol_map` 中。
- 报告中出现但 `ios-spec.json` 无对应 id 的能力、功能、页面或资源不能直接生成适配项，必须记录为 `spec_gap`。

---
name: platform-adaptation
description: 当 iOS 工程分析已经产出 ios-spec.json，需要把 iOS 原生平台能力适配为 HarmonyOS NEXT Kit/能力策略时使用。本 skill 维护可扩展的平台能力参考库，基于当前工程命中的能力输出可供 Harmony 代码生成直接消费的适配策略、风险、权限和实现任务。
---

# 平台能力适配

## 目标

把 `ios-analyze` 产出的 iOS 平台能力事实，转换成 HarmonyOS NEXT 侧可执行的迁移策略。

本 skill 不是简单表格，也不生成 Harmony 代码。它的产物应该让后续 `harmony-generate` 明确知道：

- 哪些 iOS 能力命中了当前工程。
- 每个能力对应 HarmonyOS NEXT 的哪个 Kit / API area / 工程边界。
- 是否能原生等价、需要替代、需要降级、需要配套服务。
- 要改哪些 module、feature、function、manifest/permission、service/store/page。
- 哪些能力有风险，后续代码生成不能自由发挥。

## 职责边界

输入：

```text
output_{{PROJECT_NAME}}/ios-analyze/ios-spec.json
skills/platform-adaptation/references/platform-capabilities.json
```

读取 `ios-spec.json` 中的 `capabilities`、`features`、`modules`、`functions`、`screens`、`resources` 六个 section。

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

Markdown 只用于人工审阅，不作为跨阶段输入。

## 不纳入本 skill 的范围

不要把基础 UI 控件映射放进能力库，例如：

- SwiftUI `View` -> ArkUI
- `Button` / `Text` / `List` / `Form`
- `NavigationStack` / `TabView`
- Window / Stage 基础生命周期

这些属于后续 UI/工程生成规则。

本 skill 关注平台能力和系统能力，例如：

- 通知、推送、后台任务
- 定位、地图、相机、相册、音频、语音
- WebView、网络、XML/JSON 解析
- 存储、Keychain、iCloud、App Groups
- Widget/Card、分享、支付、健康、蓝牙、NFC
- 机器学习、文本分析、自然语言处理

网络、存储、WebView 虽然基础，但属于平台服务能力，可以保留。

## 内部编排流程

### Step 1. 读取全量能力参考库

读取：

```text
skills/platform-adaptation/references/platform-capabilities.json
```

参考库不要求一次覆盖所有 iOS 能力，但必须优先覆盖当前工程命中的能力。

每条参考能力必须包含：

- `id`
- `ios.frameworks`
- `ios.apis`
- `harmony.kit`
- `harmony.api_area`
- `strategy`
- `permission`
- `manifest`
- `risk_level`
- `implementation_notes`
- `fallback`

### Step 2. 读取当前工程能力事实

读取 `output_{{PROJECT_NAME}}/ios-analyze/ios-spec.json.capabilities`，并结合：

- `features.json`：能力影响哪些功能。
- `functions.json`：能力落在哪些函数/服务。特别关注 `concurrency` 字段，每个异步函数的并发模式必须匹配到参考库中的并发原语映射。
- `modules.json`：能力影响哪些模块边界。
- `screens.json`：特别关注每个页面的 `interactions` 字段，每个交互模式必须匹配到参考库中的交互映射。特别关注 `navigates_to` 字段，记录导航关系供后续 harmony-generate 消费。

### Step 3. 命中能力匹配与 feature 级适配策略

把当前工程 capability 和参考库做归一化匹配，直接产出 `platform-adaptation.json.feature_adaptation`。

**匹配字段优先级**：

1. `capabilities.json[].id`
2. iOS framework 名称，例如 `UserNotifications`、`WebKit`
3. iOS API 名称，例如 `UNUserNotificationCenter`、`WKWebView`
4. entitlement / permission，例如 `aps-environment`、`com.apple.security.application-groups`

如果参考库缺项，不能静默跳过，必须在对应 adaptation_item 中标注 `strategy: "unsupported_pending_decision"` 并给出临时迁移建议。

输出 `platform-adaptation.json.feature_adaptation`。

每个 feature 需要说明：

- `feature_id`
- 命中的平台能力
- 需要新增的 Harmony service / store / platform adapter
- 需要的权限和 manifest 配置
- 需要降级或替代的行为
- 对 UI 生成的约束
- 风险等级和需要人工决策的项（如有）

格式：

```json
{
  "schema_version": "1.0",
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
          "decision_needed": "Whether background delivery is required or foreground-only is acceptable."
        }
      ]
    }
  ]
}
```

规则：
- `risk_level` 取值 `high` / `medium` / `low` / `none`。`high` 表示该能力无原生等价、存在行为差异或需要人工决策；后续 harmony-generate 不允许跳过 `high` 风险的 `fallback` 策略。
- `decision_needed` 仅在该 capability 需要人工决策时填写（如"选什么云后端"），无需决策时留空字符串。
- `high` 风险条目的 `fallback` 必须明确可执行的降级方案。

### Step 5. 生成代码生成指导

输出 `platform-adaptation.json.implementation_guidance`。

这是给 `harmony-generate` 的主要输入。它要按工程层级聚合任务：

```json
{
  "schema_version": "1.0",
  "platform_modules": [
    {
      "id": "platform.notification",
      "target_path": "entry/src/main/ets/platform/NotificationAdapter.ets",
      "source_capabilities": ["notification.usernotifications"],
      "used_by_features": [],
      "public_api": [
        "requestPermission(): Promise<boolean>",
        "publishNotification(title: string, body: string): Promise<void>"
      ],
      "implementation_tasks": [],
      "verification": []
    }
  ],
  "manifest_requirements": [],
  "permission_requirements": [],
  "service_requirements": [],
  "store_requirements": []
}
```

后续代码生成优先读这个文件，而不是重新猜 capability。

### Step 5b. 交互模式适配

从 `screens.json` 的 `interactions` 字段提取所有交互模式，逐个匹配参考库中 `category: "interaction"` 的条目。

输出 `platform-adaptation.json.interaction_adaptation`：

```json
{
  "schema_version": "1.0",
  "interactions": [
    {
      "screen_id": "",
      "type": "pull_to_refresh",
      "ios_modifier": ".refreshable",
      "harmony_component": "Refresh",
      "implementation_note": "用 Refresh 组件包裹列表，绑定 @Trace refreshing 状态和 onRefresh 回调",
      "source_ref": ""
    }
  ],
  "navigation_map": [
    {
      "from": "",
      "to": "",
      "trigger": "",
      "style": "navigation_push",
      "harmony_implementation": "Navigation.pushUrl or router.pushUrl with page params"
    }
  ]
}
```

`navigation_map` 来自所有 screen 的 `navigates_to` 字段聚合。后续 harmony-generate 必须按这个 map 生成路由注册和导航调用。

### Step 5d. SF Symbol 图标映射

SF Symbols 是 iOS 系统内置的矢量图标库（5000+ 个），不是 app 打包的图片资源。代码中只写名字（如 `"gear"`、`"newspaper.fill"`），系统运行时渲染。HarmonyOS 有**对等的系统符号体系** `sys.symbol.*`（4000+ 个），命名规则与 SF Symbol 几乎一致，通过 `SymbolGlyph` 组件渲染，是 SF Symbol 的直接等价物。

从 `screens.json` 的 `layout_spec`、`component_specs` 和 `resources.json` 中提取所有 `system_name` 字段（iOS SF Symbol 名），逐个映射。

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
| `newspaper.fill` | — 无直接对应 | emoji `'\u{1F4F0}'` |
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
      "ios_symbol": "newspaper.fill",
      "harmony_resource": "'\\u{1F4F0}'",
      "mapping_type": "emoji",
      "usage": "tab_bar.home"
    }
  ]
}
```

规则：
- layout_spec 和 component_specs 中出现的每个 `system_name` 都必须出现在 `symbol_map` 中。
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

- 当前工程 `capabilities.json` 中每个能力都必须出现在 `platform-adaptation.json.feature_adaptation` 的某个 `adaptation_items[]` 中，或标注 `strategy: "unsupported_pending_decision"`。
- 每个 high/medium priority feature 如果有关联 capability，必须出现在 `platform-adaptation.json.feature_adaptation`。
- `platform-adaptation.json.implementation_guidance` 必须给出目标文件边界和 public API 草案。
- `risk_level: "high"` 的 adaptation_item 必须写明确的 `fallback`。
- 不允许把基础 UI 控件映射塞进平台能力库。
- `screens.json` 中所有页面的 `interactions` 必须出现在 `platform-adaptation.json.interaction_adaptation` 中。
- `screens.json` 中所有 `navigates_to` 条目必须聚合到 `platform-adaptation.json.interaction_adaptation` 的 `navigation_map` 中。
- `screens.json` 的 `layout_spec` 和 `component_specs` 中出现的每个 `system_name` 必须出现在 `platform-adaptation.json.interaction_adaptation` 的 `symbol_map` 中。

---
name: platform-adaptation
description: 当 iOS 工程分析已经产出 specs/*.json，需要把 iOS 原生平台能力适配为 HarmonyOS NEXT Kit/能力策略时使用。本 skill 维护可扩展的平台能力参考库，基于当前工程命中的能力输出可供 Harmony 代码生成直接消费的适配策略、风险、权限和实现任务。
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
output_{{PROJECT_NAME}}/ios-analyze/specs/capabilities.json
output_{{PROJECT_NAME}}/ios-analyze/specs/features.json
output_{{PROJECT_NAME}}/ios-analyze/specs/modules.json
output_{{PROJECT_NAME}}/ios-analyze/specs/functions.json
skills/platform-adaptation/references/platform-capabilities.json
```

输出：

```text
output_{{PROJECT_NAME}}/platform-adaptation/
  capability-coverage.json
  feature-adaptation.json
  implementation-guidance.json
  risks.json
  interaction-adaptation.json
  concurrency-adaptation.json
  reports/平台能力适配摘要.md
```

不要输出旧式 `ios-harmony-kit映射.md` 作为主产物。Markdown 只用于人工审阅。

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

读取 `output_{{PROJECT_NAME}}/ios-analyze/specs/capabilities.json`，并结合：

- `features.json`：能力影响哪些功能。
- `functions.json`：能力落在哪些函数/服务。特别关注 `concurrency` 字段，每个异步函数的并发模式必须匹配到参考库中的并发原语映射。
- `modules.json`：能力影响哪些模块边界。
- `screens.json`：特别关注每个页面的 `interactions` 字段，每个交互模式必须匹配到参考库中的交互映射。特别关注 `navigates_to` 字段，记录导航关系供后续 harmony-generate 消费。

### Step 3. 命中能力集合

把当前工程 capability 和参考库做归一化匹配。

匹配字段优先级：

1. `capabilities.json[].id`
2. iOS framework 名称，例如 `UserNotifications`、`WebKit`
3. iOS API 名称，例如 `UNUserNotificationCenter`、`WKWebView`
4. entitlement / permission，例如 `aps-environment`、`com.apple.security.application-groups`

输出 `capability-coverage.json`。

格式：

```json
{
  "schema_version": "1.0",
  "items": [
    {
      "capability_id": "notification.usernotifications",
      "status": "mapped",
      "ios": {},
      "harmony": {},
      "matched_by": ["id", "framework"],
      "affected_features": [],
      "affected_modules": [],
      "affected_functions": [],
      "source_refs": []
    }
  ],
  "unmapped": []
}
```

如果参考库缺项，不能静默跳过，必须进入 `unmapped`，并给出临时迁移建议。

### Step 4. 生成 feature 级适配策略

输出 `feature-adaptation.json`。

每个 feature 需要说明：

- `feature_id`
- 命中的平台能力
- 需要新增的 Harmony service / store / platform adapter
- 需要的权限和 manifest 配置
- 需要降级或替代的行为
- 对 UI 生成的约束

格式：

```json
{
  "schema_version": "1.0",
  "features": [
    {
      "feature_id": "feature.notifications.breaking_keyword",
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
          "fallback": "If background notification trigger is unavailable, keep in-app keyword match badge and foreground notification."
        }
      ]
    }
  ]
}
```

### Step 5. 生成代码生成指导

输出 `implementation-guidance.json`。

这是给 `harmony-generate` 的主要输入。它要按工程层级聚合任务：

```json
{
  "schema_version": "1.0",
  "platform_modules": [
    {
      "id": "platform.notification",
      "target_path": "entry/src/main/ets/platform/NotificationAdapter.ets",
      "source_capabilities": ["notification.usernotifications"],
      "used_by_features": ["feature.notifications.breaking_keyword"],
      "public_api": [
        "requestPermission(): Promise<boolean>",
        "publishBreakingNews(title: string, body: string): Promise<void>"
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

输出 `interaction-adaptation.json`：

```json
{
  "schema_version": "1.0",
  "interactions": [
    {
      "screen_id": "screen.home.feed",
      "type": "pull_to_refresh",
      "ios_modifier": ".refreshable",
      "harmony_component": "Refresh",
      "implementation_note": "用 Refresh 组件包裹列表，绑定 @Trace refreshing 状态和 onRefresh 回调",
      "source_ref": ""
    }
  ],
  "navigation_map": [
    {
      "from": "screen.home.feed",
      "to": "screen.article.detail",
      "trigger": "tap article card",
      "style": "navigation_push",
      "harmony_implementation": "Navigation.pushUrl or router.pushUrl with article params"
    }
  ]
}
```

`navigation_map` 来自所有 screen 的 `navigates_to` 字段聚合。后续 harmony-generate 必须按这个 map 生成路由注册和导航调用。

### Step 5c. 并发原语适配

从 `functions.json` 的 `concurrency` 字段提取所有并发模式，逐个匹配参考库中 `category: "concurrency"` 的条目。

输出 `concurrency-adaptation.json`：

```json
{
  "schema_version": "1.0",
  "concurrency_map": [
    {
      "function_id": "services.news.fetchAllNews",
      "ios_pattern": "task_group",
      "ios_detail": "withTaskGroup(maxConcurrency=5)",
      "harmony_pattern": "Promise.all batched",
      "batch_size": 5,
      "implementation_note": "将 RSS 源按 5 个一组切片，每组 Promise.all，串联执行所有批次"
    }
  ]
}
```

后续 harmony-generate 遇到 `task_group` 时必须按 batch_size 分批并发，禁止退化为串行循环。

### Step 5d. SF Symbol 图标映射

从 `screens.json` 的 `layout_spec`、`component_specs` 和 `resources.json` 中提取所有 `system_name` 字段（iOS SF Symbol 名），逐个映射为 HarmonyOS 可用的图标。

HarmonyOS 没有 SF Symbol 等价库，映射策略优先级：
1. `$r('sys.symbol.xxx')` — HarmonyOS 系统符号资源（部分可用）
2. `$r('sys.media.ohos_ic_public_xxx')` — HarmonyOS 公共图标资源
3. Unicode emoji 字符 — 兜底方案，如 `'\u{1F4F0}'`

输出追加到 `interaction-adaptation.json`：

```json
{
  "symbol_map": [
    {
      "ios_symbol": "newspaper.fill",
      "harmony_resource": "\\u{1F4F0}",
      "mapping_type": "emoji",
      "usage": "tab_bar.home, ArticleCard category icon"
    },
    {
      "ios_symbol": "magnifyingglass",
      "harmony_resource": "$r('sys.symbol.search')",
      "mapping_type": "sys_symbol",
      "usage": "tab_bar.search"
    },
    {
      "ios_symbol": "arrow.clockwise",
      "harmony_resource": "\\u{1F504}",
      "mapping_type": "emoji",
      "usage": "HomeView toolbar refresh button"
    }
  ]
}
```

规则：
- layout_spec 和 component_specs 中出现的每个 `system_name` 都必须出现在 `symbol_map` 中。
- tab_bar.items[].icon 必须被映射。
- 后续 harmony-generate 必须在代码中使用 `symbol_map` 中的映射值，不允许丢弃图标。

### Step 6. 输出风险清单

输出 `risks.json`。

风险必须可执行，不要写泛泛而谈。

格式：

```json
{
  "schema_version": "1.0",
  "risks": [
    {
      "id": "risk.background.refresh",
      "level": "high",
      "capability_id": "background.bgapprefresh",
      "affected_features": ["feature.background.refresh"],
      "problem": "iOS BGAppRefreshTask 与 Harmony 后台执行策略不同。",
      "decision_needed": "是否允许降级为前台刷新或定时拉取。",
      "recommended_action": "先实现前台 refresh 和设置开关；后台能力作为单独 platform adapter。"
    }
  ]
}
```

### Step 7. 写人工摘要

输出：

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

- 当前工程 `capabilities.json` 中每个能力都必须出现在 `capability-coverage.json` 的 `items` 或 `unmapped`。
- 每个 high/medium priority feature 如果有关联 capability，必须出现在 `feature-adaptation.json`。
- `implementation-guidance.json` 必须给出目标文件边界和 public API 草案。
- 风险不能只写"有风险"，必须写 `recommended_action`。
- 不允许把基础 UI 控件映射塞进平台能力库。
- `screens.json` 中所有页面的 `interactions` 必须出现在 `interaction-adaptation.json` 中。
- `screens.json` 中所有 `navigates_to` 条目必须聚合到 `interaction-adaptation.json` 的 `navigation_map` 中。
- `functions.json` 中所有 `concurrency` 不为 `none` 的函数必须出现在 `concurrency-adaptation.json` 中。
- `screens.json` 的 `layout_spec` 和 `component_specs` 中出现的每个 `system_name` 必须出现在 `interaction-adaptation.json` 的 `symbol_map` 中。

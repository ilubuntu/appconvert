---
name: harmony-generate
description: 当 iOS 工程分析和平台能力适配完成后使用。本 skill 负责根据迁移规格生成或修改 HarmonyOS NEXT ArkTS/ArkUI 工程，实现页面和服务，接入存储、网络和系统能力，并验证构建。它不重新从头理解 iOS 原工程。
---

# HarmonyOS NEXT 工程辅助生成

## 职责边界

输入：

- `output_{{PROJECT_NAME}}/ios-analyze/specs/project.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/modules.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/features.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/functions.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/screens.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/capabilities.json`
- `output_{{PROJECT_NAME}}/ios-analyze/specs/resources.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/capability-coverage.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/feature-adaptation.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/implementation-guidance.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/risks.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/interaction-adaptation.json`
- `output_{{PROJECT_NAME}}/platform-adaptation/concurrency-adaptation.json`
- 截图产物

输出：

- HarmonyOS NEXT 工程或工程改动
- ArkTS 数据模型、服务和页面
- 真实数据加载链路
- 参照 iOS 截图实现的高保真 ArkUI 页面
- 构建/测试结果摘要
- 全量实现追踪表和外部配套要求

除非规格不完整或互相矛盾，否则不要回到 iOS 工程重新作为主要信息源。

## 工程模板

### 模板位置

```
skills/harmony-generate/references/project-template/
```

### 工程初始化

1. 复制 `references/project-template/` 到目标 Harmony 工程目录，替换占位符（bundleName、vendor、应用名称等）。
2. 工程目录结构由模型根据 iOS 分析产物自行组织，不硬编码。
3. 必须同步维护：每新增 page 更新 `main_pages.json`，按平台能力需求更新 `module.json5`（权限、extensionAbilities 等）。

### module.json5 扩展规则

迁移过程中需要扩展 `module.json5`：

- 新增页面 → 更新 `pages` 字段指向 `$profile:main_pages`（已默认），然后在 `main_pages.json` 添加路由。
- 新增权限 → 在 `module` 下添加 `requestPermissions` 数组。
- 新增后台任务 → 在 `module` 下添加 `extensionAbilities`。
- 新增卡片 → 在 `module` 下添加 `extensionAbilities`（type: "form"）。

### 关键配置文件说明

**`build-profile.json5`（根级）**：
- `signingConfigs`：签名配置，迁移阶段可留空。
- `targetSdkVersion` / `compatibleSdkVersion`：SDK 版本，当前模板为 `"6.0.2(22)"`。
- `products`：构建产物配置。
- `modules`：注册的模块列表，默认只有 `entry`。

**`entry/build-profile.json5`**：
- `apiType: "stageMode"`：Stage 模型（必须）。
- `obfuscation`：混淆开关，默认关闭。

**`entry/src/main/module.json5`**：
- `abilities`：主 Ability 声明（入口页面、图标、label）。
- `extensionAbilities`：备份、卡片等扩展能力。
- `requestPermissions`：运行时权限声明（网络、定位、通知等）。

## 工作流

1. 读取已分析完成的 iOS JSON specs 和平台适配产物（包括 interaction-adaptation.json 和 concurrency-adaptation.json）。
2. 在 **模块实现计划阶段** 执行工程初始化：如果目标 Harmony 工程不存在，从 `project-template/` 复制模板、替换占位符（bundleName、vendor、app_name）、创建迁移目录（由模型根据分析产物自行组织）。
3. 生成模块实现计划（JSON），按 iOS 模块拆分 Harmony models/services/stores/pages/components/platform，每个 iOS 类型/函数映射到 Harmony 文件和迁移动作。
4. 逐模块实现 ArkTS 模型和服务，每个文件必须追溯到 iOS 类型或函数。
5. 接入真实数据源，使用与 iOS 应用相同的数据 URL 和请求方式。不允许出现空白页面。
6. 按 `screens.json` 的 `layout_spec` 和 `component_specs` 实现 ArkUI 页面。`layout_spec` 是 UI 生成的主要输入，截图是辅助参考。不允许只实现信息不完整的框架 UI。
7. 按 `implementation-guidance.json` 的 `platform_modules` 接入平台能力适配层。
8. **实现每个 feature 前，读取 `feature-adaptation.json` 中该 feature 的 `generation_tasks[]`，逐项实现；读取 `ui_constraints[]`，在 UI 生成时遵守约束**。
9. **实现涉及平台能力的代码前，读取 `risks.json` 中该 `capability_id` 对应的风险，按 `recommended_action` 执行**。high 级风险不允许跳过。
10. 生成集成追踪表，明确每个 iOS 类型/函数的 Harmony 去向。
11. 使用本地 HarmonyOS 工具链构建，并用精确文件和命令报告失败。

### 阶段与职责映射

| 阶段 | 按模块 | 职责 |
|---|---|---|
| 模块计划 | — | 从模板创建工程 + 生成 JSON 计划 + 初始化追踪表 |
| 基础层 | models + stores | 所有数据模型 + PersistenceStore |
| 核心功能 | 由 harmony模块实现计划.json 决定 | 根据 features.json 和 modules.json 中的实际模块划分 |
| 设置模块 | 由 harmony模块实现计划.json 决定 | 所有设置和配置页面 |
| 平台能力 | platform/* + module.json5 | 所有平台适配层 |
| 集成构建 | main_pages.json + 缺口修复 | 入口组装 + 路由注册 + 全量检查 + 构建 |

## 实现规则

### 强制：ArkTS 严格模式编码规范

HarmonyOS NEXT 的 ArkTS 使用严格模式，以下 TypeScript/JavaScript 语法**禁止使用**，违反会导致编译失败：

1. **禁止 `any`、`unknown` 类型** — 必须用具体类型。
2. **禁止对象展开 `{...obj}`** — 必须逐字段赋值或写 helper 函数。
3. **禁止解构声明 `const {a, b} = obj`** — 必须逐个赋值。
4. **禁止索引访问 `obj[key]`** — 必须用具体字段名或 `Map`。
5. **禁止对象字面量作类型声明 `Array<{...}>`** — 必须先声明 `interface`，再用 `Array<InterfaceName>`。
6. **禁止无类型对象字面量** — 必须用 `as Type` 或声明 interface。
7. **禁止函数隐式返回类型** — 必须显式标注 `: ReturnType`。
8. **装饰器必须用 V2 版本** — `@ComponentV2`（不是 `@Component`）、`@ObservedV2`（不是 `@Observed`）、`@Trace`（不是 `@Prop`/`@Link`）、`@Local`（组件内部状态）、`@Param`（父传子）、`@Provider`/`@Consumer`（跨层级共享）、`@Event`（子传父回调）。
9. **Store 必须用 `@ObservedV2 + @Trace`** — 这是 SwiftUI `ObservableObject + @Published` 的等价机制。Store 用普通 class 会导致异步数据到达后 UI 永远不刷新。
10. **页面组件用 `@Local` 持有 Store** — Store 属性变化自动触发 build() 重新渲染。
11. **不允许 barrel export（index.ets）** — ArkTS 不支持，必须直接 import 具体文件路径。
12. **RegExp 是独立类型** — 不能赋值给 `string` 变量。

### 强制：按功能清单全量实现

`specs/features.json` 中的每一个 feature 都必须实现，不允许跳过、标记"后续再做"或降级为占位符。实现追踪表中每个 feature 的状态只能是 `已实现` 或 `等价替代`，不能出现 `暂不实现`、`不在范围内`、`占位` 等规避状态。

实现顺序和完整性检查：
1. 读取 `specs/features.json`，列出全部 feature（一级功能→二级功能→三级功能点）。
2. 每个三级功能点必须有对应的 Harmony 文件和代码。
3. 对照 `specs/functions.json`，每个 iOS 函数都有 Harmony 等价实现。
4. **对照 `specs/screens.json`，每个 screen 必须生成对应的页面文件**。不允许跳过任何 screen。screen 的 `ios_view` 名 → 对应的 `pages/XxxPage.ets`，必须在 `main_pages.json` 中注册。
5. 对照 `capability-coverage.json`，每个平台能力都有适配层入口。
6. 缺口必须在集成汇总阶段补齐，不能以"总结"代替实现。

### 强制：真实数据链路必须跑通

iOS 应用从哪些 URL 拿数据，HarmonyOS 应用就从同样的 URL 拿数据。数据获取链路必须端到端可运行，不允许出现空白页面。

规则：

1. **数据源必须与 iOS 一致**。iOS 用哪些 API endpoint、URL、查询参数，HarmonyOS 就用哪些。从 `features.json` 的 `data_sources[].url` 字段提取真实 URL。
2. **HTTP 请求必须能成功**。如果构建通过但运行时数据为空，优先排查：网络权限是否声明（`ohos.permission.INTERNET`）、HTTP 明文请求是否允许（`module.json5` security config）、请求超时设置、响应解析逻辑。
3. **不允许用静态数据掩盖数据获取失败**。如果网络请求失败，页面应该显示错误状态和重试入口，而不是静默切换到预置数据。
4. **数据获取失败的排查优先级高于 UI 还原**。页面能显示真实数据 > 页面样式完美但没有数据。
5. **Store 的 errorMessage 必须在页面中渲染**。当数据加载失败时页面不能空白。每个加载异步数据的页面 build() 中必须有如下模式：

```typescript
if (this.store.errorMessage.length > 0) {
  Column({ space: 16 }) {
    Text('\u{26A0}').fontSize(48).fontColor('#FF9500')
    Text(this.store.errorMessage).fontSize(16).fontColor('#8E8E93')
    Button('Retry').onClick(() => { this.store.loadData() })
  }
  .width('100%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
}
```

### 强制：导航还原规范

`interaction-adaptation.json` 的 `navigation_map` 中每一条导航关系都必须生成对应的路由代码。

规则：

1. `navigation_map` 中的每条记录都必须在 Harmony 工程中实现。不允许出现"页面存在但无法到达"。
2. `style: "navigation_push"` → 使用 `Navigation.pushUrl` 或 `router.pushUrl`，目标页面必须在 `main_pages.json` 中注册。
3. `style: "sheet"` → 使用 `bindSheet` 半模态或 `router.pushUrl`（ArkUI sheet 的限制）。
4. `style: "full_screen_cover"` → 使用 `Navigation.pushUrl` 全屏。
5. `style: "tab_switch"` → 使用 Tabs 组件的 `currentIndex` 切换。
6. 每个 NavigationLink 的 target screen 如果存在于 screens.json，目标页面必须生成。
7. 如果导航断裂（源页面有 navigates_to 但目标页面无入口），视为迁移失败。
8. **不允许跳过中间页面**。如果 navigates_to 的链路是 A → B → C，A 的点击必须跳到 B，B 内部按钮才跳到 C。不允许从 A 直接跳到 C。
9. **saved/list 页面的 ListItem 必须有 onClick**。不允许只有展示但没有点击导航。

### 强制：交互还原规范

`interaction-adaptation.json` 的 `interactions` 中每一条交互都必须生成对应的 ArkUI 代码。

| iOS interaction | ArkUI 实现 |
|---|---|
| `pull_to_refresh` | 用 `Refresh` 组件包裹列表，绑定 `refreshing` 状态和 `onRefresh` 回调 |
| `search` | 用 `Search` 组件，实现 `onChange` 实时搜索，搜索结果文本高亮 |
| `swipe_action` | 用 `ListItem` 的 `swipeAction` 属性，支持 leading/trailing |
| `toolbar` | 用 `Navigation` 的 `toolbarConfiguration` + `@Builder`，toolbar items 从 adaptation 搬运 |
| `context_menu` | 用 `bindContextMenu` |
| `on_disappear` | 用 `aboutToDisappear` 生命周期，behavior 从 adaptation 搬运 |
| `long_press` | 用 `gesture(LongPressGesture)` |
| `drag_drop` | 用 `ListItem` 的 `onDragStart` / `onDrop` |
| `share` | 用 `@kit.Share` 系统分享面板，不允许仅复制到剪贴板 |
| `confirmation_dialog` | 用 `AlertDialog` 或 `AlertDialog` |

规则：

1. 每个 screen 的 `interactions` 数组不能被忽略或简化。如果一个页面有 3 个 interactions，生成的代码必须体现 3 个。
2. `toolbar` 类型必须生成所有 `items` 中列出的按钮。
3. `on_disappear` 类型必须实现 `behavior` 字段描述的具体行为。
4. `pull_to_refresh` 不能用"页面顶部刷新按钮"替代，必须用 Refresh 组件。
5. **`swipe_action` 必须实现**。iOS 的 `.onDelete` / `.swipeActions` 必须映射为 ArkUI `ListItem` 的 `.swipeAction({ end: { builder: () => { ... } } })`。不允许只有列表但没有滑动删除。

### 强制：空态和错误态必须实现

screens.json 中每个 screen 的 `states` 数组列出了所有页面状态。每个状态都必须有对应的 UI。

规则：

1. **`empty` 状态**：列表为空时必须显示空态（大图标 + 提示文字），不能是空白页面。
2. **`error` 状态**：数据加载失败时必须显示错误信息 + 重试按钮（见"真实数据链路"规则）。
3. **`loading` 状态**：加载中必须显示 Progress 或 Loading 文字，不是空白。
4. **`no_results` 状态**（搜索页）：搜索无结果时显示"No Results"提示。
5. **条件状态**：layout_spec 中标记了 `condition` 的 section，其 else 分支也必须有 UI（如条件 section 的 else 分支空态）。

### 强制：Form 控件完整实现

layout_spec 中 `form_section` 类型的 section 的 `rows` 数组，每一行都必须生成对应的 ArkUI 控件。

| row type | ArkUI 实现 |
|---|---|
| `toggle` | `Toggle({ type: ToggleType.Switch, isOn: binding })` |
| `picker` | `Select([{ value: 'xxx' }, ...]).selected(index)` 绑定到 binding |
| `navigation_link` | `Row { Text(label) ... }.onClick(() => router.pushUrl(...))` |
| `button` | `Button(label)` |
| `info_row` | `Row { Text(label) Text(value) }` |

规则：

1. **不允许遗漏 picker/select**。如果 layout_spec 的 form_section row 类型是 `picker`，必须生成 `Select` 组件和所有选项。不允许只生成 label 文字。
2. **picker 的 options 必须完整**。layout_spec 中列出的每个 option 都必须在 Select 组件的 options 数组中。
3. **条件行**（`condition` 字段非空的 row）必须用 `if (...)` 包裹。

### 强制：持久化必须接通

Store 中的用户数据（收藏、关键词、自定义源、设置）必须持久化到设备存储，应用重启后不丢失。

规则：

1. **列表类 Store 的数据项必须持久化**。toggle/remove/markAsRead 后调用 `PersistenceStore.save()`。
2. **用户配置类 Store 的条目必须持久化**。add/remove/toggle 后保存。
3. **用户自建内容类 Store 的条目必须持久化**。add/remove 后保存。
4. **设置类 Store 的配置必须持久化**。每次修改后保存。
5. 使用 `AppStorageV2` / `PersistenceV2` 或 `preferences` API 实现持久化。
6. 应用启动时 `aboutToAppear` 必须从存储加载数据。

### 强制：功能必须端到端实现（不止 UI 表面）

任何功能都有三层：UI 表面（控件）→ 状态变更（存值）→ 效果生效（真正改变 App 行为）。**三层都必须实现，不允许只做前两层跳过第三层。**

典型错误模式（必须避免）：
- Toggle 能开关、值能存储，但 App 行为不变（"能改但不能用"）
- Button 能点击、弹确认框，但不执行实际操作（"能点但没效果"）
- Picker 能选、值能存，但选了之后没任何影响（"能选但没用"）
- 导航能跳到子页面，但子页面内部功能是空壳（"能进但没内容"）
- 表单能填写、能提交，但提交后数据不处理（"能填但不存"）

规则：

1. **每个 UI 控件必须沿着 iOS 源码追踪到最终效果**。生成 Toggle/Button/Picker 时，不能只生成控件 + 存值，必须回查 iOS 源码中这个绑定值/动作在哪里被读取、产生了什么效果，然后在 Harmony 侧实现等价效果。
2. **如果 iOS 源码中一个设置值在 App 入口处被消费**（如 `App.swift` 中的 `.preferredColorScheme()`），Harmony 侧必须在等价位置（`EntryAbility` 或根组件）实现同样效果。
3. **如果 iOS 源码中一个设置值在某个组件中被读取**（如某个组件读取设置中的开关值决定是否显示某 UI 元素），Harmony 侧对应组件必须读取同样值产生同样行为。
4. **不允许"TODO: 后续接入"**。如果 iOS 源码中某个功能有完整链路，Harmony 侧必须有完整链路。
5. **验证方法**：对每个生成的控件，自问"用户操作这个控件后，App 的行为会发生什么变化？"如果答案是"值存了但没有其他变化"，说明第三层没实现。

### 强制：并发还原规范

`concurrency-adaptation.json` 的 `concurrency_map` 中每一条并发模式都必须按映射关系实现。

规则：

1. `task_group` → `Promise.all` 分批执行，`batch_size` 从 adaptation 读取。禁止简化为串行 for 循环。
2. `async_let` → `Promise.all` 并发发起。
3. `async_await` → ArkTS `async/await`。
4. `callback` → 用 Promise 包装，保持调用链扁平。
5. `combine` → 用事件回调或 `@Watch` 替代。
6. `gcd` → 用 `Task` 或 `worker` 替代。
7. `functions.json` 中标注了 `concurrency` 的函数，其 Harmony 实现必须使用对应的并发模式，不允许退化为同步或串行。

### 强制：layout_spec 驱动 UI 生成

`screens.json` 的 `layout_spec` 是 UI 生成的主要输入，优先级高于截图。每个页面的 ArkUI 代码必须严格按 `layout_spec` 的 section 树和 element 树生成。

**容器映射**：

| layout_spec container | ArkUI 实现 |
|---|---|
| `NavigationStack > ScrollView` | `Navigation { Scroll() { Column() } }` |
| `NavigationStack > List` | `Navigation { List() }` |
| `NavigationStack > Form` | `Navigation { Column() { ... Form 用 Column + Divider 模拟 } }` |
| `TabView` | `Tabs()` |

**section 类型映射**：

| layout_spec type | ArkUI 实现 |
|---|---|
| `lazy_list` | `List() { ForEach() { ListItem() { ... } } }` |
| `scroll_row` | `Scroll(ScrollDirection.Horizontal) { Row() { ForEach() { ... } } }` |
| `list` | `List() { ... }` |
| `form_section` | `Column() { Text(header).fontWeight(FontWeight.Bold) ... }` + 分隔线 |
| `conditional_widget` | `if (condition) { ... }` |
| `conditional_list` | `if (condition) { ... }` |
| `grid` | `GridRow() { ForEach() { ... } }` |

**element 属性映射**：

| layout_spec attribute | ArkUI 实现 |
|---|---|
| `font_size: 14, font_weight: "semibold"` | `.fontSize(14).fontWeight(FontWeight.Bolder)` |
| `color: "#FF9500"` | `.fontColor('#FF9500')` |
| `padding: { horizontal: 16 }` | `.padding({ left: 16, right: 16 })` |
| `corner_radius: 12` | `.borderRadius(12)` |
| `max_lines: 3` | `.maxLines(3).textOverflow({ overflow: TextOverflow.Ellipsis })` |
| `background: "secondarySystemBackground"` | `.backgroundColor($r('sys.color.ohos_id_color_sub_background'))` |
| `system_name: "star.fill"` | 需映射到 HarmonyOS 系统图标或自定义 resource |
| `spacing: 10` | Column/Row 的 `space: 10` 参数 |

**规则**：

1. **逐 section 生成**：`layout_spec.sections` 有几项，代码就分几个视觉区块。不允许把多个 section 合并。
2. **视觉参数必须还原**：每个 element 的 `font_size`、`color`、`padding`、`corner_radius`、`spacing`、`max_lines` 都要体现在 ArkUI 代码中。
3. **条件渲染必须保留**：`condition` 字段要翻译为 `if (...)` 分支，不能去掉条件默认显示。
4. **component_specs 展开**：`content_ref` 引用的组件要从 `component_specs` 展开生成独立的 `@Builder` 函数或子组件。
5. **navigation_bar 必须实现，且每个 trailing_items/leading_items 都必须生成对应按钮**：`navigation_bar.title` → `Navigation` 的 `.title()`，`trailing_items` 中的每个 button/add_button/info_button/navigation_link → `Navigation` 的 `.menus()` @Builder 中的可点击控件。**根 Tab 页面的 Navigation 必须加 `.hideBackButton(true)`**（Tab 首页没有上级页面，不需要返回按钮）。

   **快捷操作入口实现规范**（主线流程入口，最易丢失）：
   - `trailing_items` 中 `type: "button"` 且 `icon: "plus"` → 生成 `.menus()` 中带 `+` 文字的 Text，`.onClick()` 打开 bindSheet 或 pushUrl
   - `trailing_items` 中 `type: "info_button"` → 生成 `.menus()` 中带 `ⓘ` 或 icon 的按钮，`.onClick()` 跳转到详情页
   - `trailing_items` 中 `type: "navigation_link"` → 生成 `.menus()` 中按钮，`.onClick()` 调用 `router.pushUrl()`
   - `trailing_items` 中 `type: "share_button"` → 生成分享按钮，调用 platform/ShareAdapter
   - `trailing_items` 中 `type: "edit_button"` → 生成编辑模式切换按钮
   - `trailing_items` 中 `type: "conditional"` → 用 `if/else` 分支实现两个状态
   - **每个 menu item 必须有 `.onClick()` 且实现真实行为**，不允许只渲染图标但没有点击事件
   - 如果 `navigates_to` 非空，`.onClick()` 中必须调用 `router.pushUrl()` 跳转到对应页面
   - 如果 `triggers_sheet` 非空，`.onClick()` 中必须设置 `this.sheetVisible = true` 触发 bindSheet
6. **tab_bar 必须实现且必须带图标**：根页面的 `tab_bar` → `Tabs()` 组件，每个 tab item 必须有 icon + label。`tab_bar.items[].icon` 来自 layout_spec，是 iOS SF Symbol 名，必须按下表映射为 HarmonyOS 图标或 emoji。不允许只写文字 tab。

   **tabBar 正确写法（图标和文字分两行，不是拼成一个字符串）**：
   ```typescript
   // ✅ 正确：用 @Builder 返回 Column，图标在上文字在下
   @Builder
   TabBuilder(icon: string, text: string) {
     Column({ space: 4 }) {
       Text(icon).fontSize(20)
       Text(text).fontSize(10).fontColor('#8E8E93')
     }
   }
   // 使用：
    TabContent() { ... }.tabBar(this.TabBuilder('\u{1F4C4}', 'Home'))

    // ❌ 错误：图标和文字拼成一个字符串，会显示 ...
    TabContent() { ... }.tabBar('\u{1F4C4} Home')
   ```
7. **如果 layout_spec 和截图冲突，以 layout_spec 为准**。layout_spec 来自源码事实，截图可能过时或不完整。

### 强制：SF Symbol 映射

layout_spec 和 component_specs 中的 `"system_name"` 字段是 iOS SF Symbol 名。`interaction-adaptation.json` 的 `symbol_map` 提供了每个符号的映射值，必须直接使用。

规则：

1. 读取 `interaction-adaptation.json` 的 `symbol_map`，在代码中查找映射值。
2. 如果 `symbol_map` 中有映射，直接使用 `harmony_resource` 字段的值。
3. 如果 `symbol_map` 中没有（理论上不应该发生），按下表兜底：

**常用兜底映射**：

| iOS SF Symbol | 兜底方案 |
|---|---|
| `*.fill` | 对应 emoji 或 $r 资源 |
| `star.fill` | `'\u{2B50}'` |
| `magnifyingglass` | `'\u{1F50D}'` |
| `bookmark` / `bookmark.fill` | `'\u{1F516}'` / `'\u{1F4D1}'` |
| `gear` | `'\u{2699}'` |
| `arrow.clockwise` | `'\u{1F504}'` |
| `chart.line.uptrend.xyaxis` | `'\u{1F4C8}'` |
| `location.circle` | `'\u{1F4CD}'` |
| `safari` | `'\u{1F310}'` |
| `speaker.wave.2.fill` | `'\u{1F50A}'` |
| `square.and.arrow.up` | `'\u{1F4E4}'` |
| `bolt.fill` | `'\u{26A1}'` |
| `chevron.right` | `'\u{203A}'` |

4. **tab_bar 的每个 item 必须生成带图标的 `.tabBar()` 配置**。ArkUI 的 TabContent `.tabBar()` 支持 `{ text: 'xxx', icon: 'xxx' }` 对象参数。
5. 绝不允许丢弃 `system_name` 字段只留文字。

### 强制：HTTP 请求和错误处理

网络请求必须可诊断、可观测。不允许静默吞掉错误。

规则：

1. **所有 HTTP 请求必须用 hilog 记录**：请求 URL、响应码、响应长度、失败原因。`import { hilog } from '@kit.PerformanceAnalysisKit'`。
2. **catch 块不允许为空或只 return 空值**。必须 `hilog.error()` 记录错误消息。
3. **数据为空时必须显示错误状态**：如果 loadData() 结果为空数组，页面必须显示错误提示文本和重试按钮，不是空白页面。
4. **`module.json5` 必须声明 `ohos.permission.INTERNET`**。
5. **HTTP 请求必须设置 `expectDataType: http.HttpDataType.STRING`**，否则 response.result 可能返回 ArrayBuffer。
6. **Store 的 `errorMessage` 字段必须被页面消费**：当 `errorMessage` 非空时，页面显示错误信息而非空白。

### 追溯规则

- 每个页面必须能追溯到 `specs/features.json` 中的 feature。
- 每个 Harmony 模块必须能追溯到 `specs/modules.json` 中的模块。
- 每个 Harmony 文件必须能追溯到 `specs/functions.json` 中的 iOS 函数。
- 每个系统能力必须能追溯到 `capability-coverage.json` 中的能力。
- 每个 UI 决策必须能追溯到 `specs/screens.json` 的 `layout_spec` 或截图产物。
- 真实数据接入属于本 skill 的职责，不能留给单独后置阶段。
- 不允许只写 mock 或 `example.com` 假数据来冒充迁移完成。
- 网络请求和解析必须有可运行链路，数据必须来自真实 URL。
- 页面实现必须以 iOS 截图为视觉基准，争取高度还原。
- 必须复刻或合理替代顶栏、底部 Tab、卡片、分类 chip、设置列表、空态、详情页操作区等主要 UI。
- 如果 ArkUI 原生控件无法和 iOS 截图一致，优先使用自定义 ArkUI 组件复刻。
- 如果必须采用 HarmonyOS 设计替代，必须记录替代原因、替代组件和保留的交互语义。
- 不按版本切范围；规格里的功能都进入迁移目标。
- 对需要云服务、卡片、后台策略或系统权限的能力，先实现工程侧入口和接口，再记录外部配套要求。
- 优先写简单、可构建、但不能低保真的 ArkTS，不做过度抽象。

## 多 Agent 分工规则

当通过 workflow runner 执行时，本 skill 可以被多个生成阶段复用，但每个阶段只能负责自己的模块范围。

所有阶段都必须读取 `interaction-adaptation.json` 和 `concurrency-adaptation.json`，并在自己的模块范围内实现对应的导航、交互和并发要求。

| 子阶段 | 主要输出 | 禁止事项 |
| --- | --- | --- |
| 模块计划 | Harmony 工程初始化 + `harmony模块实现计划.json` + `harmony全量实现追踪.md` | 不写业务代码 |
| 基础层 | `models/`、`stores/` | 不写页面和 UI |
| 核心功能 | 根据 `harmony模块实现计划.json` 分配的 services/ 和 pages/ | 不写不属于自己的模块 |
| 平台能力 | `platform/`、`module.json5` | 不删减功能 |
| 集成构建 | `main_pages.json`、缺口修复、构建验证 | 不跳过未映射函数 |

每个子阶段都要更新 `output_{{PROJECT_NAME}}/harmony-generate/harmony全量实现追踪.md`，新增或修改的每一项至少包含：

```md
| iOS 文件 | iOS 类型/函数 | Harmony 文件 | Harmony 类型/函数 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- |
```

状态只能使用：

- `已实现`
- `等价替代`
- `工程侧入口已实现，需外部配置`
- `待修复`

不能使用"后续再做""暂不实现""不适用"来规避迁移。

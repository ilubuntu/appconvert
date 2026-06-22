# iOS Analyze JSON 输出模板

这些模板定义 `ios-spec.json` 的顶层 section。`ios-report.md` 只能从 `ios-spec.json` 和源码证据派生，不能成为新的事实源。

## ios-spec.json.project

```json
{
  "project_name": "",
  "root": "",
  "targets": [],
  "bundle_ids": [],
  "entry_points": [],
  "dependencies": {
    "frameworks": [],
    "external": []
  }
}
```

## ios-spec.json.modules

```json
{
  "modules": [
    {
      "id": "views.home",
      "name": "Home Views",
      "ios_paths": [],
      "responsibility": "",
      "public_interfaces": [],
      "depends_on": [],
      "source_refs": [],
      "suggested_harmony_boundary": ""
    }
  ]
}
```

## ios-spec.json.features

```json
{
  "features": [
    {
      "id": "",
      "title": "",
      "level1": "",
      "level2": "",
      "level3": "",
      "summary": "",
      "user_flow": [
        "用户从哪里进入",
        "系统读取或准备什么数据",
        "不同状态下展示什么",
        "用户操作后产生什么结果"
      ],
      "behavior": [
        "业务规则、排序、分组、过滤、校验、点击、删除、编辑等行为事实"
      ],
      "states": ["loading", "populated", "empty", "error"],
      "entry_points": [],
      "screens": [],
      "modules": [],
      "functions": [],
      "capabilities": [],
      "data_sources": [
        {
          "type": "network|local|database|system|fixed_sample",
          "name": "",
          "url": "",
          "fallback": ""
        }
      ],
      "acceptance": [
        {
          "id": "",
          "description": ""
        }
      ],
      "migration_priority": "high|medium|low",
      "source_refs": []
    }
  ]
}
```

## ios-spec.json.functions

```json
{
  "items": [
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
      "migration_action": "model|service|store|arkui_component|platform_adapter|merge|delete_with_reason",
      "concurrency": "none|async_await|task_group|async_let|callback|combine|gcd|actor|async_stream|timer_publish|dispatch_async",
      "concurrency_detail": "",
      "type_definition": []
    }
  ]
}
```

`concurrency` 记录异步执行模式（枚举值见 ios-analyze SKILL.md），`concurrency_detail` 记录具体参数（如 `maxConcurrency=5`、`interval=1s`、`delay=5s`）。

`type_definition` 仅用于 `kind=model` 的 enum/struct 类型，列出完整定义：

```json
{
  "id": "",
  "kind": "model",
  "type": "",
  "member": "enum",
  "type_definition": [
    {"case": "", "color": "", "description": ""}
  ]
}
```

## ios-spec.json.screens

```json
{
  "screens": [
    {
      "id": "",
      "name": "",
      "ios_view": "",
      "feature_ids": [],
      "route": "",
      "states": ["loading", "populated", "empty", "error"],
      "layout_confidence": "high|medium|low",
      "source_evidence": [
        {
          "type": "swift_syntax|source_review",
          "view": "",
          "file": "",
          "node_path": "",
          "notes": ""
        }
      ],
      "runtime_ui_tree_evidence": [
        {
          "path": "",
          "source": "xctest_accessibility",
          "runtime_state": "empty|populated|sheet|alert|error|unknown",
          "element_count": 0,
          "key_elements": [
            {
              "type": "button|text|image|tab|input|list|navigation_bar|unknown",
              "label": "",
              "value": "",
              "identifier": "",
              "frame": { "x": 0, "y": 0, "width": 0, "height": 0 },
              "enabled": true,
              "selected": false,
              "exists": true
            }
          ],
          "ast_runtime_diff": ""
        }
      ],
      "visual_notes": [],
      "layout_spec": {
        "container": "NavigationStack > ScrollView",
        "background": "",
        "sections": [
          {
            "id": "section.empty",
            "type": "empty_state",
            "condition": "",
            "layout": { "direction": "vertical", "spacing": 8, "padding": { "horizontal": 16 } },
            "elements": [
              { "role": "image", "source": "", "resource_ref": "", "size": 72 },
              { "role": "text", "content": "", "font_size": "title2", "font_weight": "semibold", "color": "" },
              { "role": "text", "content": "", "font_size": "body", "color": "secondary" }
            ]
          },
          {
            "id": "section.items",
            "type": "list",
            "name": "",
            "condition": "",
            "data_binding": "",
            "empty_state_ref": "section.empty",
            "spacing": 12,
            "layout": { "padding": { "horizontal": 16 } },
            "row": {
              "component_ref": "",
              "layout": { "direction": "horizontal", "spacing": 8, "padding": { "horizontal": 12, "vertical": 10 }, "corner_radius": 12 },
              "elements": [
                { "role": "image", "binding": "", "resource_ref": "", "size": 40 },
                { "role": "text", "binding": "", "font_size": "body", "font_weight": "semibold", "color": "" },
                { "role": "text", "binding": "", "font_size": "caption", "color": "secondary", "optional": true }
              ],
              "actions": [
                { "type": "tap", "target": "", "source_ref": "" },
                { "type": "swipe_delete", "direction": "trailing", "source_ref": "" }
              ]
            }
          }
        ],
        "navigation_bar": {
          "title": "",
          "title_mode": "large",
          "trailing_items": [
            {
              "type": "button",
              "icon": "",
              "label": "",
              "action": "",
              "navigates_to": "",
              "triggers_sheet": "",
              "source_ref": ""
            },
            {
              "type": "conditional",
              "condition": "",
              "when_true": { "type": "progress_indicator" },
              "when_false": { "type": "button", "icon": "", "action": "" }
            }
          ],
          "leading_items": []
        }
      },
      "component_specs": {
        "": {
          "container": { "direction": "vertical", "spacing": 8, "padding": 12, "corner_radius": 12 },
          "elements": [
            { "role": "text", "binding": "", "font_size": "body", "font_weight": "semibold" },
            { "role": "text", "binding": "", "font_size": "caption", "color": "secondary", "optional": true }
          ]
        }
      },
      "resource_refs": [],
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
          "modifier": "",
          "source_ref": ""
        },
        {
          "type": "search",
          "modifier": "",
          "source_ref": ""
        },
        {
          "type": "swipe_action",
          "modifier": "",
          "direction": "trailing|leading",
          "source_ref": ""
        },
        {
          "type": "toolbar",
          "modifier": "",
          "items": [],
          "source_ref": ""
        },
        {
          "type": "on_disappear",
          "modifier": "",
          "behavior": "",
          "source_ref": ""
        }
      ]
    }
  ]
}
```

如果实际采集了截图，screen 可追加 `screenshot_evidence`；未采集时不要输出空数组或截图计划字段。

### layout_spec 字段说明

`layout_spec` 是从 SwiftUI 源码提取的结构化 UI 规格，是 harmony-generate 生成 ArkUI 代码的**主要视觉输入**。

#### 顶层结构

```json
{
  "container": "NavigationStack > ScrollView",
  "background": "",
  "sections": [],
  "navigation_bar": {},
  "tab_bar": {}
}
```

- `container`：页面容器层级，用 `>` 连接嵌套关系。
- `background`：页面背景色或系统背景。
- `sections`：页面从上到下的视觉分区。
- `navigation_bar`：顶部导航栏配置（标题、快捷操作按钮）。**trailing_items 和 leading_items 中的每个按钮都必须完整提取**，不可省略。这些是主线用户流程的入口（如 +添加、详情介绍、编辑、分享、刷新等），丢失会导致功能不可达。
- `tab_bar`：底部标签栏配置（仅在根页面出现）。

#### section 类型

| type | 说明 | 关键字段 |
|---|---|---|
| `lazy_list` | LazyVStack/LazyVGrid，纵向滚动列表 | `spacing`, `item_template`, `columns` |
| `scroll_row` | ScrollView(.horizontal)，横向滚动 | `axis: "horizontal"`, `spacing`, `item_template` |
| `list` | List/Form，系统列表 | `style: "plain"\|"insetGrouped"` |
| `form_section` | Form 中的 Section | `header`, `rows` |
| `conditional_widget` | 有条件显示的独立组件 | `condition`, `content_ref` |
| `conditional_list` | 有条件显示的列表 | `condition` |
| `fixed` | 非滚动的固定内容 | `elements` |
| `grid` | LazyVGrid/LazyHGrid | `columns`, `spacing` |

#### element 结构

```json
{
  "role": "text|icon|image|button|badge|spacer|divider|progress|toggle|picker|input|circle",
  "source": "数据绑定路径",
  "content": "固定文本",
  "system_name": "SF Symbol 名",
  "font_size": 14,
  "font_weight": "regular|medium|semibold|bold|headline",
  "color": "#RRGGBB 或语义色名",
  "max_lines": 2,
  "optional": true,
  "condition": "显示条件",
  "action": "交互动作",
  "effect": {
    "source_ref": "消费侧源码位置",
    "description": "该控件值被读取后产生的效果描述"
  },
  "layout": { "direction": "horizontal|vertical", "spacing": 8, "padding": {}, "alignment": "leading|center|trailing" },
  "background": "背景色",
  "corner_radius": 12,
  "children": [],
  "content_ref": "引用 component_specs 中的组件",
  "visual_confirmed_by": "截图路径，可为空"
}
```

`effect` 字段：仅用于 toggle/picker/button/input 类型。记录该控件的绑定值在 iOS 工程中被读取/消费的位置和产生的行为变化。如果搜索不到消费侧，设为 `{"description": "未发现消费侧"}`。

#### tab_bar 结构

```json
{
  "position": "bottom",
  "items": [
    {
      "label": "Tab 标题",
      "icon": "SF Symbol 名（如 house、plus、gear）",
      "target_screen": "对应的 screen id"
    }
  ],
  "accent_color": "#RRGGBB"
}
```

`position` 取值：`bottom|top|side|unknown`。SwiftUI 根 `TabView` 在 iPhone 形态默认写 `bottom`。

#### form_section rows 结构

```json
{
  "rows": [
    {
      "type": "toggle|picker|navigation_link|button|info_row",
      "label": "行标题",
      "binding": "绑定值路径",
      "effect": {
        "source_ref": "消费侧源码位置",
        "description": "效果描述"
      },
      "options": [],
      "target": "",
      "value": ""
    }
  ]
}
```

#### component_specs

页面内复用的子组件，结构与 section 的 element 一致。用 `content_ref` 在 section 中引用。

```json
{
  "ItemRowView": {
    "source_evidence": [
      {
        "type": "swift_syntax",
        "view": "ItemRowView",
        "file": "Views/ItemRowView.swift",
        "node_path": "body.NavigationLink.HStack"
      }
    ],
    "layout": { "direction": "horizontal", "spacing": 8 },
    "elements": [
      { "role": "image", "source": "", "shape": "circle", "visual_confirmed_by": "" },
      { "role": "text", "source": "", "font_size": 20 }
    ]
  }
}
```

#### 提取规则

1. **必须优先从 `scan/swiftui_view_tree.json` 的 SwiftSyntax View Tree 逐层提取**，不能只写概述。
2. 每个 VStack/HStack/List/ScrollView/Section 都必须反映到 sections 或 elements 中。
3. **视觉参数必须提取**：`font` (.system(size:, weight:))、`foregroundColor`、`padding`、`cornerRadius`、`spacing`、`background`、`lineLimit`。
4. `color` 优先提取具体 hex 值；如果用的是系统色（.blue, .secondary），写语义名。
5. 条件渲染（`if let`、`if !isEmpty`）必须记录为 `condition` 或 `optional: true`。
6. 子组件（独立的 `struct XxxView: View`）提取到 `component_specs`，在主页面用 `content_ref` 引用。
7. NavigationStack/NavigationSplitView 的 `.navigationTitle`、`.toolbar` 提取到 `navigation_bar`。
8. TabView 的 tab items 提取到 `tab_bar`。
9. 样式修饰符（.listStyle、.buttonStyle）记录在对应 element 的 `style` 字段。
10. 每个 screen 必须记录 `layout_confidence`、`source_evidence`、`runtime_ui_tree_evidence`；有截图时才记录 `screenshot_evidence`。
11. `runtime_ui_tree_evidence` 来自 XCUITest Accessibility Tree，用于记录运行时真实渲染元素、label/value/identifier、frame、enabled/selected/exists。
12. 截图用于补充字体层级、颜色、间距、图片裁剪、系统控件真实样式和运行态分支，不能替代源码、AST 或运行时 UI 树。
13. 如果 SwiftSyntax、运行时 UI 树和截图不一致，保留三种证据，并在 `visual_notes` / `ast_runtime_diff` / `ast_visual_diff` 中记录差异。

## ios-spec.json.capabilities

```json
{
  "capabilities": [
    {
      "id": "network.urlsession",
      "category": "network",
      "ios_framework": "Foundation",
      "ios_apis": ["URLSession"],
      "usage": "",
      "source_refs": [],
      "permission_or_entitlement": [],
      "migration_risk": "low|medium|high",
      "fallback_required": false
    }
  ]
}
```

## ios-spec.json.resources

```json
{
  "resources": {
    "colors": {
      "accent.primary": {
        "ios_name": "AppTheme.primaryColor",
        "usage": "primary_accent",
        "value": "#4ECDC4",
        "value_light": "#4ECDC4",
        "value_dark": "#4ECDC4",
        "source_ref": "Theme/AppTheme.swift",
        "asset_path": "",
        "target_name": "AppTheme.primaryColor"
      }
    },
    "symbols": {
      "tab.main": {
        "ios_name": "house.fill",
        "usage": "tab_bar.main",
        "source_ref": "RootView.swift",
        "asset_path": "",
        "target_name": "house.fill"
      }
    },
    "images": {
      "logo": {
        "ios_name": "logo",
        "usage": "brand_logo",
        "source_ref": "Assets.xcassets/logo.imageset",
        "asset_path": "assets/ios/logo.png",
        "target_name": "logo"
      }
    }
  }
}
```

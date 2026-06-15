# iOS Analyze JSON 输出模板

这些模板定义后续迁移模型的主输入。Markdown 摘要只能从这些 JSON 派生。

## project.json

```json
{
  "project_name": "",
  "root": "",
  "targets": [],
  "schemes": [],
  "bundle_ids": [],
  "entry_points": [],
  "dependencies": [],
  "build_notes": []
}
```

## modules.json

```json
{
  "modules": [
    {
      "id": "views.home",
      "name": "Home Views",
      "ios_paths": [],
      "responsibility": "",
      "public_interfaces": [],
      "inputs": [],
      "outputs": [],
      "depends_on": [],
      "used_by": [],
      "feature_ids": [],
      "apple_capabilities": [],
      "source_refs": [],
      "suggested_harmony_boundary": ""
    }
  ]
}
```

## features.json

```json
{
  "features": [
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
          "url": "",
          "fallback": ""
        }
      ],
      "states": ["loading", "populated", "empty", "error"],
      "user_actions": [],
      "acceptance": [],
      "migration_priority": "high|medium|low"
    }
  ]
}
```

## functions.json

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
      "used_by_features": [],
      "called_by": [],
      "migration_action": "model|service|store|arkui_component|platform_adapter|merge|delete_with_reason",
      "concurrency": "none|async_await|task_group|async_let|callback|combine|gcd",
      "concurrency_detail": "",
      "type_definition": []
    }
  ]
}
```

`concurrency` 记录异步执行模式，`concurrency_detail` 记录具体参数（并发数、调度策略等）。

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

## screens.json

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
      "key_controls": [],
      "layout_notes": [],
      "layout_spec": {
        "container": "NavigationStack > ScrollView",
        "background": "",
        "sections": [
          {
            "id": "",
            "type": "conditional_widget",
            "condition": "",
            "layout": { "direction": "horizontal", "padding": { "horizontal": 16 } },
            "content_ref": ""
          },
          {
            "id": "",
            "type": "conditional_list",
            "condition": "",
            "layout": { "direction": "vertical", "spacing": 8 },
            "elements": [
              {
                "role": "header",
                "layout": { "direction": "horizontal", "spacing": 4, "padding": { "horizontal": 16 } },
                "children": [
                  { "role": "icon", "system_name": "", "color": "" },
                  { "role": "text", "content": "", "font_size": 15, "font_weight": "semibold" }
                ]
              },
              {
                "role": "scroll_row",
                "axis": "horizontal",
                "spacing": 10,
                "padding": { "horizontal": 16 },
                "item_template": {
                  "layout": { "direction": "horizontal", "spacing": 6, "padding": { "horizontal": 12, "vertical": 8 }, "corner_radius": 20, "background": "tertiarySystemBackground" },
                  "children": [
                    { "role": "icon", "source": "", "font_size": 12, "color": "" },
                    { "role": "text", "source": "", "font_size": 15 },
                    { "role": "badge", "source": "", "font_size": 10, "color": "", "background": "", "padding": { "horizontal": 6, "vertical": 2 }, "corner_radius": 8 }
                  ]
                }
              }
            ]
          },
          {
            "id": "",
            "type": "scroll_row",
            "axis": "horizontal",
            "layout": { "padding": { "horizontal": 0 } },
            "item_template": {
              "layout": { "direction": "horizontal", "spacing": 6, "padding": { "horizontal": 14, "vertical": 8 }, "corner_radius": 999 },
              "background_selected": "",
              "background_unselected": "",
              "children": [
                { "role": "icon", "source": "", "font_size": 14 },
                { "role": "text", "source": "", "font_size": 14, "font_weight_selected": "semibold", "font_weight_unselected": "regular" }
              ]
            }
          },
          {
            "id": "",
            "type": "lazy_list",
            "spacing": 12,
            "layout": { "padding": { "horizontal": 16 } },
            "item_template": {
              "content_ref": ""
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
          "container": {
            "direction": "vertical",
            "alignment": "leading",
            "spacing": 10,
            "padding": 16,
            "background": "secondarySystemBackground",
            "corner_radius": 12
          },
          "elements": [
            {
              "role": "meta_row",
              "layout": { "direction": "horizontal", "spacing": 6 },
              "children": [
                { "role": "icon", "source": "", "color": "" },
                { "role": "text", "source": "", "font_size": 12, "font_weight": "medium" },
                { "role": "spacer" },
                { "role": "text", "source": "", "font_size": 12, "color": "secondary" }
              ]
            },
            {
              "role": "title",
              "source": "",
              "font_size": 17,
              "font_weight": "headline",
              "max_lines": 3
            },
            {
              "role": "description",
              "source": "",
              "font_size": 15,
              "color": "secondary",
              "max_lines": 2,
              "optional": true
            },
            {
              "role": "badges_row",
              "layout": { "direction": "horizontal", "spacing": 8 },
              "children": [
                { "role": "sentiment_badge", "optional": true, "condition": "", "content_ref": "" },
                { "role": "bias_badge", "optional": true, "condition": "", "content_ref": "" },
                { "role": "spacer" },
                { "role": "bookmark_button", "icon": "", "action": "" }
              ]
            }
          ]
        },
        "": {
          "layout": { "direction": "horizontal", "spacing": 4, "padding": { "horizontal": 8, "vertical": 4 }, "corner_radius": 8 },
          "background": "",
          "children": [
            { "role": "icon", "source": "", "color": "" },
            { "role": "text", "source": "", "font_size": 12, "color": "" }
          ]
        },
        "": {
          "layout": { "direction": "horizontal", "spacing": 4, "padding": { "horizontal": 8, "vertical": 4 }, "corner_radius": 8 },
          "background": "",
          "children": [
            { "role": "circle", "size": 6, "color": "" },
            { "role": "text", "source": "", "font_size": 12, "color": "" }
          ]
        }
      },
      "resource_refs": [],
      "screenshot": "",
      "screenshot_required": false,
      "screenshot_reason": "",
      "snapshot_arg": "",
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
  "content_ref": "引用 component_specs 中的组件"
}
```

`effect` 字段：仅用于 toggle/picker/button/input 类型。记录该控件的绑定值在 iOS 工程中被读取/消费的位置和产生的行为变化。如果搜索不到消费侧，设为 `{"description": "未发现消费侧"}`。

#### tab_bar 结构

```json
{
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

#### 提取规则

1. **必须从 SwiftUI body 的 View hierarchy 逐层提取**，不能只写概述。
2. 每个 VStack/HStack/List/ScrollView/Section 都必须反映到 sections 或 elements 中。
3. **视觉参数必须提取**：`font` (.system(size:, weight:))、`foregroundColor`、`padding`、`cornerRadius`、`spacing`、`background`、`lineLimit`。
4. `color` 优先提取具体 hex 值；如果用的是系统色（.blue, .secondary），写语义名。
5. 条件渲染（`if let`、`if !isEmpty`）必须记录为 `condition` 或 `optional: true`。
6. 子组件（独立的 `struct XxxView: View`）提取到 `component_specs`，在主页面用 `content_ref` 引用。
7. NavigationStack/NavigationSplitView 的 `.navigationTitle`、`.toolbar` 提取到 `navigation_bar`。
8. TabView 的 tab items 提取到 `tab_bar`。
9. 样式修饰符（.listStyle、.buttonStyle）记录在对应 element 的 `style` 字段。

## capabilities.json

```json
{
  "capabilities": [
    {
      "id": "network.urlsession",
      "capability": "URLSession",
      "source_refs": [],
      "runtime_behavior": "",
      "permission_or_entitlement": "",
      "feature_ids": [],
      "notes": ""
    }
  ]
}
```

## resources.json

```json
{
  "resources": [
    {
      "id": "",
      "type": "sf_symbol|asset_catalog|screenshot_crop|color|font|layout_metric",
      "ios_name": "",
      "usage": "bottom_tab",
      "screen_id": "",
      "used_by_features": [],
      "source_ref": "",
      "archive_path": "",
      "crop_ref": "",
      "fidelity_requirement": "exact_or_vector_equivalent"
    }
  ]
}
```

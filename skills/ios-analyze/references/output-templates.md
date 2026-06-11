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
      "id": "feature.news.home_feed",
      "level1": "新闻浏览",
      "level2": "首页信息流",
      "level3": "新闻列表加载与展示",
      "name": "首页新闻流",
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
      "id": "services.news.fetchArticles",
      "module_id": "services.news",
      "file": "",
      "type": "",
      "kind": "view|model|service|store|view_model|app|widget|extension|utility",
      "member": "",
      "inputs": [],
      "outputs": [],
      "side_effects": [],
      "used_by_features": [],
      "called_by": [],
      "migration_action": "model|service|store|arkui_component|platform_adapter|merge|delete_with_reason"
    }
  ]
}
```

## screens.json

```json
{
  "screens": [
    {
      "id": "screen.home.feed",
      "name": "首页信息流",
      "ios_view": "",
      "feature_ids": [],
      "route": "",
      "states": ["loading", "populated", "empty", "error"],
      "key_controls": [],
      "layout_notes": [],
      "resource_refs": [],
      "screenshot": "",
      "screenshot_required": false,
      "screenshot_reason": "",
      "source_refs": []
    }
  ]
}
```

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
      "id": "tab.home",
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

通过 harmony-generate skill 为 {{HARMONY_PROJECT}} 执行工程初始化和模块实现计划。

工作目录：{{WORKDIR}}

## 第一步：工程初始化

如果 {{HARMONY_PROJECT}}/ 目录不存在，执行以下初始化：

1. 从模板复制工程骨架：
   ```bash
   cp -r skills/harmony-generate/references/project-template/ {{HARMONY_PROJECT}}/
   ```

2. 替换占位符：
   - `{{HARMONY_PROJECT}}/AppScope/app.json5`：`bundleName` 改为 `com.example.{{HARMONY_PROJECT}}`（小写），`vendor` 改为 `example`
   - `{{HARMONY_PROJECT}}/AppScope/resources/base/element/string.json`：`app_name` 改为 `{{HARMONY_PROJECT}}`
   - `{{HARMONY_PROJECT}}/entry/src/main/resources/base/element/string.json`：`EntryAbility_label` 改为应用名，`EntryAbility_desc` 改为应用描述

3. 创建迁移目录：
   ```bash
   mkdir -p {{HARMONY_PROJECT}}/entry/src/main/ets/{models,models/news,models/settings,services,services/news,services/weather,services/rss,services/search,services/audio,services/nlp,services/personalization,services/sync,services/system,services/localapi,services/background,services/notification,services/card,services/ai,stores,pages,components,cards,fixtures,platform,support}
   ```

4. 删除模板的 `oh-package-lock.json5`（后续由 `ohpm install` 重新生成）

如果 {{HARMONY_PROJECT}}/ 已存在，跳过初始化步骤。

## 第二步：生成模块实现计划

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json

必须输出：
- output/harmony-generate/harmony模块实现计划.json
- output/harmony-generate/harmony全量实现追踪.md

## harmony模块实现计划.json 格式

```json
{
  "schema_version": "1.0",
  "project_name": "NewsMobileHarmony",
  "bundle_name": "com.example.newsmobileharmony",
  "target_sdk": "6.0.2(22)",
  "harmony_modules": [
    {
      "id": "models.news",
      "target_path": "entry/src/main/ets/models/news/",
      "ios_sources": ["NewsMobile/NewsMobile/Models/"],
      "ios_types": ["NewsArticle", "NewsSource"],
      "sub_stage": "core-services",
      "files_to_create": ["NewsArticle.ets", "NewsSource.ets"]
    }
  ],
  "stage_plan": {
    "core-services": {
      "description": "实现 models、services、stores",
      "target_paths": ["models/", "services/", "stores/"],
      "input_specs": ["specs/functions.json", "specs/features.json", "platform-adaptation/implementation-guidance.json"]
    },
    "pages-ui": {
      "description": "实现 pages、components",
      "target_paths": ["pages/", "components/"],
      "input_specs": ["specs/screens.json", "specs/features.json"]
    },
    "platform-capabilities": {
      "description": "实现 platform 适配层 + 更新 module.json5",
      "target_paths": ["platform/", "module.json5"],
      "input_specs": ["platform-adaptation/implementation-guidance.json", "platform-adaptation/risks.json"]
    },
    "integration-summary": {
      "description": "补缺口 + 构建",
      "target_paths": ["*"],
      "input_specs": ["specs/functions.json", "specs/features.json"]
    }
  }
}
```

## 约束

- 本阶段只做工程初始化和计划，不写业务代码。
- 计划必须按 iOS 模块和文件结构映射到 Harmony 目录。
- 每个 iOS 类型/函数都必须有 Harmony 处置：独立实现、合并、替代、删除并说明原因。
- 必须拆出后续子 agent 任务：核心服务、页面 UI、系统能力、集成汇总。
- 平台能力实现按 implementation-guidance.json 的 platform_modules 拆分。
- harmony_modules 中每个条目必须包含 `sub_stage` 字段，明确后续由哪个阶段负责。

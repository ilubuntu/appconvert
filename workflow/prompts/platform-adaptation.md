通过 platform-adaptation skill 生成平台能力适配策略。

工作目录：{{WORKDIR}}

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- skills/platform-adaptation/references/platform-capabilities.json

必须输出：
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/feature-adaptation.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json
- output/platform-adaptation/reports/平台能力适配摘要.md

约束：
- 不生成 Harmony 工程。
- 不做基础 UI 控件映射，例如 SwiftUI View/Button/List/TabView 到 ArkUI。
- 当前工程 capabilities.json 中每个能力都必须进入 capability-coverage.json 的 items 或 unmapped。
- high/medium priority feature 如果有关联 capability，必须进入 feature-adaptation.json。
- implementation-guidance.json 是后续 Harmony 代码生成的主输入，必须包含目标文件边界、public API 草案、权限/manifest/service/store 需求。
- risks.json 的每条风险必须有 recommended_action。
- Markdown 只写摘要，不作为后续模型唯一输入。

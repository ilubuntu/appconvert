通过 harmony-generate skill 汇总 {{HARMONY_PROJECT}} 的模块实现，并补齐缺口。

工作目录：{{WORKDIR}}

必须读取：
- output/harmony-generate/harmony模块实现计划.json
- output/harmony-generate/harmony全量实现追踪.md
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json

上下文预算规则：
- 禁止读取 `output/ios-analyze/archive/` 下的完整归档文件。
- 禁止整段打印或复述大型输入文件；只用 `rg`/`sed` 抽查相关章节和待修复项。
- 集成检查以 `output/ios-analyze/specs/functions.json` 为默认依据，不做完整归档逐函数扫描。
- `output/harmony-generate/harmony全量实现追踪.md` 只读取待修复、工程侧入口、截图页面追踪和构建验证相关行。

必须输出：
- {{HARMONY_PROJECT}}/
- output/harmony-generate/harmony全量实现追踪.md
- output/workflow/迁移状态.md
- 构建验证结果

约束：
- 对照 functions.json，检查每个 iOS 类型/函数是否已有 Harmony 去向。
- 对照 features.json，检查每个功能是否有页面、服务、状态和验收点。
- 对照 screens.json，检查每个主要页面是否可打开且有数据。
- 对照 capability-coverage.json，检查每个平台能力是否有工程侧入口。
- 发现缺口必须补代码或明确阻塞，不允许只写总结。
- 最终必须构建验证。
- 不修改签名文件或签名配置。

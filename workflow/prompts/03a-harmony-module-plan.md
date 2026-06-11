通过 harmony-generate skill 为 {{HARMONY_PROJECT}} 生成模块实现计划。

工作目录：{{WORKDIR}}

必须读取：
- output/01-ios-analyze/ios源码索引.md
- output/01-ios-analyze/ios模块结构.md
- output/01-ios-analyze/ios函数级清单.md
- output/01-ios-analyze/ios功能清单.md
- output/01-ios-analyze/ios界面清单.md
- output/02-ios-map/ios-harmony-kit映射.md
- output/01-ios-analyze/screenshots/png/

必须输出：
- output/03-harmony-generate/harmony模块实现计划.md
- output/03-harmony-generate/harmony全量实现追踪.md

约束：
- 本阶段只做计划和追踪表初始化，不大规模改 Harmony 代码。
- 计划必须按 iOS 模块和文件结构映射到 Harmony 目录。
- 每个 iOS 类型/函数都必须有 Harmony 处置：独立实现、合并、替代、删除并说明原因。
- 必须拆出后续子 agent 任务：核心服务、页面 UI、系统能力、集成汇总。

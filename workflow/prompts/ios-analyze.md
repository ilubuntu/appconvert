通过 ios-analyze skill 分析 {{IOS_PROJECT}} iOS 工程。

工作目录：{{WORKDIR}}

必须读取：
- {{IOS_PROJECT}}/

必须输出：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- output/ios-analyze/assets/ios/
- output/ios-analyze/assets/symbols/
- output/ios-analyze/assets/crops/
- output/ios-analyze/reports/ios工程分析.md
- output/ios-analyze/reports/ios功能摘要.md
- output/ios-analyze/reports/ios界面摘要.md

约束：
- 不生成 Harmony 工程。
- 不做 iOS 到 Harmony Kit 映射。
- 必须按 ios-analyze skill 的“内部编排流程”执行：工程索引 -> 模块结构 -> 功能清单 -> 轻量函数索引 -> 页面清单 -> 系统能力 -> 资源归档 -> 辅助截图 -> 人工摘要。
- features.json 是核心产物，必须按 一级功能 -> 二级功能 -> 三级功能 组织。
- 每个核心 feature 必须有稳定 id、source_refs、modules、screens、functions 或 capabilities 关联，以及 acceptance 验收标准。
- 后续模型消费 JSON specs，不消费 Markdown 表格；Markdown 只写给人审阅的摘要。
- 必须逐个读取 Swift 源文件，按 工程 -> Target/模块 -> 文件 -> 类型 -> 函数/属性 的颗粒度分析，但 functions.json 只保留轻量输入/输出/副作用/关联功能/迁移动作。
- JSON 之间必须通过稳定 id 互相引用，例如 feature id、module id、screen id、function id、capability id、resource id。
- 每个功能必须追溯到具体 iOS 文件、类型或函数；截图只是辅助证据，不是功能成立的前提。
- 必须归档 UI 资源，特别是底部 Tab 图标、SF Symbols、Assets.xcassets、关键颜色和截图裁剪；资源写入 resources.json，并关联 feature 或 screen。
- 截图计划必须从代码动态生成，写入 specs/screens.json；截图是辅助证据，只有需要补足视觉理解或后续 UI 对齐时才采集。采集截图不能人工点击。如需为截图模式修改 iOS 工程，必须保持正常启动路径不受影响。
- 如果实际采集了截图，生成 output/ios-analyze/screenshots/png/screenshots-manifest.json。
- 不能用 README 或脚本扫描结果代替源码级分析。

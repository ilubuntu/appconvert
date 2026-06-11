通过 harmony-generate skill 基于迁移规格生成或修改 {{HARMONY_PROJECT}}。

工作目录：{{WORKDIR}}

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json
- output/ios-analyze/screenshots/png/

必须输出：
- {{HARMONY_PROJECT}}/
- output/harmony-generate/harmony模块实现计划.json
- output/harmony-generate/harmony全量实现追踪.md
- 构建验证结果

约束：
- 不重新完整分析 iOS 工程。
- 必须先产出模块实现计划，再写代码。
- 每个 Harmony 模块必须追溯到 output/ios-analyze/specs/modules.json。
- 每个 Harmony 文件必须追溯到 output/ios-analyze/specs/functions.json。
- 每个核心函数必须追溯到 output/ios-analyze/specs/functions.json。
- 每个页面必须追溯到 output/ios-analyze/specs/features.json 和 output/ios-analyze/specs/screens.json。
- 每个系统能力必须追溯到 output/platform-adaptation/implementation-guidance.json。
- 真实数据接入属于本阶段，不允许单独拆成后置阶段。
- 新闻流必须真实数据优先，固定样例数据 只作为网络失败、解析失败或截图稳定性的兜底。
- 必须实现 RSS/Atom 网络请求和 XML 解析的可运行链路；不能只写 `NewsFixtures` 或 `example.com` 假数据。
- UI 必须以 output/ios-analyze/screenshots/png/ 的截图为主要视觉约束。
- 需要复刻信息层级、字号、颜色、卡片、间距、圆角、顶部导航、底部 Tab、空态和有数据态。
- 如果 ArkUI 原生控件达不到 iOS 截图效果，优先写自定义 ArkUI 组件复刻。
- 如果必须使用 HarmonyOS 设计替代，必须在 output/harmony-generate/harmony全量实现追踪.md 记录替代原因、替代组件和保留的交互语义。
- 首屏必须有真实数据加载入口和 固定样例数据兜底数据。
- 必须构建验证。
- 不修改签名文件或签名配置。

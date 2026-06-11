通过 harmony-generate skill 实现 {{HARMONY_PROJECT}} 的页面和组件 UI。

工作目录：{{WORKDIR}}

必须读取：
- output/harmony-generate/harmony模块实现计划.md
- output/ios-analyze/ios界面清单.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/screenshots/png/
- output/harmony-generate/harmony全量实现追踪.md

上下文预算规则：
- 禁止读取 `output/ios-analyze/archive/` 下的完整归档文件。
- 禁止整段打印或复述大型输入文件；只用 `rg`/`sed` 读取本阶段相关章节。
- `output/harmony-generate/harmony全量实现追踪.md` 只允许按 `截图页面追踪`、Views、Components 相关行读取，不要整文件展开。
- 本阶段只处理页面和组件，不重写核心服务。

必须输出：
- {{HARMONY_PROJECT}}/entry/src/main/ets/pages/
- {{HARMONY_PROJECT}}/entry/src/main/ets/components/
- output/harmony-generate/harmony全量实现追踪.md
- 阶段变更摘要；本阶段不跑完整 `assembleHap`，构建统一交给 `harmony-integration-summary`

约束：
- UI 以 iOS 截图为主要约束，目标是尽量 1:1 复刻信息层级、字号、颜色、卡片、间距、圆角、顶部导航、底部 Tab、空态和有数据态。
- 不能只写简单框架 UI；每个页面必须有真实内容、交互和状态。
- 如果 ArkUI 原生控件无法达成一致，优先写自定义组件。
- 如果必须采用 HarmonyOS 设计替代，必须记录替代原因、替代组件和保留的交互语义。
- 不重新设计服务层数据结构，除非发现页面无法消费，并必须记录原因。
- 不执行完整 hvigor 构建；如需检查，只做快速文件/导入级自查并记录。
- 不修改签名文件或签名配置。

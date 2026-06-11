通过 harmony-generate skill 实现 {{HARMONY_PROJECT}} 的页面和组件 UI。

工作目录：{{WORKDIR}}

必须读取：
- output/03-harmony-generate/harmony模块实现计划.md
- output/01-ios-analyze/ios界面清单.md
- output/01-ios-analyze/ios功能清单.md
- output/01-ios-analyze/screenshots/png/
- output/03-harmony-generate/harmony全量实现追踪.md

必须输出：
- {{HARMONY_PROJECT}}/entry/src/main/ets/pages/
- {{HARMONY_PROJECT}}/entry/src/main/ets/components/
- output/03-harmony-generate/harmony全量实现追踪.md
- 构建验证结果

约束：
- UI 以 iOS 截图为主要约束，目标是尽量 1:1 复刻信息层级、字号、颜色、卡片、间距、圆角、顶部导航、底部 Tab、空态和有数据态。
- 不能只写简单框架 UI；每个页面必须有真实内容、交互和状态。
- 如果 ArkUI 原生控件无法达成一致，优先写自定义组件。
- 如果必须采用 HarmonyOS 设计替代，必须记录替代原因、替代组件和保留的交互语义。
- 不重新设计服务层数据结构，除非发现页面无法消费，并必须记录原因。
- 不修改签名文件或签名配置。

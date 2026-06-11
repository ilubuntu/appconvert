通过 harmony-visual-verify skill、build-harmony-project skill 和必要的 UI 预览能力验收 {{HARMONY_PROJECT}}。

工作目录：{{WORKDIR}}

必须读取：
- {{HARMONY_PROJECT}}/
- output/03-harmony-generate/harmony全量实现追踪.md
- output/01-ios-analyze/ios界面清单.md
- output/01-ios-analyze/screenshots/png/

必须输出：
- 构建结果
- Harmony 截图产物
- output/04-harmony-visual-verify/界面对齐.md
- UI/UX 修复说明
- 更新后的 output/03-harmony-generate/harmony全量实现追踪.md
- 更新后的 output/00-workflow/迁移状态.md

约束：
- 这是视觉验收阶段，不是单纯构建阶段。
- 必须读取 iOS 截图并逐页对比，不能只看代码或构建结果。
- 必须覆盖 output/01-ios-analyze/ios界面清单.md 中列出的主要页面。
- 必须对比信息层级、页面结构、导航、Tab、卡片、字号、字重、颜色、图标、间距、圆角、空态/加载态/有数据态。
- 底部 Tab 必须有图标+文字或等价的 Harmony 高保真替代，不允许只有裸文字。
- 差异明显时必须修 ArkUI 实现并重新构建。
- 如果 ArkUI 原生控件无法一致，使用自定义组件或 HarmonyOS 替代设计，并在 output/04-harmony-visual-verify/界面对齐.md 记录原因。
- 不扩大迁移范围。
- 不删除卡片、云同步、后台刷新、本地 API、NLP、AI 后端等配套服务能力入口。
- 不修改签名文件或签名配置。
- 构建失败必须给出具体错误和下一步。

通过 harmony-generate skill 实现 {{HARMONY_PROJECT}} 的核心模型、服务和状态层。

工作目录：{{WORKDIR}}

必须读取：
- output/harmony-generate/harmony模块实现计划.md
- output/ios-analyze/ios源码索引.md
- output/ios-analyze/ios模块结构.md
- output/ios-analyze/ios函数级清单.md
- output/ios-analyze/ios功能清单.md
- output/ios-map/ios-harmony-kit映射.md

上下文预算规则：
- 禁止读取 `output/ios-analyze/archive/` 下的完整归档文件。
- 禁止整段打印或复述大型输入文件；只用 `rg`/`sed` 读取本阶段相关章节。
- `output/harmony-generate/harmony全量实现追踪.md` 只允许按 `类型级处置表`、`函数级处置表` 中 Models、Services、Stores 相关行读取，不要整文件展开。
- 本阶段只处理核心服务，不处理页面 UI 和视觉验收。

必须输出：
- {{HARMONY_PROJECT}}/entry/src/main/ets/models/
- {{HARMONY_PROJECT}}/entry/src/main/ets/services/
- {{HARMONY_PROJECT}}/entry/src/main/ets/stores/
- output/harmony-generate/harmony全量实现追踪.md
- 阶段变更摘要；本阶段不跑完整 `assembleHap`，构建统一交给 `harmony-integration-summary`

约束：
- 不重新设计 UI。
- 不删除现有页面入口。
- 新闻、搜索、收藏、设置、订阅源、趋势、聚类、TTS/Web/通知/定位/后台/卡片/本地 API 相关数据接口都必须有对应模型或服务。
- 每个新增 ArkTS 文件必须在追踪表中记录对应 iOS 文件、类型和函数。
- 真实数据接入属于本阶段，固定样例数据 只能作为兜底。
- 不执行完整 hvigor 构建；如需检查，只做快速文件/导入级自查并记录。
- 不修改签名文件或签名配置。

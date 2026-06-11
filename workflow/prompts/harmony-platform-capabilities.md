通过 harmony-generate skill 实现 {{HARMONY_PROJECT}} 的平台能力适配层。

工作目录：{{WORKDIR}}

必须读取：
- output/harmony-generate/harmony模块实现计划.md
- output/ios-analyze/ios特性清单.md
- output/ios-map/ios-harmony-kit映射.md
- output/harmony-generate/harmony全量实现追踪.md

上下文预算规则：
- 禁止读取 `output/ios-analyze/archive/` 下的完整归档文件。
- 禁止整段打印或复述大型输入文件；只用 `rg`/`sed` 读取本阶段相关章节。
- `output/harmony-generate/harmony全量实现追踪.md` 只允许按平台能力相关行读取，不要整文件展开。
- 本阶段只处理平台适配层，不重写页面 UI 和核心业务服务。

必须输出：
- {{HARMONY_PROJECT}}/entry/src/main/ets/platform/
- {{HARMONY_PROJECT}}/entry/src/main/module.json5
- output/harmony-generate/harmony全量实现追踪.md
- 阶段变更摘要；本阶段不跑完整 `assembleHap`，构建统一交给 `harmony-integration-summary`

约束：
- 覆盖 Web、TTS、通知、定位、后台刷新、Widget/Card、云同步、本地 API、网络权限、持久化等能力。
- 需要外部配置的能力，工程侧入口和接口必须实现，不能直接标记不做。
- 权限变更必须最小化，并在追踪表中记录。
- 不执行完整 hvigor 构建；如需检查，只做快速文件/导入级自查并记录。
- 不修改签名文件或签名配置。

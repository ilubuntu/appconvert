通过 harmony-generate skill 实现 {{HARMONY_PROJECT}} 的平台能力适配层。

工作目录：{{WORKDIR}}

必须读取：
- output/03-harmony-generate/harmony模块实现计划.md
- output/01-ios-analyze/ios特性清单.md
- output/02-ios-map/ios-harmony-kit映射.md
- output/03-harmony-generate/harmony全量实现追踪.md

必须输出：
- {{HARMONY_PROJECT}}/entry/src/main/ets/platform/
- {{HARMONY_PROJECT}}/entry/src/main/module.json5
- output/03-harmony-generate/harmony全量实现追踪.md
- 构建验证结果

约束：
- 覆盖 Web、TTS、通知、定位、后台刷新、Widget/Card、云同步、本地 API、网络权限、持久化等能力。
- 需要外部配置的能力，工程侧入口和接口必须实现，不能直接标记不做。
- 权限变更必须最小化，并在追踪表中记录。
- 不修改签名文件或签名配置。

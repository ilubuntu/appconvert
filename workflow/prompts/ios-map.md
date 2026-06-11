通过 ios-map skill 生成 iOS 到 HarmonyOS NEXT 能力映射。

工作目录：{{WORKDIR}}

必须读取：
- output/ios-analyze/ios模块结构.md
- output/ios-analyze/ios功能清单.md
- output/ios-analyze/ios特性清单.md

必须输出：
- output/ios-map/ios-harmony-kit映射.md

约束：
- 不读取完整 iOS 源码，除非文档证据不足。
- 不生成 Harmony 工程。
- 所有能力都进入迁移目标。
- 每项能力只能标记为 平台直迁、等价替代 或 配套服务。

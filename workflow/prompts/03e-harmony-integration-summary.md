通过 harmony-generate skill 汇总 {{HARMONY_PROJECT}} 的模块实现，并补齐缺口。

工作目录：{{WORKDIR}}

必须读取：
- output/03-harmony-generate/harmony模块实现计划.md
- output/03-harmony-generate/harmony全量实现追踪.md
- output/01-ios-analyze/ios源码索引.md
- output/01-ios-analyze/ios函数级清单.md
- output/01-ios-analyze/ios功能清单.md
- output/01-ios-analyze/ios界面清单.md
- output/02-ios-map/ios-harmony-kit映射.md

必须输出：
- {{HARMONY_PROJECT}}/
- output/03-harmony-generate/harmony全量实现追踪.md
- output/00-workflow/迁移状态.md
- 构建验证结果

约束：
- 对照 ios函数级清单，检查每个 iOS 类型/函数是否已有 Harmony 去向。
- 对照 ios功能清单，检查每个功能是否有页面、服务、状态和验收点。
- 对照 ios界面清单，检查每个主要页面是否可打开且有数据。
- 发现缺口必须补代码或明确阻塞，不允许只写总结。
- 最终必须构建验证。
- 不修改签名文件或签名配置。

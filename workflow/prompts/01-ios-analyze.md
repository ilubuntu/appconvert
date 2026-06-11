通过 ios-analyze skill 分析 {{IOS_PROJECT}} iOS 工程。

工作目录：{{WORKDIR}}

必须读取：
- {{IOS_PROJECT}}/

必须输出：
- output/01-ios-analyze/ios源码索引.md
- output/01-ios-analyze/ios模块结构.md
- output/01-ios-analyze/ios函数级清单.md
- output/01-ios-analyze/ios功能清单.md
- output/01-ios-analyze/ios界面清单.md
- output/01-ios-analyze/ios特性清单.md
- output/01-ios-analyze/screenshots/png/screenshots-manifest.json

约束：
- 不生成 Harmony 工程。
- 不做 iOS 到 Harmony Kit 映射。
- 截图不能人工点击。
- 如需为截图模式修改 iOS 工程，必须保持正常启动路径不受影响。
- 必须逐个读取 Swift 源文件，按 工程 -> Target/模块 -> 文件 -> 类型 -> 函数/属性 的颗粒度分析。
- 每个功能必须追溯到具体 iOS 文件、类型、函数和截图。
- 不能用 README 或脚本扫描结果代替源码级分析。

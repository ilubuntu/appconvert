# Output Directory Layout

`output/` 按迁移阶段存放产物，不再把文件直接散在根目录。

## 00-workflow

- `迁移状态.md`：当前阶段、已完成项、下一步和阻塞项。
- `rendered-prompts/`：workflow runner 临时渲染的 prompt，可再生成。

## 01-ios-analyze

iOS 工程深度分析阶段产物：

- `ios源码索引.md`
- `ios模块结构.md`
- `ios函数级清单.md`：轻量版，按“模块 -> 函数 -> 输入 -> 输出/副作用”组织，作为后续 agent 默认输入。
- `ios功能清单.md`
- `ios界面清单.md`
- `ios特性清单.md`
- `screenshots/png/`
- `archive/ios函数级清单.full.md`：完整审计底账，只在查证具体文件时按需打开。

## 02-ios-map

iOS 能力到 HarmonyOS NEXT 能力映射：

- `ios-harmony-kit映射.md`

## 03-harmony-generate

Harmony 工程生成、模块实现计划和实现追踪：

- `harmony模块实现计划.md`
- `harmony全量实现追踪.md`

## 04-harmony-visual-verify

Harmony 视觉验收和截图对齐：

- `界面对齐.md`
- `screenshots/`

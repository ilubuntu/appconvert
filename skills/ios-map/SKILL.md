---
name: ios-map
description: 当 iOS 工程结构、功能和 Apple 能力使用情况已经分析完成后使用。本 skill 负责把 iOS framework、entitlement、权限、生命周期行为和 API 全量映射到 HarmonyOS NEXT Kit、等价实现策略和配套服务方案。它不检查 UI 截图，也不生成鸿蒙工程文件。
---

# iOS 能力到 HarmonyOS NEXT 映射

## 职责边界

输入：

- `output/ios-analyze/ios功能清单.md`
- `output/ios-analyze/ios模块结构.md`
- `output/ios-analyze/ios特性清单.md`
- 必要时读取 iOS 源码证据

输出：

- `output/ios-map/ios-harmony-kit映射.md`
- 能力迁移决策
- 配套服务和等价替代清单

不要在本 skill 中生成 ArkTS 页面或鸿蒙工程文件。

## 工作流

1. 先读取 `output/ios-analyze/ios特性清单.md`。
2. 按行为分类 iOS 能力：UI、网络、存储、权限、通知、定位、Web、媒体、ML、Widget、后台、云同步。
3. 为每个能力识别 HarmonyOS NEXT Kit 或实现方向。
4. 将每项标记为 `平台直迁`、`等价替代` 或 `配套服务`。
5. 写出可被鸿蒙工程生成 skill 消费的具体实现备注。

## 输出格式

```md
# iOS 到 HarmonyOS NEXT 能力映射

| iOS 能力 | 使用位置 | 行为 | HarmonyOS NEXT 方向 | 实现类型 | 实现备注 |
| --- | --- | --- | --- | --- | --- |
```

## 决策规则

- 如果 Harmony 有直接平台 Kit，标记为 `平台直迁`。
- 如果 iOS 能力依赖 Apple 专有实现但产品行为可以在鸿蒙侧复现，标记为 `等价替代`。
- 如果需要云服务、卡片基础设施、后台任务策略或服务端配合，标记为 `配套服务`，但仍然必须写出实现方案。
- 不允许把功能排除到当前迁移目标之外。全量迁移目标下，每项 iOS 能力都要有鸿蒙侧落点。
- 保留源码证据，确保每条映射都能追溯到 iOS 工程分析产物。

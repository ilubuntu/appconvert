---
name: harmony-visual-verify
description: 当 HarmonyOS NEXT 迁移工程已经生成后使用。本 skill 负责用 iOS 截图和 Harmony 截图逐页对比 UX、布局、颜色、字号、图标、间距、状态和交互，还原不足时直接修复 ArkUI 实现，并输出界面对齐报告。它不是单纯构建验收。
---

# HarmonyOS NEXT 视觉验收

## 职责边界

输入：

- `NewsMobileHarmony/`
- `output/01-ios-analyze/ios界面清单.md`
- `output/01-ios-analyze/screenshots/png/`
- `output/03-harmony-generate/harmony全量实现追踪.md`

输出：

- Harmony 截图产物
- `output/04-harmony-visual-verify/界面对齐.md`
- 修复后的 ArkUI 页面和组件
- 构建结果
- 更新后的 `output/03-harmony-generate/harmony全量实现追踪.md`
- 更新后的 `output/00-workflow/迁移状态.md`

## 工作流

1. 读取 `output/01-ios-analyze/ios界面清单.md`，列出必须对齐的每个页面。
2. 读取对应 iOS 截图，不只读文字描述。
3. 生成或采集 Harmony 页面截图。
4. 对每个页面逐项比较：
   - 信息层级
   - 页面结构
   - 顶栏/导航
   - Tab 样式
   - 卡片样式
   - 字号和字重
   - 颜色和状态色
   - 图标语义
   - 间距和圆角
   - 空态/加载态/有数据态
5. 如果 ArkUI 原生控件无法达到 iOS 效果，优先使用自定义 ArkUI 组件复刻。
6. 如果必须采用 HarmonyOS 设计替代，写清楚替代原因、替代组件和保留的交互语义。
7. 修复页面后重新构建。
8. 输出 `output/04-harmony-visual-verify/界面对齐.md`。

## 验收规则

- 不能只说构建通过。
- 不能只看代码，不看截图。
- 不能只优化单个 Tab 或单个控件；必须逐页对齐。
- 不能因为 ArkUI 原生 Tab 只有文字就接受低保真结果；需要自定义图标+文字 Tab 或合理的 Harmony 替代方案。
- 每一页都必须记录 iOS 截图路径、Harmony 截图路径、差异、修复项和剩余差异。
- UI 差异明显时必须继续修，不应把 `output/04-harmony-visual-verify/界面对齐.md` 写成通过。

## `output/04-harmony-visual-verify/界面对齐.md` 格式

```md
# 界面对齐

## 页面：Home

- iOS 截图：
- Harmony 截图：
- 对齐结论：通过 / 待修复
- 主要差异：
- 已修复：
- 剩余差异：
- 如果使用 Harmony 替代设计：

## 页面：...
```

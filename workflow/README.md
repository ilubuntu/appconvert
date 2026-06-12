# iOS to HarmonyOS NEXT Workflow

4 个阶段，每个阶段对应一个独立 skill：

1. **ios-analyze** — 深度分析 iOS 工程，输出 JSON specs
2. **platform-adaptation** — iOS 平台能力 → HarmonyOS Kit 适配策略
3. **harmony-generate** — 从模板创建工程 + 按模块生成完整 ArkTS 代码 + 构建
4. **harmony-visual-verify** — 构建验证 + 视觉对齐

每个 skill 通过 `opencode run` 或其他 agent runner 直接调用，不依赖 workflow runner。

目录结构：

- `skills/` — 可复用的迁移 skill
- `output/` — 生成的 specs、适配产物、追踪表
- `方案/` — 迁移方案、诉求、agent 设计文档
- `NewsMobile/` — 源 iOS 工程
- `NewsMobileHarmony/` — 目标 HarmonyOS NEXT 工程

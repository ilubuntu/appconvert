# iOS 到 HarmonyOS NEXT 迁移 Agent 设计

## 结论

skill 是操作手册，agent 是执行单元。

在这个迁移项目里：

- skill 负责沉淀"怎么做"。
- agent 配置负责定义"是谁"：身份、默认提示词、工具边界和模型。
- agent runner（如 opencode run / codex exec 等工具）负责"跑起来"。
- 多个阶段之间只通过本地文件交接。

## Skill 和 Agent 的区别

| 对比项 | Skill | Agent |
| --- | --- | --- |
| 本质 | 可复用操作说明、模板、脚本和约束 | 一次具体任务的执行者 |
| 生命周期 | 常驻在本地 skill 目录，可反复使用 | 一次任务启动，完成后关闭 |
| 调用方式 | 用户或任务触发 skill，工具读取 `SKILL.md` | 通过 agent runner（如 opencode run / codex exec 等工具）启动一个阶段 |
| 上下文 | 只在触发时读取相关说明 | 可以选择是否继承当前上下文 |
| 适合做什么 | 规范流程、工具用法、输出格式 | 长链路拆分、并行执行、隔离上下文 |
| 文件输出 | skill 本身不执行，除非 agent 按 skill 去做 | agent 执行后产出/修改文件 |

## Agent 配置和启动方式

### 1. 定义身份：`[agents.*]`

`[agents.*]` 用来定义可复用 agent 身份。

本项目模板：

- `workflow/agents.config.toml`

它定义：

- description
- prompt
- tools
- model

这回答"这个 agent 是谁"。

### 2. 启动执行：agent runner

通过 agent runner（如 opencode run / codex exec 等工具）启动阶段执行。

单阶段示例：

```bash
# opencode
opencode run --dir /Users/bb/work/appConvert --agent harmony-generate < workflow/prompts/harmony-generate.md

# codex
codex exec -C /Users/bb/work/appConvert -p harmony-generate < workflow/prompts/harmony-generate.md
```

这回答"怎么跑起来"。

### 3. 编排多个阶段：workflow runner

本项目用 runner 显式串起多个阶段执行：

- `workflow/ios-to-harmony.workflow.yaml`
- `workflow/run_ios_to_harmony.py`
- `workflow/prompts/`
- `workflow/profiles/`

干跑验证：

```bash
python3 workflow/run_ios_to_harmony.py --dry-run
```

本项目建议：

- 用 `[agents.*]` 保存 agent 身份。
- 通过 agent runner 启动阶段。
- 用 `workflow/run_ios_to_harmony.py` 串起完整流程。

## 调用方式

## 用户真正应该怎么说

用户不应该说"创建 agent"或"启动子 agent"。面向用户的表达应该是：

```text
通过 ios-to-harmony-workflow 执行 <iOS工程目录> 的 iOS 工程转换，输出到 <Harmony工程目录>
```

示例：

```text
通过 ios-to-harmony-workflow 执行 /Users/bb/work/appConvert/NewsMobile 的 iOS 工程转换，输出到 /Users/bb/work/appConvert/NewsMobileHarmony
```

内部可以用 runner 串行跑多个阶段，也可以在支持时使用命名 agent；这是实现细节，不暴露给用户。

### 调用 Skill

用户可以直接说：

```text
使用 ios-analyze skill 分析 NewsMobile。
```

工具会读取：

```text
skills/ios-analyze/SKILL.md
```

然后按 skill 的规则在当前上下文里执行。

### 调用 Agent 阶段

调试或开发工作流时，才需要显式指定某个阶段。推荐通过 runner 启动：

```bash
python3 workflow/run_ios_to_harmony.py \
  --execute \
  --from-stage harmony-module-plan \
  --to-stage harmony-integration-summary
```

### 调试用调用语句

```text
python3 workflow/run_ios_to_harmony.py --execute --from-stage harmony-module-plan --to-stage harmony-integration-summary
```

执行完整工作流时，runner 读取：

- `output/workflow/迁移状态.md`
- `agent设计.md`
- `多agent迁移工作流.md`

然后 runner 根据 workflow 文件启动对应阶段。

也可以指定阶段：

```text
执行 Harmony 模块实现计划阶段。
```

或：

```text
只执行平台能力适配阶段。
```

## 上下文策略

### 默认策略

每个阶段默认不继承完整对话上下文。

等价策略：

```text
fork_context: false
```

原因：

- 迁移链路长。
- 当前对话历史会越来越大。
- 阶段只需要输入文件，不需要完整聊天记录。

### 允许继承上下文的情况

只有短任务可以考虑继承：

- 临时核对刚刚生成的一个文件。
- 修复刚刚出现的一条构建错误。
- 不值得重新写输入契约的小任务。

对于完整迁移阶段，不使用完整上下文继承。

## Agent 列表

## 1. 迁移总控 Runner

### 职责

- 读取 `output/workflow/迁移状态.md`。
- 判断当前阶段。
- 检查输入文件是否齐全。
- 生成阶段 prompt。
- 通过 agent runner 启动阶段执行。
- 验收阶段输出。
- 更新 `output/workflow/迁移状态.md`。

### 使用 Skill

- 可读取 `多agent迁移工作流.md`。
- 可读取本文件。
- 不需要专门业务 skill。

### 允许读

- `output/workflow/迁移状态.md`
- `agent设计.md`
- `多agent迁移工作流.md`
- 各阶段输出文档

### 允许写

- `output/workflow/迁移状态.md`
- 阶段总结文档

### 不应该做

- 不直接重写 Harmony 工程。
- 不完整读取 iOS 源码。
- 不把所有上下文传给阶段执行进程。

### 用户调用

```text
python3 workflow/run_ios_to_harmony.py --execute
```

## 2. iOS 工程分析 Agent

### 职责

- 按工程、Target/模块、文件、类型、函数/属性颗粒度分析 iOS 工程结构。
- 生成 JSON specs：project.json、modules.json、features.json、functions.json、screens.json、capabilities.json、resources.json。
- 辅助采集 iOS 截图。

### 使用 Skill

- `ios-analyze`

### 输入

- `NewsMobile/`

### 输出

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `output/ios-analyze/reports/ios工程分析.md`
- `output/ios-analyze/reports/ios功能摘要.md`
- `output/ios-analyze/reports/ios界面摘要.md`
- `output/ios-analyze/assets/`（资源归档）
- `output/ios-analyze/screenshots/png/screenshots-manifest.json`（如采集截图）

### 允许写

- iOS 分析 JSON specs 和 reports。
- iOS 截图产物。
- 为截图模式做必要 iOS 代码改动。

### 不允许做

- 不生成 Harmony 工程。
- 不做平台能力适配。
- 不人工点击模拟器截图。

### 调用模板

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 ios-analyze skill 分析 NewsMobile iOS 工程。

必须读取：
- NewsMobile/

必须输出：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- output/ios-analyze/reports/ios工程分析.md
- output/ios-analyze/reports/ios功能摘要.md
- output/ios-analyze/reports/ios界面摘要.md

约束：
- 不生成 Harmony 工程。
- 不做平台能力适配。
- 截图不能人工点击。
- 必须按 ios-analyze skill 的内部编排流程执行。
- features.json 是核心产物，必须按三级功能结构组织。
- JSON 之间必须通过稳定 id 互相引用。
- 必须逐文件读取 Swift 源码，不能只用 README 或扫描结果总结。
```

## 3. 平台能力适配 Agent

### 职责

- 读取 iOS 分析产出的 JSON specs 和平台能力参考库。
- 生成能力覆盖、feature 适配策略、实现指导和风险清单。

### 使用 Skill

- `platform-adaptation`

### 输入

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`
- `skills/platform-adaptation/references/platform-capabilities.json`

### 输出

- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `output/platform-adaptation/reports/平台能力适配摘要.md`

### 允许写

- `output/platform-adaptation/` 下所有 JSON 和 reports。

### 不允许做

- 不生成 Harmony 工程。
- 不做基础 UI 控件映射（SwiftUI View/Button/List/TabView 到 ArkUI）。
- 不把能力排除出迁移目标。
- 不重新完整分析 iOS 源码，除非 JSON specs 证据不足。

### 调用模板

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 platform-adaptation skill 生成平台能力适配策略。

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/screens.json
- output/ios-analyze/specs/capabilities.json
- output/ios-analyze/specs/resources.json
- skills/platform-adaptation/references/platform-capabilities.json

必须输出：
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/feature-adaptation.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json
- output/platform-adaptation/reports/平台能力适配摘要.md

约束：
- 不生成 Harmony 工程。
- 不做基础 UI 控件映射。
- capabilities.json 中每个能力都必须进入 capability-coverage.json 的 items 或 unmapped。
- high/medium priority feature 有关联 capability 时必须进入 feature-adaptation.json。
- implementation-guidance.json 是后续 Harmony 代码生成的主输入，必须包含目标文件边界和 public API 草案。
- risks.json 每条风险必须有 recommended_action。
```

## 4. Harmony 工程初始化与模块计划 Agent

### 职责

- 如果目标 Harmony 工程不存在，从 `skills/harmony-generate/references/project-template/` 复制模板、替换占位符（bundleName、vendor、app_name）、创建迁移目录、删除 oh-package-lock.json5。
- 根据 iOS JSON specs 和平台能力适配产物拆分 Harmony 实现任务。
- 生成 `output/harmony-generate/harmony模块实现计划.json`。
- 初始化或更新 `output/harmony-generate/harmony全量实现追踪.md`。
- 明确后续核心服务、页面 UI、平台能力、集成汇总 agent 的输入和验收点。

### 使用 Skill

- `harmony-generate`

### 输入

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/screens.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `skills/harmony-generate/references/project-template/`

### 输出

- `NewsMobileHarmony/`（工程骨架，如果不存在）
- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`

### 允许写

- `NewsMobileHarmony/`（工程初始化）
- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`

### 不允许做

- 不重新完整分析 iOS 工程。
- 不写业务代码（models/services/stores/pages/components/platform）。
- 不跳过任何 iOS 类型/函数。
- 不修改签名文件或签名配置。

### 调用模板

```text
工作目录：/Users/bb/work/appConvert

任务：
使用 harmony-generate skill 为 NewsMobileHarmony 生成模块实现计划。

必须读取：
- output/ios-analyze/specs/project.json
- output/ios-analyze/specs/modules.json
- output/ios-analyze/specs/functions.json
- output/ios-analyze/specs/features.json
- output/ios-analyze/specs/screens.json
- output/platform-adaptation/capability-coverage.json
- output/platform-adaptation/implementation-guidance.json
- output/platform-adaptation/risks.json

必须输出：
- output/harmony-generate/harmony模块实现计划.json
- output/harmony-generate/harmony全量实现追踪.md

约束：
- 不重新完整分析 iOS 工程。
- 每个 iOS 类型/函数都必须有 Harmony 处置。
- 本阶段不做大规模代码实现。
- 不修改签名配置。
```

## 5. Harmony 核心服务 Agent

### 职责

- 实现 `models/`、`services/`、`stores/`。
- 接入真实数据加载、解析、搜索、收藏、设置、订阅源、趋势、聚类和 fixture 数据兜底。
- 更新实现追踪表。

### 使用 Skill

- `harmony-generate`
- `build-harmony-project`

### 输入

- `output/harmony-generate/harmony模块实现计划.json`
- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/platform-adaptation/implementation-guidance.json`

### 输出

- `NewsMobileHarmony/entry/src/main/ets/models/`
- `NewsMobileHarmony/entry/src/main/ets/services/`
- `NewsMobileHarmony/entry/src/main/ets/stores/`
- `output/harmony-generate/harmony全量实现追踪.md`

## 6. Harmony 页面 UI Agent

### 职责

- 实现 `pages/` 和 `components/`。
- 按 iOS 截图复刻主 Tab、首页、详情、搜索、收藏、设置等页面。
- 保证页面不是空壳，有数据、有状态、有交互。

### 使用 Skill

- `harmony-generate`
- `build-harmony-project`

### 输入

- `output/harmony-generate/harmony模块实现计划.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/screenshots/png/`
- `output/harmony-generate/harmony全量实现追踪.md`

### 输出

- `NewsMobileHarmony/entry/src/main/ets/pages/`
- `NewsMobileHarmony/entry/src/main/ets/components/`
- `output/harmony-generate/harmony全量实现追踪.md`

## 7. Harmony 平台能力 Agent

### 职责

- 按 `implementation-guidance.json` 的 platform_modules 实现 Web、TTS、通知、定位、后台刷新、Widget/Card、云同步、本地 API、权限、持久化等平台适配层。
- 对需要外部配置的能力提供工程侧入口和配置说明。

### 使用 Skill

- `harmony-generate`
- `build-harmony-project`

### 输入

- `output/harmony-generate/harmony模块实现计划.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/feature-adaptation.json`
- `output/platform-adaptation/implementation-guidance.json`
- `output/platform-adaptation/risks.json`
- `output/harmony-generate/harmony全量实现追踪.md`

### 输出

- `NewsMobileHarmony/entry/src/main/ets/platform/`
- `NewsMobileHarmony/entry/src/main/module.json5`
- `output/harmony-generate/harmony全量实现追踪.md`

## 8. Harmony 集成汇总 Agent

### 职责

- 对照 `output/ios-analyze/specs/functions.json` 检查每个 iOS 类型/函数的 Harmony 去向。
- 对照 `output/ios-analyze/specs/features.json` 检查页面、服务、状态和验收点。
- 补齐缺口并构建验证。

### 使用 Skill

- `harmony-generate`
- `build-harmony-project`

### 输入

- `output/harmony-generate/harmony模块实现计划.json`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/screens.json`
- `output/platform-adaptation/capability-coverage.json`
- `output/platform-adaptation/implementation-guidance.json`

### 输出

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/workflow/迁移状态.md`
- 构建结果

## 9. Harmony 视觉验收 Agent

### 职责

- 构建 Harmony 工程。
- 运行或预览 UI。
- 对照 iOS 截图和追踪表修复问题。

### 使用 Skill

- `build-harmony-project`
- `harmonyos-live-preview`
- `harmony-visual-verify`

### 输入

- `NewsMobileHarmony/`
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/screenshots/png/`

### 输出

- 构建结果。
- Harmony 截图或预览结果。
- 差异记录。
- 修复后的工程。
- 更新后的 `output/harmony-generate/harmony全量实现追踪.md`。
- 更新后的 `output/workflow/迁移状态.md`。

### 允许写

- `NewsMobileHarmony/entry/src/main/ets/`
- 验收截图产物。
- `output/harmony-generate/harmony全量实现追踪.md`
- `output/workflow/迁移状态.md`

### 不允许做

- 不扩大迁移范围。
- 不删除配套服务能力入口。
- 不修改签名配置。

### 调用模板

```text
工作目录：/Users/bb/work/appConvert

任务：
构建并验收 NewsMobileHarmony，对照 iOS 截图和追踪表修复问题。

必须读取：
- NewsMobileHarmony/
- output/harmony-generate/harmony全量实现追踪.md
- output/ios-analyze/specs/screens.json
- output/ios-analyze/screenshots/png/

必须输出：
- 构建结果
- 差异记录
- 修复说明
- 更新后的 output/harmony-generate/harmony全量实现追踪.md
- 更新后的 output/workflow/迁移状态.md

约束：
- 不扩大迁移范围。
- 不删除配套服务能力入口。
- 构建失败必须给出具体错误和下一步。
```

## 推荐编排方式

runner 执行下一阶段时：

1. 读取 `output/workflow/迁移状态.md`。
2. 根据当前阶段选择 workflow stage。
3. 渲染对应 prompt 文件。
4. 通过 agent runner 启动阶段执行。
5. 阶段执行完成后检查输出文件。
6. 更新 `output/workflow/迁移状态.md`。

## 当前建议

当前状态已有 iOS 分析 JSON specs（`output/ios-analyze/specs/*.json`），下一步应运行平台能力适配阶段。

下一次执行时应运行：

```text
平台能力适配阶段
```

目标：

- 生成 `output/platform-adaptation/capability-coverage.json`。
- 生成 `output/platform-adaptation/feature-adaptation.json`。
- 生成 `output/platform-adaptation/implementation-guidance.json`。
- 生成 `output/platform-adaptation/risks.json`。
- 然后再执行 `harmony-module-plan` 到 `harmony-integration-summary`。

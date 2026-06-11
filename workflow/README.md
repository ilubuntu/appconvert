# iOS to HarmonyOS NEXT Workflow Runner

Use this runner when you want an explicit, profile-like workflow. Agent config defines identity; `codex exec` starts each stage.

Directory layout:

- `skills/`: reusable migration skills.
- `output/`: generated specs, screenshots, rendered prompts, status, and migration tracking files.
- `方案/`: plan, requirement, and agent design documents.
- `NewsMobile/`: source iOS project.
- `NewsMobileHarmony/`: target HarmonyOS NEXT project.
- `workflow/`: runner, profiles, prompts, and agent identity templates.
- `workflow/entry/`: workflow entry instructions; not counted as an execution skill.

Dry run:

```bash
python3 workflow/run_ios_to_harmony.py --dry-run
```

Run one stage:

```bash
python3 workflow/run_ios_to_harmony.py --execute --from-stage harmony-module-plan --to-stage harmony-module-plan
```

Use installed Codex profiles:

```bash
python3 workflow/run_ios_to_harmony.py --execute --use-installed-profiles
```

Profiles in `workflow/profiles/` are templates. To use `codex exec -p <profile>`, copy them to `$CODEX_HOME/<profile>.config.toml`.

Reusable agent identities:

```text
workflow/agents.config.toml
```

`[agents.*]` config is useful for naming reusable agent roles: who the agent is, its prompt, tools, and model. It does not start execution by itself. The runner starts stages with `codex exec`.

Stage boundaries:

- `ios-analyze`: deep iOS analysis. It must read Swift source file by file and produce `output/ios-analyze/ios源码索引.md`, `output/ios-analyze/ios函数级清单.md`, module/function/feature/UI/capability specs, and iOS screenshots.
- `ios-map`: map iOS native capabilities to HarmonyOS NEXT Kit or adapter layers.
- `harmony-module-plan`: create `output/harmony-generate/harmony模块实现计划.md` from the iOS module/function specs.
- `harmony-core-services`: implement Harmony models, services, stores, real-data loading, parsing, persistence, and 固定样例数据 fallback.
- `harmony-pages-ui`: implement ArkUI pages and components from iOS screenshots and UI specs.
- `harmony-platform-capabilities`: implement platform adapters for Web, TTS, notification, location, background, card/widget, cloud sync, local API, and permissions.
- `harmony-integration-summary`: aggregate module work, compare against the iOS function list, fill gaps, update tracking, and build.
- `harmony-visual-verify`: install/run or otherwise capture Harmony screenshots, compare page-by-page with iOS screenshots, write `output/harmony-visual-verify/界面对齐.md`, fix visible UI gaps, and build.

Recommended continuation after deep analysis:

```bash
python3 workflow/run_ios_to_harmony.py --execute --from-stage harmony-module-plan --to-stage harmony-integration-summary
```

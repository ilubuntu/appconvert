#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path


def load_workflow(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Workflow file must be JSON-compatible YAML: {path}\n{exc}") from exc


def render_prompt(template: str, values: dict[str, str]) -> str:
    text = template
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def shell_command(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def profile_installed(profile: str) -> bool:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return (codex_home / f"{profile}.config.toml").exists()


def validate_paths(workdir: Path, paths: list[str]) -> list[str]:
    missing: list[str] = []
    for item in paths:
        if not (workdir / item).exists():
            missing.append(item)
    return missing


def stage_selected(stage_id: str, from_stage: str | None, to_stage: str | None, stage_ids: list[str]) -> bool:
    start = stage_ids.index(from_stage) if from_stage else 0
    end = stage_ids.index(to_stage) if to_stage else len(stage_ids) - 1
    current = stage_ids.index(stage_id)
    return start <= current <= end


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or validate the iOS to HarmonyOS NEXT Codex workflow.")
    parser.add_argument("--workflow", default="workflow/ios-to-harmony.workflow.yaml")
    parser.add_argument("--workdir")
    parser.add_argument("--ios-project")
    parser.add_argument("--harmony-project")
    parser.add_argument("--from-stage")
    parser.add_argument("--to-stage")
    parser.add_argument("--dry-run", action="store_true", help="Print commands and validate files without running Codex.")
    parser.add_argument("--execute", action="store_true", help="Actually run codex exec for selected stages.")
    parser.add_argument("--use-installed-profiles", action="store_true", help="Pass -p <profile> to codex exec. Profiles must exist under CODEX_HOME.")
    args = parser.parse_args()

    workflow_path = Path(args.workflow).resolve()
    workflow = load_workflow(workflow_path)
    workdir = Path(args.workdir or workflow["workdir"]).resolve()
    ios_project = args.ios_project or workflow["ios_project"]
    harmony_project = args.harmony_project or workflow["harmony_project"]
    stages = workflow["stages"]
    stage_ids = [stage["id"] for stage in stages]

    if args.from_stage and args.from_stage not in stage_ids:
      raise SystemExit(f"Unknown --from-stage {args.from_stage}. Known stages: {', '.join(stage_ids)}")
    if args.to_stage and args.to_stage not in stage_ids:
      raise SystemExit(f"Unknown --to-stage {args.to_stage}. Known stages: {', '.join(stage_ids)}")
    if not args.dry_run and not args.execute:
        raise SystemExit("Choose --dry-run or --execute.")

    values = {
        "WORKDIR": str(workdir),
        "IOS_PROJECT": ios_project,
        "HARMONY_PROJECT": harmony_project,
    }

    print(f"workflow: {workflow['name']}")
    print(f"workdir: {workdir}")
    print(f"ios_project: {ios_project}")
    print(f"harmony_project: {harmony_project}")
    print("")

    overall_missing_inputs: list[str] = []
    for stage in stages:
        if not stage_selected(stage["id"], args.from_stage, args.to_stage, stage_ids):
            continue

        prompt_path = workdir / stage["prompt"]
        if not prompt_path.exists():
            raise SystemExit(f"Prompt not found: {prompt_path}")

        prompt = render_prompt(prompt_path.read_text(encoding="utf-8"), values)
        prompt_output = workdir / "output" / "00-workflow" / "rendered-prompts" / f"{stage['id']}.prompt.md"
        prompt_output.parent.mkdir(parents=True, exist_ok=True)
        prompt_output.write_text(prompt, encoding="utf-8")

        missing_inputs = validate_paths(workdir, stage.get("required_inputs", []))
        missing_outputs = validate_paths(workdir, stage.get("expected_outputs", []))
        overall_missing_inputs.extend([f"{stage['id']}:{item}" for item in missing_inputs])

        cmd = ["codex", "exec", "--skip-git-repo-check", "-C", str(workdir)]
        if args.use_installed_profiles:
            profile = stage["profile"]
            if not profile_installed(profile):
                print(f"warning: profile is not installed under CODEX_HOME: {profile}")
            cmd.extend(["-p", profile])
        cmd.append("-")

        print(f"stage: {stage['id']} ({stage['name']})")
        print(f"profile: {stage['profile']}")
        print(f"prompt: {prompt_output.relative_to(workdir)}")
        print(f"missing_inputs: {missing_inputs if missing_inputs else 'none'}")
        print(f"missing_expected_outputs_before_run: {missing_outputs if missing_outputs else 'none'}")
        print(f"command: {shell_command(cmd)} < {shlex.quote(str(prompt_output.relative_to(workdir)))}")
        print("")

        if args.execute:
            result = subprocess.run(cmd, input=prompt, text=True, cwd=workdir)
            if result.returncode != 0:
                return result.returncode

    if args.dry_run:
        if overall_missing_inputs:
            print("dry-run result: failed")
            print("missing required inputs:")
            for item in overall_missing_inputs:
                print(f"- {item}")
            return 2
        print("dry-run result: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
from pathlib import Path


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def load_screens(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    screens = payload.get("screens", [])
    if not isinstance(screens, list) or len(screens) == 0:
        raise SystemExit(f"No screens found in {path}")
    return screens


def screenshot_filename(index: int, screen: dict) -> str:
    existing = screen.get("screenshot")
    if isinstance(existing, str) and existing:
        return Path(existing).name
    screen_id = str(screen.get("id", f"screen-{index + 1}")).replace("_", "-")
    state = str(screen.get("state", "default")).replace("_", "-")
    return f"{index + 1:02d}-{screen_id}-{state}.png"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="booted")
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--screens-spec", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    screens = load_screens(Path(args.screens_spec))

    manifest = []
    for index, screen in enumerate(screens):
        screen_id = str(screen.get("id", f"screen-{index + 1}"))
        snapshot_arg = str(screen.get("snapshot_arg", screen_id))
        filename = screenshot_filename(index, screen)
        run([
            "xcrun", "simctl", "launch", "--terminate-running-process",
            args.device, args.bundle_id,
            "-uiSnapshotMode", "true",
            "-snapshotScreen", snapshot_arg,
        ])
        time.sleep(max(args.delay, 6.0) if index == 0 else args.delay)
        path = output_dir / filename
        run(["xcrun", "simctl", "io", args.device, "screenshot", str(path)])
        manifest.append({
            "file": filename,
            "screen_id": screen_id,
            "title": screen.get("name", screen_id),
            "state": screen.get("state", "default"),
            "required": bool(screen.get("required", True)),
            "path": str(path),
            "launch_args": ["-uiSnapshotMode", "true", "-snapshotScreen", snapshot_arg],
        })

    (output_dir / "screenshots-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def screenshot_stems(path: Path) -> set[str]:
    stems: set[str] = set()
    for item in path.iterdir():
        if item.name == "screenshots-manifest.json":
            continue
        if item.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            stems.add(item.stem)
    return stems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate that Harmony visual verification has real page screenshots.")
    parser.add_argument("--ios-dir", default="output/ios-analyze/screenshots/png")
    parser.add_argument("--harmony-dir", default="output/harmony-visual-verify/screenshots")
    parser.add_argument("--report", default="output/harmony-visual-verify/界面对齐.md")
    args = parser.parse_args()

    ios_dir = Path(args.ios_dir)
    harmony_dir = Path(args.harmony_dir)
    report = Path(args.report)

    failures: list[str] = []
    if not ios_dir.exists():
        failures.append(f"iOS screenshot dir missing: {ios_dir}")
    if not harmony_dir.exists():
        failures.append(f"Harmony screenshot dir missing: {harmony_dir}")
    if not report.exists():
        failures.append(f"visual report missing: {report}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 2

    ios = screenshot_stems(ios_dir)
    harmony = screenshot_stems(harmony_dir)
    missing = sorted(ios - harmony)
    extra = sorted(harmony - ios)

    if len(ios) == 0:
        failures.append("no iOS baseline screenshots found")
    if len(harmony) == 0:
        failures.append("no Harmony screenshots found")
    if len(harmony) < len(ios):
        failures.append(f"Harmony screenshot count {len(harmony)} is less than iOS baseline count {len(ios)}")
    if missing:
        failures.append("missing Harmony screenshots: " + ", ".join(missing))

    text = report.read_text(encoding="utf-8")
    if "结论：通过" in text and failures:
        failures.append("report claims pass while screenshot gate fails")
    for stem in sorted(ios):
        if stem not in text:
            failures.append(f"report does not mention page screenshot stem: {stem}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        if extra:
            print("INFO: extra Harmony screenshots: " + ", ".join(extra))
        return 1

    print(f"PASS: {len(ios)} iOS screenshots matched by {len(harmony)} Harmony screenshots")
    if extra:
        print("INFO: extra Harmony screenshots: " + ", ".join(extra))
    return 0


if __name__ == "__main__":
    sys.exit(main())

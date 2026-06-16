#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


HELPER_SOURCE = r'''import XCTest

final class RuntimeUITreeDumpTests: XCTestCase {
    func testDumpRuntimeUITree() throws {
        let app = XCUIApplication()
        app.launchArguments += ["-uiRuntimeTreeDump", "true"]
        app.launch()

        let payload = dump(element: app, depth: 0, maxDepth: 8)
        let data = try JSONSerialization.data(withJSONObject: payload, options: [.prettyPrinted])
        let text = String(data: data, encoding: .utf8) ?? "{}"
        print("BEGIN_IOS_RUNTIME_UI_TREE_JSON")
        print(text)
        print("END_IOS_RUNTIME_UI_TREE_JSON")
    }

    private func dump(element: XCUIElement, depth: Int, maxDepth: Int) -> [String: Any] {
        var node: [String: Any] = [
            "type": element.elementType.debugName,
            "label": element.label,
            "value": String(describing: element.value ?? ""),
            "identifier": element.identifier,
            "enabled": element.isEnabled,
            "selected": element.isSelected,
            "exists": element.exists,
            "frame": [
                "x": element.frame.origin.x,
                "y": element.frame.origin.y,
                "width": element.frame.size.width,
                "height": element.frame.size.height
            ]
        ]

        if depth < maxDepth {
            let children = element.children(matching: .any).allElementsBoundByIndex
            node["children"] = children.map { dump(element: $0, depth: depth + 1, maxDepth: maxDepth) }
        }
        return node
    }
}

private extension XCUIElement.ElementType {
    var debugName: String {
        switch self {
        case .application: return "application"
        case .window: return "window"
        case .sheet: return "sheet"
        case .drawer: return "drawer"
        case .alert: return "alert"
        case .dialog: return "dialog"
        case .button: return "button"
        case .radioButton: return "radio_button"
        case .radioGroup: return "radio_group"
        case .checkBox: return "checkbox"
        case .disclosureTriangle: return "disclosure_triangle"
        case .popUpButton: return "popup_button"
        case .comboBox: return "combo_box"
        case .menuButton: return "menu_button"
        case .toolbarButton: return "toolbar_button"
        case .popover: return "popover"
        case .keyboard: return "keyboard"
        case .key: return "key"
        case .navigationBar: return "navigation_bar"
        case .tabBar: return "tab_bar"
        case .tabGroup: return "tab_group"
        case .toolbar: return "toolbar"
        case .statusBar: return "status_bar"
        case .table: return "table"
        case .tableRow: return "table_row"
        case .tableColumn: return "table_column"
        case .outline: return "outline"
        case .outlineRow: return "outline_row"
        case .browser: return "browser"
        case .collectionView: return "collection_view"
        case .slider: return "slider"
        case .pageIndicator: return "page_indicator"
        case .progressIndicator: return "progress_indicator"
        case .activityIndicator: return "activity_indicator"
        case .segmentedControl: return "segmented_control"
        case .picker: return "picker"
        case .pickerWheel: return "picker_wheel"
        case .switch: return "switch"
        case .toggle: return "toggle"
        case .link: return "link"
        case .image: return "image"
        case .icon: return "icon"
        case .searchField: return "search_field"
        case .scrollView: return "scroll_view"
        case .scrollBar: return "scroll_bar"
        case .staticText: return "text"
        case .textField: return "text_field"
        case .secureTextField: return "secure_text_field"
        case .datePicker: return "date_picker"
        case .textView: return "text_view"
        case .menu: return "menu"
        case .menuItem: return "menu_item"
        case .menuBar: return "menu_bar"
        case .menuBarItem: return "menu_bar_item"
        case .map: return "map"
        case .webView: return "web_view"
        case .incrementArrow: return "increment_arrow"
        case .decrementArrow: return "decrement_arrow"
        case .timeline: return "timeline"
        case .ratingIndicator: return "rating_indicator"
        case .valueIndicator: return "value_indicator"
        case .splitGroup: return "split_group"
        case .splitter: return "splitter"
        case .relevanceIndicator: return "relevance_indicator"
        case .colorWell: return "color_well"
        case .helpTag: return "help_tag"
        case .matte: return "matte"
        case .dockItem: return "dock_item"
        case .ruler: return "ruler"
        case .rulerMarker: return "ruler_marker"
        case .grid: return "grid"
        case .levelIndicator: return "level_indicator"
        case .cell: return "cell"
        case .layoutArea: return "layout_area"
        case .layoutItem: return "layout_item"
        case .handle: return "handle"
        case .stepper: return "stepper"
        case .tab: return "tab"
        case .touchBar: return "touch_bar"
        case .other: return "other"
        @unknown default: return "unknown"
        }
    }
}
'''


def extract_json(text: str) -> dict:
    match = re.search(
        r"BEGIN_IOS_RUNTIME_UI_TREE_JSON\s*(\{.*?\})\s*END_IOS_RUNTIME_UI_TREE_JSON",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise SystemExit("No runtime UI tree JSON markers found in the input log")
    return json.loads(match.group(1))


def collect_key_elements(node: dict, limit: int = 80) -> list[dict]:
    result: list[dict] = []

    def visit(item: dict) -> None:
        if len(result) >= limit:
            return
        element_type = str(item.get("type", "unknown"))
        label = str(item.get("label", ""))
        identifier = str(item.get("identifier", ""))
        value = str(item.get("value", ""))
        if element_type in {
            "button", "toolbar_button", "text", "tab", "text_field", "secure_text_field",
            "search_field", "switch", "picker", "navigation_bar", "cell", "image",
        } or label or identifier:
            result.append({
                "type": element_type,
                "label": label,
                "value": value,
                "identifier": identifier,
                "frame": item.get("frame", {}),
                "enabled": bool(item.get("enabled", False)),
                "selected": bool(item.get("selected", False)),
                "exists": bool(item.get("exists", False)),
            })
        for child in item.get("children", []) or []:
            if isinstance(child, dict):
                visit(child)

    visit(node)
    return result


def count_elements(node: dict) -> int:
    total = 1
    for child in node.get("children", []) or []:
        if isinstance(child, dict):
            total += count_elements(child)
    return total


def run_command(cmd: list[str], cwd: Path | None = None) -> dict:
    try:
        result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=60)
        return {
            "command": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except FileNotFoundError as exc:
        return {
            "command": cmd,
            "returncode": 127,
            "stdout": "",
            "stderr": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": cmd,
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "command timed out",
        }


def parse_xcode_targets(text: str) -> list[str]:
    targets: list[str] = []
    in_targets = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "Targets:":
            in_targets = True
            continue
        if in_targets and stripped.endswith(":"):
            break
        if in_targets and stripped:
            targets.append(stripped)
    return targets


def preflight(project_root: Path, project_path: str | None, workspace_path: str | None, scheme: str | None) -> dict:
    checks: dict = {}

    simctl = run_command(["xcrun", "simctl", "list", "devices", "booted"])
    checks["simulator"] = simctl
    if simctl["returncode"] != 0:
        return {
            "status": "failed",
            "reason": "simulator_unavailable",
            "details": "xcrun simctl list devices booted failed in the current process.",
            "checks": checks,
        }
    if "(Booted)" not in simctl["stdout"]:
        return {
            "status": "failed",
            "reason": "simulator_unavailable",
            "details": "No booted simulator is visible from the current process.",
            "checks": checks,
        }

    list_cmd = ["xcodebuild", "-list"]
    if workspace_path:
        list_cmd.extend(["-workspace", workspace_path])
        if scheme:
            list_cmd.extend(["-scheme", scheme])
    elif project_path:
        list_cmd.extend(["-project", project_path])
    xcode_list = run_command(list_cmd, cwd=project_root)
    checks["xcodebuild_list"] = xcode_list
    if xcode_list["returncode"] != 0:
        return {
            "status": "failed",
            "reason": "xcodebuild_list_failed",
            "details": "xcodebuild -list failed.",
            "checks": checks,
        }

    targets = parse_xcode_targets(xcode_list["stdout"])
    ui_test_targets = [target for target in targets if target.endswith("UITests") or "UITests" in target]
    checks["targets"] = {
        "all": targets,
        "ui_test_targets": ui_test_targets,
    }
    if not ui_test_targets:
        return {
            "status": "failed",
            "reason": "ui_test_target_missing",
            "details": "No *UITests target found. Unit test targets are not enough for XCUITest runtime UI tree capture.",
            "checks": checks,
        }

    return {
        "status": "passed",
        "reason": "",
        "details": "Booted simulator and UI Test target are visible.",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or parse an XCUITest runtime UI tree dump.")
    parser.add_argument("--preflight", action="store_true", help="Check simulator and UI Test target availability")
    parser.add_argument("--project-root", help="iOS project root for xcodebuild -list")
    parser.add_argument("--project", help="Relative or absolute .xcodeproj path")
    parser.add_argument("--workspace", help="Relative or absolute .xcworkspace path")
    parser.add_argument("--scheme", help="Scheme used with workspace-based xcodebuild -list")
    parser.add_argument("--emit-helper", help="Write RuntimeUITreeDumpTests.swift to this path")
    parser.add_argument("--xcodebuild-log", help="Parse an xcodebuild test log containing JSON markers")
    parser.add_argument("--screen-id", default="screen.unknown")
    parser.add_argument("--runtime-state", default="unknown")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.preflight:
        project_root = Path(args.project_root or ".").resolve()
        payload = preflight(project_root, args.project, args.workspace, args.scheme)
        (output_dir / "preflight.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.emit_helper:
        helper_path = Path(args.emit_helper)
        helper_path.parent.mkdir(parents=True, exist_ok=True)
        helper_path.write_text(HELPER_SOURCE, encoding="utf-8")

    if not args.xcodebuild_log:
        return

    raw_tree = extract_json(Path(args.xcodebuild_log).read_text(encoding="utf-8", errors="ignore"))
    payload = {
        "screen_id": args.screen_id,
        "source": "xctest_accessibility",
        "runtime_state": args.runtime_state,
        "element_count": count_elements(raw_tree),
        "key_elements": collect_key_elements(raw_tree),
        "raw_tree": raw_tree,
    }
    filename = args.screen_id.replace(".", "-").replace("_", "-") + ".json"
    (output_dir / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z0-9_]+)", re.MULTILINE)
TYPE_RE = re.compile(r"\b(class|struct|enum|protocol|actor)\s+([A-Za-z_][A-Za-z0-9_]*)")
VIEW_RE = re.compile(r"\bstruct\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*View\b")
FUNC_RE = re.compile(
    r"^\s*(?:(?:public|private|fileprivate|internal|open)\s+)?"
    r"(?:static\s+|class\s+|mutating\s+)?func\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)"
    r"(?:\s*(?:async\s*)?(?:throws\s*)?(?:->\s*([^\n{]+))?)?",
    re.MULTILINE,
)
PROPERTY_RE = re.compile(
    r"^\s*(?:(?:public|private|fileprivate|internal|open)\s+)?"
    r"(?:@(?:State|Published|ObservedObject|StateObject|EnvironmentObject|Environment|AppStorage|Binding)[^\n]*\s+)?"
    r"(let|var)\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)

UI_PATTERNS = [
    "TabView",
    "NavigationStack",
    "NavigationView",
    "NavigationLink",
    ".sheet",
    ".fullScreenCover",
    ".toolbar",
    ".refreshable",
    "Form",
    "List",
    "ScrollView",
    "LazyVStack",
    "LazyHStack",
    "ForEach",
    "WebView",
    "WKWebView",
]

CAPABILITY_IMPORTS = {
    "AVFoundation": "media.avfoundation",
    "AVKit": "media.avkit",
    "CoreLocation": "location.corelocation",
    "MapKit": "map.mapkit",
    "PhotosUI": "photo.photosui",
    "UserNotifications": "notification.usernotifications",
    "WebKit": "webview.webkit",
    "WidgetKit": "widget.widgetkit",
}

EXCLUDED_DIR_NAMES = {
    ".build",
    ".git",
    "build",
    "DerivedData",
    "Pods",
    "Carthage",
    ".swiftpm",
}


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def is_excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in EXCLUDED_DIR_NAMES or part.endswith(".noindex") for part in parts)


def project_files(root: Path, pattern: str) -> list[Path]:
    return sorted(path for path in root.rglob(pattern) if not is_excluded(path, root))


def infer_module(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    parts = relative.parts
    if len(parts) <= 1:
        return "root"
    parent_parts = parts[:-1]
    useful = [part for part in parent_parts if not part.endswith(".xcodeproj")]
    if not useful:
        return "root"
    return ".".join(part.lower().replace(" ", "_") for part in useful[-2:])


def scan_swift_file(path: Path, root: Path) -> dict:
    text = read_text(path)
    imports = sorted(set(IMPORT_RE.findall(text)))
    functions = []
    for name, params, output in FUNC_RE.findall(text):
        functions.append({
            "name": name,
            "inputs": params.strip(),
            "output": output.strip(),
        })

    properties = []
    for kind, name in PROPERTY_RE.findall(text):
        properties.append({"kind": kind, "name": name})

    return {
        "path": rel(path, root),
        "module_hint": infer_module(path, root),
        "imports": imports,
        "types": [
            {"kind": kind, "name": name}
            for kind, name in TYPE_RE.findall(text)
        ],
        "views": VIEW_RE.findall(text),
        "functions": functions,
        "properties": properties,
        "ui_patterns": [pattern for pattern in UI_PATTERNS if pattern in text],
        "capability_hints": [
            CAPABILITY_IMPORTS[item]
            for item in imports
            if item in CAPABILITY_IMPORTS
        ],
        "line_count": text.count("\n") + 1,
    }


def build_module_index(files: list[dict]) -> list[dict]:
    modules: dict[str, dict] = {}
    for item in files:
        module_id = item["module_hint"]
        module = modules.setdefault(module_id, {
            "id": module_id,
            "files": [],
            "imports": set(),
            "types": [],
            "views": [],
            "function_count": 0,
            "capability_hints": set(),
        })
        module["files"].append(item["path"])
        module["imports"].update(item["imports"])
        module["types"].extend(item["types"])
        module["views"].extend(item["views"])
        module["function_count"] += len(item["functions"])
        module["capability_hints"].update(item["capability_hints"])

    result = []
    for module in modules.values():
        result.append({
            "id": module["id"],
            "files": sorted(module["files"]),
            "imports": sorted(module["imports"]),
            "types": module["types"],
            "views": sorted(set(module["views"])),
            "function_count": module["function_count"],
            "capability_hints": sorted(module["capability_hints"]),
        })
    return sorted(result, key=lambda item: item["id"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a neutral JSON scan index for an iOS project.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.exists():
        raise SystemExit(f"Project root does not exist: {root}")

    output_dir = Path(args.output_dir).resolve()
    scan_dir = output_dir / "scan"
    scan_dir.mkdir(parents=True, exist_ok=True)

    swift_files = project_files(root, "*.swift")
    source_files = [scan_swift_file(path, root) for path in swift_files]

    project = {
        "root": str(root),
        "swift_file_count": len(swift_files),
        "xcodeproj": [rel(path, root) for path in project_files(root, "*.xcodeproj")],
        "xcworkspace": [rel(path, root) for path in project_files(root, "*.xcworkspace")],
        "package_swift": [rel(path, root) for path in project_files(root, "Package.swift")],
        "podfile": [rel(path, root) for path in project_files(root, "Podfile")],
        "plist_files": [rel(path, root) for path in project_files(root, "*.plist")],
        "entitlements": [rel(path, root) for path in project_files(root, "*.entitlements")],
        "asset_catalogs": [rel(path, root) for path in project_files(root, "*.xcassets")],
    }

    imports = sorted({item for source in source_files for item in source["imports"]})
    views = [
        {
            "path": source["path"],
            "module_hint": source["module_hint"],
            "views": source["views"],
            "ui_patterns": source["ui_patterns"],
        }
        for source in source_files
        if source["views"] or source["ui_patterns"]
    ]
    capability_hints = sorted({
        hint
        for source in source_files
        for hint in source["capability_hints"]
    })

    (scan_dir / "project.scan.json").write_text(
        json.dumps(project, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (scan_dir / "source_index.json").write_text(
        json.dumps({"files": source_files}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (scan_dir / "module_hints.json").write_text(
        json.dumps({"modules": build_module_index(source_files)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (scan_dir / "ui_hints.json").write_text(
        json.dumps({"views": views}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (scan_dir / "capability_hints.json").write_text(
        json.dumps({"imports": imports, "capability_hints": capability_hints}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

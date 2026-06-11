#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


VIEW_RE = re.compile(r"\bstruct\s+(\w+)\s*:\s*View\b")
CLASS_RE = re.compile(r"\b(?:final\s+)?class\s+(\w+)")
STRUCT_RE = re.compile(r"\bstruct\s+(\w+)")
ENUM_RE = re.compile(r"\benum\s+(\w+)")
PROTOCOL_RE = re.compile(r"\bprotocol\s+(\w+)")
FUNC_RE = re.compile(r"^\s*(?:public\s+|internal\s+)?func\s+([A-Za-z0-9_]+)\s*\(", re.MULTILINE)
IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z0-9_]+)", re.MULTILINE)
NAV_PATTERNS = [
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
    "LazyVStack",
    "LazyHStack",
    "ForEach",
]


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def scan_swift_file(path: Path, root: Path) -> dict:
    text = path.read_text(errors="ignore")
    return {
        "path": rel(path, root),
        "imports": sorted(set(IMPORT_RE.findall(text))),
        "views": VIEW_RE.findall(text),
        "classes": CLASS_RE.findall(text),
        "structs": STRUCT_RE.findall(text),
        "enums": ENUM_RE.findall(text),
        "protocols": PROTOCOL_RE.findall(text),
        "functions": FUNC_RE.findall(text),
        "ui_patterns": [p for p in NAV_PATTERNS if p in text],
    }


def module_name(path: str) -> str:
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "NewsMobile":
        if parts[1] in {"Views", "Services", "Models", "ML", "Resources"}:
            if parts[1] == "Views" and len(parts) >= 3 and parts[2] == "Components":
                return "Views/Components"
            return parts[1]
        return "App"
    if len(parts) >= 1 and parts[0] == "NewsMobileWidget":
        return "Widget"
    if len(parts) >= 1 and parts[0] == "NewsMobileTests":
        return "Tests"
    return parts[0] if parts else "Unknown"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    swift_files = sorted(root.rglob("*.swift"))
    entitlements = sorted(root.rglob("*.entitlements"))
    plists = sorted(root.rglob("*.plist"))
    pbxproj = sorted(root.rglob("project.pbxproj"))

    swift_scan = [scan_swift_file(path, root) for path in swift_files]
    imports = sorted({imp for item in swift_scan for imp in item["imports"]})
    views = [item for item in swift_scan if item["views"]]
    ui_files = [item for item in swift_scan if item["ui_patterns"]]
    modules: dict[str, list[dict]] = {}
    for item in swift_scan:
        modules.setdefault(module_name(item["path"]), []).append(item)

    lines = [
        "# iOS 功能清单草稿",
        "",
        "## 工程概览",
        "",
        f"- Swift 文件数：{len(swift_files)}",
        f"- Apple/Swift imports：{', '.join(imports)}",
        "",
        "## 页面候选",
        "",
    ]

    for item in views:
        lines.append(f"### {', '.join(item['views'])}")
        lines.append("")
        lines.append(f"- 文件：`{item['path']}`")
        lines.append(f"- UI 线索：{', '.join(item['ui_patterns']) or '待人工确认'}")
        lines.append("- 用户价值：待根据代码和截图补充")
        lines.append("- 数据来源：待根据 Services/Models 补充")
        lines.append("- Harmony 迁移方式：待根据能力映射确认")
        lines.append("")

    lines.extend([
        "## 系统能力候选",
        "",
    ])
    for imp in imports:
        lines.append(f"- `{imp}`")
    lines.append("")

    (out / "ios功能清单.draft.md").write_text("\n".join(lines), encoding="utf-8")

    module_lines = [
        "# iOS 模块结构草稿",
        "",
        "## 工程概览",
        "",
        f"- Swift 文件数：{len(swift_files)}",
        f"- 模块数：{len(modules)}",
        "",
        "## 模块清单",
        "",
    ]

    for name, entries in sorted(modules.items()):
        module_imports = sorted({imp for entry in entries for imp in entry["imports"]})
        module_types = sorted({
            typ
            for entry in entries
            for typ in entry["classes"] + entry["structs"] + entry["enums"] + entry["protocols"]
        })
        module_functions = sorted({fn for entry in entries for fn in entry["functions"]})
        module_lines.append(f"### {name}")
        module_lines.append("")
        module_lines.append(f"- 文件数：{len(entries)}")
        module_lines.append(f"- 文件：{', '.join(f'`{entry['path']}`' for entry in entries)}")
        module_lines.append(f"- 类型：{', '.join(module_types) or '无'}")
        module_lines.append(f"- 对外方法线索：{', '.join(module_functions) or '无'}")
        module_lines.append(f"- Apple/Swift imports：{', '.join(module_imports) or '无'}")
        module_lines.append("- 模块职责：待根据代码补充")
        module_lines.append("- 对外接口：待根据调用关系补充")
        module_lines.append("- 依赖模块：待根据调用关系补充")
        module_lines.append("- HarmonyOS NEXT 参考拆分：待补充")
        module_lines.append("")

    module_lines.extend([
        "## 模块依赖关系",
        "",
        "| 上游模块 | 下游模块 | 依赖内容 | 依赖原因 | Harmony 迁移校验 |",
        "| --- | --- | --- | --- | --- |",
        "| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |",
        "",
    ])

    (out / "ios模块结构.draft.md").write_text("\n".join(module_lines), encoding="utf-8")


if __name__ == "__main__":
    main()

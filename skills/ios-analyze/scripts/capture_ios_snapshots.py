#!/usr/bin/env python3
import argparse
import json
import subprocess
import time
from pathlib import Path


SCREENS = [
    ("01-home.png", "home", "首页新闻流"),
    ("02-home-category.png", "homeCategory", "分类新闻页"),
    ("03-article-detail.png", "articleDetail", "文章详情"),
    ("04-article-webview.png", "articleWebView", "文章原文 WebView"),
    ("05-for-you.png", "forYou", "For You 推荐流"),
    ("06-search-empty.png", "searchEmpty", "搜索空态"),
    ("07-search-results.png", "searchResults", "搜索结果"),
    ("08-saved-empty.png", "savedEmpty", "收藏空态"),
    ("09-saved-with-article.png", "savedWithArticle", "收藏有数据"),
    ("10-settings.png", "settings", "设置页"),
    ("11-keyword-alerts.png", "keywordAlerts", "关键词提醒"),
    ("12-custom-feeds.png", "customFeeds", "自定义订阅源"),
    ("13-local-news.png", "localNews", "本地新闻"),
    ("14-audio-briefing.png", "audioBriefing", "语音播报"),
]


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="booted")
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--delay", type=float, default=2.0)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for index, (filename, screen, title) in enumerate(SCREENS):
        run([
            "xcrun", "simctl", "launch", "--terminate-running-process",
            args.device, args.bundle_id,
            "-uiSnapshotMode", "true",
            "-snapshotScreen", screen,
        ])
        time.sleep(max(args.delay, 6.0) if index == 0 else args.delay)
        path = output_dir / filename
        run(["xcrun", "simctl", "io", args.device, "screenshot", str(path)])
        manifest.append({
            "file": filename,
            "screen": screen,
            "title": title,
            "path": str(path),
            "launch_args": ["-uiSnapshotMode", "true", "-snapshotScreen", screen],
        })

    (output_dir / "screenshots-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

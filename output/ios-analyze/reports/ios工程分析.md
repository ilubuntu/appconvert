# iOS 工程分析

## 工程概览

- 工程：NewsMobile
- 类型：SwiftUI iOS 新闻聚合应用，带 WidgetKit 扩展
- 主 App bundle id：`com.jordankoch.NewsMobile`
- Widget bundle id：`com.jordankoch.NewsMobile.widget`
- Swift 文件数：46
- 外部依赖：README 声明无第三方依赖，使用 Apple 第一方框架
- 主入口：`NewsMobile/NewsMobile/NewsMobileApp.swift`
- 根导航：`NewsMobile/NewsMobile/ContentView.swift`

## 主要模块

| 模块 ID | 职责 | 关键路径 |
|---|---|---|
| app.shell | App 入口、根 Tab、截图模式、本地 API 启动 | `NewsMobileApp.swift`, `ContentView.swift`, `NovaAPIServer.swift` |
| models.news | 新闻、分类、设置、收藏、天气等领域模型 | `Models/NewsModels.swift` |
| services.news | RSS 聚合、解析、过滤、自定义源、本地新闻 | `Services/NewsAggregator.swift`, `RSSParser.swift` |
| ml.analysis | 情绪、实体、推荐、聚类、趋势 | `ML/`, `Services/PersonalizationEngine.swift` |
| services.persistence | 设置、收藏、iCloud、Widget 缓存 | `SettingsManager.swift`, `WatchLaterManager.swift`, `CloudSyncManager.swift` |
| services.platform | 通知、后台刷新、TTS、定位天气、本地 API | `NotificationManager.swift`, `BackgroundRefreshManager.swift`, `TTSManager.swift`, `WeatherService.swift` |
| views.news | 首页、推荐、搜索、收藏、详情、WebView、音频等页面 | `Views/` |
| views.settings | 设置、关键词、自定义源、本地新闻页面 | `Views/SettingsView.swift` 等 |
| widget.news | WidgetKit 小/中/大组件 | `NewsMobileWidget.swift` |

## 规格产物

- `output/ios-analyze/specs/project.json`
- `output/ios-analyze/specs/modules.json`
- `output/ios-analyze/specs/features.json`
- `output/ios-analyze/specs/functions.json`
- `output/ios-analyze/specs/screens.json`
- `output/ios-analyze/specs/capabilities.json`
- `output/ios-analyze/specs/resources.json`

## 备注

本次没有采集模拟器截图。原因是当前阶段重点是功能清单和结构化迁移索引；截图作为后续 UI 对齐辅助项保留在 `screens.json` 的 `screenshot_required` 和 `screenshot_reason` 字段中。

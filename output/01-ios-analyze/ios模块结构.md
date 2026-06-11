# iOS 模块结构

## 工程与 Target
- 工程：`NewsMobile.xcodeproj`
- Target：`NewsMobile` 主 app、`NewsMobileWidget` Widget 扩展、`NewsMobileTests` 单元/功能/安全/性能测试。
- App 入口：`NewsMobileApp`，环境对象为 `NewsAggregator`、`SettingsManager`、`WatchLaterManager`；截图模式由 `SnapshotSupport` 参数分流。

## DerivedData
### GeneratedSources
- 责任：Xcode DerivedData 资产符号扩展。
- 文件数：2
- `NewsMobile/DerivedData/NewsMobile/Index.noindex/Build/Intermediates.noindex/NewsMobile.build/Debug-iphonesimulator/NewsMobile.build/DerivedSources/GeneratedAssetSymbols.swift`：类型/扩展 16，函数 7，属性 7
- `NewsMobile/DerivedData/NewsMobile/Index.noindex/Build/Intermediates.noindex/NewsMobile.build/Debug-iphonesimulator/NewsMobileWidget.build/DerivedSources/GeneratedAssetSymbols.swift`：类型/扩展 15，函数 6，属性 2

## NewsMobile
### AppRoot
- 责任：App 入口、Tab 导航、截图模式样本数据和截图根视图。
- 文件数：3
- `NewsMobile/NewsMobile/ContentView.swift`：类型/扩展 4，函数 2，属性 23
- `NewsMobile/NewsMobile/NewsMobileApp.swift`：类型/扩展 1，函数 1，属性 5
- `NewsMobile/NewsMobile/NovaAPIServer.swift`：类型/扩展 2，函数 11，属性 11

### ML
- 责任：NaturalLanguage 情感分析和实体抽取。
- 文件数：2
- `NewsMobile/NewsMobile/ML/EntityExtractor.swift`：类型/扩展 1，函数 1，属性 6
- `NewsMobile/NewsMobile/ML/SentimentAnalyzer.swift`：类型/扩展 1，函数 1，属性 5

### Models
- 责任：领域模型、AI 后端管理、AI 配置界面。
- 文件数：5
- `NewsMobile/NewsMobile/Models/AIBackendManager+Enhanced.swift`：类型/扩展 5，函数 18，属性 47
- `NewsMobile/NewsMobile/Models/AIBackendManager+Generation.swift`：类型/扩展 6，函数 6，属性 32
- `NewsMobile/NewsMobile/Models/AIBackendManager.swift`：类型/扩展 6，函数 13，属性 62
- `NewsMobile/NewsMobile/Models/AIBackendStatusMenu.swift`：类型/扩展 3，函数 4，属性 17
- `NewsMobile/NewsMobile/Models/NewsModels.swift`：类型/扩展 20，函数 13，属性 100

### Services
- 责任：RSS、过滤、通知、后台任务、iCloud、个性化、TTS、天气、Widget 数据等业务服务。
- 文件数：17
- `NewsMobile/NewsMobile/Services/BackgroundRefreshManager.swift`：类型/扩展 1，函数 4，属性 5
- `NewsMobile/NewsMobile/Services/CloudSyncManager.swift`：类型/扩展 1，函数 5，属性 6
- `NewsMobile/NewsMobile/Services/ContentFilter.swift`：类型/扩展 1，函数 3，属性 12
- `NewsMobile/NewsMobile/Services/CustomFeedManager.swift`：类型/扩展 1，函数 7，属性 17
- `NewsMobile/NewsMobile/Services/KeywordAlertManager.swift`：类型/扩展 1，函数 9，属性 17
- `NewsMobile/NewsMobile/Services/LocalNewsService.swift`：类型/扩展 1，函数 6，属性 13
- `NewsMobile/NewsMobile/Services/NewsAggregator.swift`：类型/扩展 1，函数 6，属性 19
- `NewsMobile/NewsMobile/Services/NotificationManager.swift`：类型/扩展 1，函数 5，属性 4
- `NewsMobile/NewsMobile/Services/PersonalizationEngine.swift`：类型/扩展 1，函数 7，属性 15
- `NewsMobile/NewsMobile/Services/RSSParser.swift`：类型/扩展 3，函数 7，属性 24
- `NewsMobile/NewsMobile/Services/SettingsManager.swift`：类型/扩展 1，函数 3，属性 4
- `NewsMobile/NewsMobile/Services/StoryClusterEngine.swift`：类型/扩展 1，函数 6，属性 27
- `NewsMobile/NewsMobile/Services/TTSManager.swift`：类型/扩展 1，函数 10，属性 12
- `NewsMobile/NewsMobile/Services/TrendingTopicsEngine.swift`：类型/扩展 1，函数 3，属性 11
- `NewsMobile/NewsMobile/Services/WatchLaterManager.swift`：类型/扩展 1，函数 11，属性 7
- `NewsMobile/NewsMobile/Services/WeatherService.swift`：类型/扩展 1，函数 6，属性 15
- `NewsMobile/NewsMobile/Services/WidgetDataManager.swift`：类型/扩展 6，函数 8，属性 13

### Views
- 责任：页面级 SwiftUI 界面。
- 文件数：13
- `NewsMobile/NewsMobile/Views/ArticleDetailView.swift`：类型/扩展 5，函数 3，属性 23
- `NewsMobile/NewsMobile/Views/ArticleWebView.swift`：类型/扩展 3，函数 7，属性 8
- `NewsMobile/NewsMobile/Views/AudioBriefingView.swift`：类型/扩展 1，函数 0，属性 3
- `NewsMobile/NewsMobile/Views/CategoryView.swift`：类型/扩展 1，函数 0，属性 4
- `NewsMobile/NewsMobile/Views/CustomFeedsView.swift`：类型/扩展 3，函数 1，属性 17
- `NewsMobile/NewsMobile/Views/ForYouView.swift`：类型/扩展 1，函数 0，属性 8
- `NewsMobile/NewsMobile/Views/HomeView.swift`：类型/扩展 2，函数 0，属性 12
- `NewsMobile/NewsMobile/Views/KeywordAlertsView.swift`：类型/扩展 5，函数 0，属性 22
- `NewsMobile/NewsMobile/Views/LocalNewsView.swift`：类型/扩展 2，函数 0，属性 11
- `NewsMobile/NewsMobile/Views/SearchView.swift`：类型/扩展 2，函数 1，属性 14
- `NewsMobile/NewsMobile/Views/SettingsView.swift`：类型/扩展 1，函数 0，属性 4
- `NewsMobile/NewsMobile/Views/StoryClusterView.swift`：类型/扩展 4，函数 0，属性 15
- `NewsMobile/NewsMobile/Views/WatchLaterView.swift`：类型/扩展 2，函数 0，属性 7

### Views/Components
- 责任：页面复用组件。
- 文件数：4
- `NewsMobile/NewsMobile/Views/Components/ArticleCard.swift`：类型/扩展 1，函数 0，属性 5
- `NewsMobile/NewsMobile/Views/Components/BreakingNewsBanner.swift`：类型/扩展 1，函数 0，属性 4
- `NewsMobile/NewsMobile/Views/Components/TrendingBar.swift`：类型/扩展 2，函数 0，属性 4
- `NewsMobile/NewsMobile/Views/Components/WeatherWidget.swift`：类型/扩展 1，函数 0，属性 2

## NewsMobileTests
### Tests
- 责任：模型、设置、安全和性能测试。
- 文件数：1
- `NewsMobile/NewsMobileTests/NewsMobileTests.swift`：类型/扩展 18，函数 87，属性 134

## NewsMobileWidget
### WidgetExtension
- 责任：WidgetKit timeline、组件视图和 Widget 配置。
- 文件数：1
- `NewsMobile/NewsMobileWidget/NewsMobileWidget.swift`：类型/扩展 11，函数 10，属性 34

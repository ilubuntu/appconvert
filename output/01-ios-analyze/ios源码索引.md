# iOS 源码索引

- 分析目录：`NewsMobile/`
- Swift 文件总数：48；维护源码：46；DerivedData 生成源码：2
- 读取方式：逐个读取 `NewsMobile/` 下 Swift 文件；README、脚本和旧产物仅作为路径线索，不作为功能结论。
- 截图来源：现有 `-uiSnapshotMode true -snapshotScreen <screen>` 自动截图产物；本轮尝试访问 CoreSimulator 失败，未人工点击。

## Target: DerivedData
### 模块：GeneratedSources
- `NewsMobile/DerivedData/NewsMobile/Index.noindex/Build/Intermediates.noindex/NewsMobile.build/Debug-iphonesimulator/NewsMobile.build/DerivedSources/GeneratedAssetSymbols.swift`：248 行 （Xcode 生成）；类型：class ResourceBundleClass, extension DeveloperToolsSupport.ColorResource, extension DeveloperToolsSupport.ImageResource, extension AppKit.NSColor, extension UIKit.UIColor, extension SwiftUI.Color, extension SwiftUI.ShapeStyle, extension AppKit.NSImage, extension UIKit.UIImage, extension DeveloperToolsSupport.ColorResource, extension AppKit.NSColor, extension UIKit.UIColor
- `NewsMobile/DerivedData/NewsMobile/Index.noindex/Build/Intermediates.noindex/NewsMobile.build/Debug-iphonesimulator/NewsMobileWidget.build/DerivedSources/GeneratedAssetSymbols.swift`：201 行 （Xcode 生成）；类型：class ResourceBundleClass, extension DeveloperToolsSupport.ColorResource, extension DeveloperToolsSupport.ImageResource, extension AppKit.NSColor, extension UIKit.UIColor, extension SwiftUI.Color, extension SwiftUI.ShapeStyle, extension AppKit.NSImage, extension UIKit.UIImage, extension DeveloperToolsSupport.ColorResource, extension UIKit.UIColor, extension SwiftUI.Color

## Target: NewsMobile
### 模块：AppRoot
- `NewsMobile/NewsMobile/ContentView.swift`：346 行 ；类型：struct ContentView, enum SnapshotScreen, struct SnapshotSupport, struct SnapshotRootView
- `NewsMobile/NewsMobile/NewsMobileApp.swift`：47 行 ；类型：struct NewsMobileApp
- `NewsMobile/NewsMobile/NovaAPIServer.swift`：73 行 ；类型：class NovaAPIServer, struct NovaRequest

### 模块：ML
- `NewsMobile/NewsMobile/ML/EntityExtractor.swift`：51 行 ；类型：class EntityExtractor
- `NewsMobile/NewsMobile/ML/SentimentAnalyzer.swift`：43 行 ；类型：class SentimentAnalyzer

### 模块：Models
- `NewsMobile/NewsMobile/Models/AIBackendManager+Enhanced.swift`：374 行 ；类型：extension AIBackendManager, struct ConnectionTestResult, struct UsageStats, struct PerformanceMetrics, extension AIBackendManager
- `NewsMobile/NewsMobile/Models/AIBackendManager+Generation.swift`：371 行 ；类型：extension AIBackendManager, struct OllamaResponse, struct OpenAIResponse, struct Choice, struct Message, enum AIError
- `NewsMobile/NewsMobile/Models/AIBackendManager.swift`：622 行 ；类型：class AIBackendManager, enum AIBackend, struct OllamaResponse, struct Model, struct AIBackendSelectionView, struct BackendStatusRow
- `NewsMobile/NewsMobile/Models/AIBackendStatusMenu.swift`：309 行 ；类型：struct AIBackendStatusMenu, struct AIBackendStatusMenuCompact, struct AIBackendStatusMenu_Previews
- `NewsMobile/NewsMobile/Models/NewsModels.swift`：458 行 ；类型：enum NewsCategory, enum SourceBias, struct NewsSource, struct NewsArticle, struct SentimentResult, enum SentimentLabel, struct ExtractedEntity, enum EntityType, struct StoryCluster, struct PerspectiveBreakdown, struct WatchLaterItem, struct KeywordAlert

### 模块：Services
- `NewsMobile/NewsMobile/Services/BackgroundRefreshManager.swift`：64 行 ；类型：class BackgroundRefreshManager
- `NewsMobile/NewsMobile/Services/CloudSyncManager.swift`：76 行 ；类型：class CloudSyncManager
- `NewsMobile/NewsMobile/Services/ContentFilter.swift`：111 行 ；类型：class ContentFilter
- `NewsMobile/NewsMobile/Services/CustomFeedManager.swift`：118 行 ；类型：class CustomFeedManager
- `NewsMobile/NewsMobile/Services/KeywordAlertManager.swift`：127 行 ；类型：class KeywordAlertManager
- `NewsMobile/NewsMobile/Services/LocalNewsService.swift`：99 行 ；类型：class LocalNewsService
- `NewsMobile/NewsMobile/Services/NewsAggregator.swift`：165 行 ；类型：class NewsAggregator
- `NewsMobile/NewsMobile/Services/NotificationManager.swift`：63 行 ；类型：class NotificationManager
- `NewsMobile/NewsMobile/Services/PersonalizationEngine.swift`：130 行 ；类型：class PersonalizationEngine
- `NewsMobile/NewsMobile/Services/RSSParser.swift`：179 行 ；类型：class XMLParserBuffer, struct RawItem, actor RSSParser
- `NewsMobile/NewsMobile/Services/SettingsManager.swift`：43 行 ；类型：class SettingsManager
- `NewsMobile/NewsMobile/Services/StoryClusterEngine.swift`：126 行 ；类型：class StoryClusterEngine
- `NewsMobile/NewsMobile/Services/TTSManager.swift`：126 行 ；类型：class TTSManager
- `NewsMobile/NewsMobile/Services/TrendingTopicsEngine.swift`：77 行 ；类型：class TrendingTopicsEngine
- `NewsMobile/NewsMobile/Services/WatchLaterManager.swift`：102 行 ；类型：class WatchLaterManager
- `NewsMobile/NewsMobile/Services/WeatherService.swift`：105 行 ；类型：class WeatherService
- `NewsMobile/NewsMobile/Services/WidgetDataManager.swift`：131 行 ；类型：class WidgetDataManager, enum Keys, extension WidgetDataManager, struct NewsArticle, enum NewsCategory, enum Sentiment

### 模块：Views
- `NewsMobile/NewsMobile/Views/ArticleDetailView.swift`：248 行 ；类型：struct ArticleDetailView, struct SentimentBadge, struct BiasIndicatorBadge, struct EntityBadge, struct FlowLayout
- `NewsMobile/NewsMobile/Views/ArticleWebView.swift`：89 行 ；类型：struct ArticleWebView, struct WebView, class Coordinator
- `NewsMobile/NewsMobile/Views/AudioBriefingView.swift`：128 行 ；类型：struct AudioBriefingView
- `NewsMobile/NewsMobile/Views/CategoryView.swift`：41 行 ；类型：struct CategoryView
- `NewsMobile/NewsMobile/Views/CustomFeedsView.swift`：230 行 ；类型：struct CustomFeedsView, struct CustomFeedRow, struct AddFeedView
- `NewsMobile/NewsMobile/Views/ForYouView.swift`：114 行 ；类型：struct ForYouView
- `NewsMobile/NewsMobile/Views/HomeView.swift`：123 行 ；类型：struct HomeView, struct CategoryButton
- `NewsMobile/NewsMobile/Views/KeywordAlertsView.swift`：216 行 ；类型：struct KeywordAlertsView, extension String, struct KeywordRow, struct KeywordMatchesView, struct ArticleRow
- `NewsMobile/NewsMobile/Views/LocalNewsView.swift`：168 行 ；类型：struct LocalNewsView, struct LocationPickerView
- `NewsMobile/NewsMobile/Views/SearchView.swift`：141 行 ；类型：struct SearchView, struct SearchResultRow
- `NewsMobile/NewsMobile/Views/SettingsView.swift`：151 行 ；类型：struct SettingsView
- `NewsMobile/NewsMobile/Views/StoryClusterView.swift`：206 行 ；类型：struct StoryClusterView, struct SourceChip, struct PerspectiveSection, struct PerspectiveCard
- `NewsMobile/NewsMobile/Views/WatchLaterView.swift`：109 行 ；类型：struct WatchLaterView, struct WatchLaterRow

### 模块：Views/Components
- `NewsMobile/NewsMobile/Views/Components/ArticleCard.swift`：113 行 ；类型：struct ArticleCard
- `NewsMobile/NewsMobile/Views/Components/BreakingNewsBanner.swift`：92 行 ；类型：struct BreakingNewsBanner
- `NewsMobile/NewsMobile/Views/Components/TrendingBar.swift`：73 行 ；类型：struct TrendingBar, struct TrendingChip
- `NewsMobile/NewsMobile/Views/Components/WeatherWidget.swift`：82 行 ；类型：struct WeatherWidget

## Target: NewsMobileTests
### 模块：Tests
- `NewsMobile/NewsMobileTests/NewsMobileTests.swift`：819 行 ；类型：enum TestData, class NewsArticleModelTests, class NewsCategoryModelTests, class SourceBiasTests, class NewsSourceModelTests, class SentimentResultTests, class ExtractedEntityTests, class StoryClusterTests, class WatchLaterItemTests, class KeywordAlertTests, class CustomRSSFeedTests, class SettingsTests

## Target: NewsMobileWidget
### 模块：WidgetExtension
- `NewsMobile/NewsMobileWidget/NewsMobileWidget.swift`：424 行 ；类型：extension View, struct NewsEntry, struct HeadlineItem, struct WeatherData, struct NewsProvider, struct NewsWidgetEntryView, struct SmallNewsWidget, struct MediumNewsWidget, struct LargeNewsWidget, struct NewsHeadlineRow, struct NewsMobileWidget

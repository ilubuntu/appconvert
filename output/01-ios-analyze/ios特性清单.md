# iOS 特性清单

## SwiftUI Tab/NavigationStack 架构
- 说明：ContentView.liveContent 组织 5 个主 Tab；页面级 View 多用 NavigationStack 和 sheet 展示详情。
- 追溯：`NewsMobile/NewsMobile/ContentView.swift -> ContentView.liveContent`

## 截图模式隔离
- 说明：SnapshotSupport 只在 `-uiSnapshotMode` 参数存在时准备样本数据并使用 SnapshotRootView；NewsMobileApp.init 和 onAppear 在截图模式跳过 Nova API、后台任务、通知和真实抓取。
- 追溯：`NewsMobile/NewsMobile/ContentView.swift -> SnapshotSupport.prepare；NewsMobile/NewsMobile/NewsMobileApp.swift -> init/body`

## RSS 聚合与本地增强
- 说明：NewsAggregator 并发抓源后调用 ContentFilter、SentimentAnalyzer、EntityExtractor、KeywordAlertManager、PersonalizationEngine、TrendingTopicsEngine。
- 追溯：`NewsMobile/NewsMobile/Services/NewsAggregator.swift -> fetchAllNews`

## NaturalLanguage 使用
- 说明：SentimentAnalyzer 使用 `.sentimentScore`；EntityExtractor 和趋势/聚类使用 `.nameType`、`.lexicalClass`。
- 追溯：`NewsMobile/NewsMobile/ML/*.swift；NewsMobile/NewsMobile/Services/TrendingTopicsEngine.swift；StoryClusterEngine.swift`

## 多种系统能力
- 说明：UserNotifications、BackgroundTasks、AVFoundation、CoreLocation、WebKit、WidgetKit、iCloud KVS、Network 均在源码中出现。
- 追溯：`Services、Views/ArticleWebView.swift、NewsMobileWidget.swift、NovaAPIServer.swift`

## 本地持久化
- 说明：SettingsManager、WatchLaterManager、PersonalizationEngine 使用 UserDefaults；CloudSyncManager 和 WatchLaterManager 使用 NSUbiquitousKeyValueStore。
- 追溯：`SettingsManager.swift；WatchLaterManager.swift；PersonalizationEngine.swift；CloudSyncManager.swift`

## Widget App Group 数据通道
- 说明：WidgetDataManager 写 `group.com.jordankoch.newsmobile`，NewsProvider 读取同一 suiteName 生成 timeline。
- 追溯：`NewsMobile/NewsMobile/Services/WidgetDataManager.swift；NewsMobile/NewsMobileWidget/NewsMobileWidget.swift`

## AI 后端管理代码独立于新闻核心流
- 说明：AIBackendManager 提供通用后端检测、配置和生成能力，但主新闻流程未直接调用生成接口。
- 追溯：`NewsMobile/NewsMobile/Models/AIBackendManager*.swift`

## 测试覆盖偏模型和数据结构
- 说明：NewsMobileTests 覆盖模型 Codable、设置默认值、安全字符串、性能测量等；未发现 UI 自动化截图测试源码。
- 追溯：`NewsMobile/NewsMobileTests/NewsMobileTests.swift`

## 潜在源码问题：WidgetDataManager 模型重名
- 说明：WidgetDataManager.swift 末尾定义了占位 `NewsArticle`，与主 target 的 `NewsArticle` 同名；若文件进入同一 target，可能造成类型冲突或错误引用。
- 追溯：`NewsMobile/NewsMobile/Services/WidgetDataManager.swift -> placeholder NewsArticle`

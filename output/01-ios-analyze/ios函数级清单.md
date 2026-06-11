# iOS 函数级清单

轻量版。只用于后续迁移规划，不作为完整源码审计底账。

- 格式：模块 -> 函数 -> 输入 -> 输出/副作用。
- 只保留页面入口、业务入口、系统能力调用点和关键数据处理函数。
- 完整版本归档在：`output/01-ios-analyze/archive/ios函数级清单.full.md`。

## AppRoot
- 职责：应用入口、Tab 导航、截图模式、本地 API

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `ContentView.swift` / `ContentView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `ContentView.swift` / `SnapshotSupport` | `func prepare()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `ContentView.swift` / `SnapshotRootView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `NewsMobileApp.swift` / `NewsMobileApp` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `NewsMobileApp.swift` / `NewsMobileApp` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `NovaAPIServer.swift` / `NovaAPIServer` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `NovaAPIServer.swift` / `NovaAPIServer` | `func start()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `NovaAPIServer.swift` / `NovaAPIServer` | `func stop()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `NovaAPIServer.swift` / `NovaAPIServer` | `func route(_ req: NovaRequest) async -> String` | _ req: NovaRequest | 持久化或状态变更 |
| `NovaAPIServer.swift` / `NovaRequest` | `func bodyJSON() -> [String: Any]?` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `NovaAPIServer.swift` / `NovaRequest` | `init ?(_ data: Data)` | _ data: Data | 返回值或状态更新 |
| `NovaAPIServer.swift` / `NovaAPIServer` | `func http(_ s: Int, _ body: String, _ ct: String = "text/plain") -> String` | _ s: Int, _ body: String, _ ct: String = "text/plain" | UI 结构 / 页面状态 |

## Models
- 职责：领域模型、AI 后端配置和生成

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func generateWithFallback(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func testConnection(for backend: AIBackend) async -> ConnectionTestResult` | for backend: AIBackend | 持久化或状态变更 |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func sendNotification(title: String, message: String)` | title: String, message: String | 系统调用或运行时副作用 |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func startBackgroundMonitoring(interval: TimeInterval = 60.0)` | interval: TimeInterval = 60.0 | 系统调用或运行时副作用 |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func stopBackgroundMonitoring()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Models/AIBackendManager+Enhanced.swift` / `AIBackendManager` | `func notifyAvailabilityChanges(from previous: [AIBackend: Bool], to current: [AIBackend: Bool])` | from previous: [AIBackend: Bool], to current: [AIBackend: Bool] | 系统调用或运行时副作用 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generate(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generateWithOllama(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generateWithTinyLLM(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generateWithTinyChat(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generateWithOpenWebUI(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager+Generation.swift` / `AIBackendManager` | `func generateWithMLX(` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager.swift` / `AIBackendManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Models/AIBackendManager.swift` / `AIBackendManager` | `func refreshAllBackends() async` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Models/AIBackendManager.swift` / `AIBackendManager` | `func checkOllamaAvailability() async -> Bool` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager.swift` / `AIBackendManager` | `func loadConfiguration()` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Models/AIBackendManager.swift` / `AIBackendManager` | `func saveConfiguration()` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Models/AIBackendManager.swift` / `AIBackendSelectionView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Models/AIBackendManager.swift` / `BackendStatusRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Models/AIBackendStatusMenu.swift` / `AIBackendStatusMenu` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Models/AIBackendStatusMenu.swift` / `AIBackendStatusMenuCompact` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Models/NewsModels.swift` / `NewsSource` | `init (name: String, feedURL: URL, category: NewsCategory, bias: SourceBias = .unknown, reliability: Double = 0.8)` | name: String, feedURL: URL, category: NewsCategory, bias: SourceBias = .unknown, | 返回值或状态更新 |
| `Models/NewsModels.swift` / `NewsArticle` | `init (` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Models/NewsModels.swift` / `ExtractedEntity` | `init (text: String, type: EntityType)` | text: String, type: EntityType | 返回值或状态更新 |
| `Models/NewsModels.swift` / `StoryCluster` | `init (topic: String, articles: [NewsArticle])` | topic: String, articles: [NewsArticle] | 返回值或状态更新 |
| `Models/NewsModels.swift` / `WatchLaterItem` | `init (article: NewsArticle)` | article: NewsArticle | 返回值或状态更新 |
| `Models/NewsModels.swift` / `KeywordAlert` | `init (keyword: String)` | keyword: String | 返回值或状态更新 |
| `Models/NewsModels.swift` / `CustomRSSFeed` | `init (name: String, url: URL, category: NewsCategory)` | name: String, url: URL, category: NewsCategory | 返回值或状态更新 |
| `Models/NewsModels.swift` / `TrendingTopic` | `init (name: String, articleCount: Int, category: NewsCategory? = nil)` | name: String, articleCount: Int, category: NewsCategory? = nil | 返回值或状态更新 |
| `Models/NewsModels.swift` / `NewsMobileSettings` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Models/NewsModels.swift` / `UserPreferenceProfile` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Models/NewsModels.swift` / `Color` | `init (hex: String)` | hex: String | 返回值或状态更新 |

## Services
- 职责：RSS、存储、通知、后台、同步、推荐、TTS、天气等业务服务

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Services/BackgroundRefreshManager.swift` / `BackgroundRefreshManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/BackgroundRefreshManager.swift` / `BackgroundRefreshManager` | `func registerBackgroundTasks()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/BackgroundRefreshManager.swift` / `BackgroundRefreshManager` | `func scheduleAppRefresh()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Services/BackgroundRefreshManager.swift` / `BackgroundRefreshManager` | `func handleAppRefresh(task: BGAppRefreshTask)` | task: BGAppRefreshTask | 系统调用或运行时副作用 |
| `Services/CloudSyncManager.swift` / `CloudSyncManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/CloudSyncManager.swift` / `CloudSyncManager` | `func syncToCloud()` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Services/CloudSyncManager.swift` / `CloudSyncManager` | `func syncFromCloud()` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Services/ContentFilter.swift` / `ContentFilter` | `func filter(_ articles: [NewsArticle]) -> [NewsArticle]` | _ articles: [NewsArticle] | 返回值或状态更新 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `func addFeed(name: String, url: URL, category: NewsCategory)` | name: String, url: URL, category: NewsCategory | 持久化或状态变更 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `func removeFeed(id: UUID)` | id: UUID | 持久化或状态变更 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `func toggleFeed(id: UUID, enabled: Bool)` | id: UUID, enabled: Bool | 持久化或状态变更 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `func fetchFeed(_ feed: CustomRSSFeed) async -> [NewsArticle]` | _ feed: CustomRSSFeed | 数据结果 / 校验结果 / 状态更新 |
| `Services/CustomFeedManager.swift` / `CustomFeedManager` | `func validateFeedURL(_ url: URL) async -> Bool` | _ url: URL | 数据结果 / 校验结果 / 状态更新 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func addAlert(keyword: String)` | keyword: String | 持久化或状态变更 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func removeAlert(id: UUID)` | id: UUID | 持久化或状态变更 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func toggleAlert(id: UUID, enabled: Bool)` | id: UUID, enabled: Bool | 持久化或状态变更 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func checkAlerts(against articles: [NewsArticle])` | against articles: [NewsArticle] | 数据结果 / 校验结果 / 状态更新 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func sendNotification(for keyword: String, articleCount: Int, firstTitle: String?)` | for keyword: String, articleCount: Int, firstTitle: String? | 系统调用或运行时副作用 |
| `Services/KeywordAlertManager.swift` / `KeywordAlertManager` | `func articles(for keyword: String) -> [NewsArticle]` | for keyword: String | 返回值或状态更新 |
| `Services/LocalNewsService.swift` / `LocalNewsService` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/LocalNewsService.swift` / `LocalNewsService` | `func setLocation(zipCode: String)` | zipCode: String | 返回值或状态更新 |
| `Services/LocalNewsService.swift` / `LocalNewsService` | `func setLocation(city: String)` | city: String | 返回值或状态更新 |
| `Services/LocalNewsService.swift` / `LocalNewsService` | `func fetchLocalNews() async` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `func fetchAllNews() async` | 对象状态 / 服务依赖 / 无显式参数 | 数据结果 / 校验结果 / 状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `func fetchFeed(from source: NewsSource) async -> [NewsArticle]` | from source: NewsSource | 数据结果 / 校验结果 / 状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `func isBreakingNews(_ article: NewsArticle) -> Bool` | _ article: NewsArticle | 返回值或状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `func articles(for category: NewsCategory) -> [NewsArticle]` | for category: NewsCategory | 返回值或状态更新 |
| `Services/NewsAggregator.swift` / `NewsAggregator` | `func refresh() async` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Services/NotificationManager.swift` / `NotificationManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/NotificationManager.swift` / `NotificationManager` | `func requestPermission()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Services/NotificationManager.swift` / `NotificationManager` | `func sendBreakingNewsNotification(_ article: NewsArticle)` | _ article: NewsArticle | 系统调用或运行时副作用 |
| `Services/PersonalizationEngine.swift` / `PersonalizationEngine` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| `Services/PersonalizationEngine.swift` / `PersonalizationEngine` | `func recordView(article: NewsArticle, duration: TimeInterval)` | article: NewsArticle, duration: TimeInterval | 持久化或状态变更 |
| `Services/PersonalizationEngine.swift` / `PersonalizationEngine` | `func updateFromFetch(articles: [NewsArticle])` | articles: [NewsArticle] | 数据结果 / 校验结果 / 状态更新 |
| `Services/PersonalizationEngine.swift` / `PersonalizationEngine` | `func resetProfile()` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Services/RSSParser.swift` / `XMLParserBuffer` | `func parser(_ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String: String] = [:])` | _ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, | 数据结果 / 校验结果 / 状态更新 |
| `Services/RSSParser.swift` / `XMLParserBuffer` | `func parser(_ parser: XMLParser, foundCharacters string: String)` | _ parser: XMLParser, foundCharacters string: String | 数据结果 / 校验结果 / 状态更新 |
| `Services/RSSParser.swift` / `XMLParserBuffer` | `func parser(_ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?)` | _ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, q | 数据结果 / 校验结果 / 状态更新 |
| `Services/RSSParser.swift` / `RSSParser` | `func parse(data: Data, source: NewsSource) async -> [NewsArticle]` | data: Data, source: NewsSource | 数据结果 / 校验结果 / 状态更新 |
| `Services/RSSParser.swift` / `RSSParser` | `func processRawItems(_ rawItems: [XMLParserBuffer.RawItem], source: NewsSource) -> [NewsArticle]` | _ rawItems: [XMLParserBuffer.RawItem], source: NewsSource | 数据结果 / 校验结果 / 状态更新 |
| `Services/RSSParser.swift` / `RSSParser` | `func parseDate(_ string: String) -> Date?` | _ string: String | 数据结果 / 校验结果 / 状态更新 |
| `Services/SettingsManager.swift` / `SettingsManager` | `init ()` | 对象状态 / 服务依赖 / 无显式参数 | 返回值或状态更新 |
| ... | 省略 38 个低优先级函数 | 需要时查 archive | - |

## ML
- 职责：情感分析和实体抽取

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `ML/EntityExtractor.swift` / `EntityExtractor` | `func extract(from text: String) -> [ExtractedEntity]` | from text: String | 数据结果 / 校验结果 / 状态更新 |
| `ML/SentimentAnalyzer.swift` / `SentimentAnalyzer` | `func analyze(_ text: String) -> SentimentResult` | _ text: String | 数据结果 / 校验结果 / 状态更新 |

## Views
- 职责：页面级 SwiftUI 界面

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Views/ArticleDetailView.swift` / `ArticleDetailView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleDetailView.swift` / `SentimentBadge` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleDetailView.swift` / `BiasIndicatorBadge` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleDetailView.swift` / `EntityBadge` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `ArticleWebView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `WebView` | `func makeUIView(context: Context) -> WKWebView` | context: Context | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `WebView` | `func updateUIView(_ webView: WKWebView, context: Context)` | _ webView: WKWebView, context: Context | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `WebView` | `func makeCoordinator() -> Coordinator` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `Coordinator` | `init (_ parent: WebView)` | _ parent: WebView | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `Coordinator` | `func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!)` | _ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation! | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `Coordinator` | `func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!)` | _ webView: WKWebView, didFinish navigation: WKNavigation! | UI 结构 / 页面状态 |
| `Views/ArticleWebView.swift` / `Coordinator` | `func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error)` | _ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error | UI 结构 / 页面状态 |
| `Views/AudioBriefingView.swift` / `AudioBriefingView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/CategoryView.swift` / `CategoryView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/CustomFeedsView.swift` / `CustomFeedsView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/CustomFeedsView.swift` / `CustomFeedRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/CustomFeedsView.swift` / `AddFeedView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/CustomFeedsView.swift` / `AddFeedView` | `func addFeed()` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/ForYouView.swift` / `ForYouView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/HomeView.swift` / `HomeView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/HomeView.swift` / `CategoryButton` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/KeywordAlertsView.swift` / `KeywordAlertsView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/KeywordAlertsView.swift` / `KeywordRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/KeywordAlertsView.swift` / `KeywordMatchesView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/KeywordAlertsView.swift` / `ArticleRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/LocalNewsView.swift` / `LocalNewsView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/LocalNewsView.swift` / `LocationPickerView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/SearchView.swift` / `SearchView` | `init (initialSearchText: String = "")` | initialSearchText: String = "" | UI 结构 / 页面状态 |
| `Views/SearchView.swift` / `SearchView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/SearchView.swift` / `SearchResultRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/SettingsView.swift` / `SettingsView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/StoryClusterView.swift` / `StoryClusterView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/StoryClusterView.swift` / `SourceChip` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/StoryClusterView.swift` / `PerspectiveSection` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/StoryClusterView.swift` / `PerspectiveCard` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/WatchLaterView.swift` / `WatchLaterView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/WatchLaterView.swift` / `WatchLaterRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |

## Views/Components
- 职责：复用 UI 组件

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Views/Components/ArticleCard.swift` / `ArticleCard` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/Components/BreakingNewsBanner.swift` / `BreakingNewsBanner` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/Components/TrendingBar.swift` / `TrendingBar` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/Components/TrendingBar.swift` / `TrendingChip` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Views/Components/WeatherWidget.swift` / `WeatherWidget` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |

## WidgetExtension
- 职责：Widget timeline 和组件 UI

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Widget/NewsMobileWidget.swift` / `NewsProvider` | `func getSnapshot(in context: Context, completion: @escaping (NewsEntry) -> Void)` | in context: Context, completion: @escaping (NewsEntry | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsProvider` | `func getTimeline(in context: Context, completion: @escaping (Timeline<NewsEntry>) -> Void)` | in context: Context, completion: @escaping (Timeline<NewsEntry> | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsProvider` | `func loadCachedHeadlines() -> [HeadlineItem]` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsProvider` | `func loadCachedWeather() -> WeatherData?` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsProvider` | `func loadTrendingTopic() -> String?` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsWidgetEntryView` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `SmallNewsWidget` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `MediumNewsWidget` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `LargeNewsWidget` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsHeadlineRow` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |
| `Widget/NewsMobileWidget.swift` / `NewsMobileWidget` | `body` | View 状态、环境对象、传入 model | UI 结构 / 页面状态 |

## Tests
- 职责：模型/安全/性能测试参考

| 文件/类型 | 函数 | 输入 | 输出/副作用 |
| --- | --- | --- | --- |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleCreation()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleEquality()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleHashability()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleCodable() throws` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleCodableWithMLFields() throws` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleWithNilDescription()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleURLScheme()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `NewsArticleModelTests` | `func testArticleMutability()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `UserPreferenceProfileTests` | `func testProfileReadDuration()` | 对象状态 / 服务依赖 / 无显式参数 | 持久化或状态变更 |
| `Tests/NewsMobileTests.swift` / `SecurityTests` | `func testArticleLinkURLScheme()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `FrameTests` | `func testArticleCreationPerformance()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |
| `Tests/NewsMobileTests.swift` / `FrameTests` | `func testArticleCodablePerformance()` | 对象状态 / 服务依赖 / 无显式参数 | 系统调用或运行时副作用 |

## 使用规则

- 后续 agent 默认只读取这份轻量版。
- 只有实现某个具体模块证据不足时，才打开 archive 中对应文件段落。
- 不要把 archive 完整清单整体放入 prompt。
- 当前保留函数行：156。
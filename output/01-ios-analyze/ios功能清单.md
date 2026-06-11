# iOS 功能清单

每个功能均追溯到具体 iOS 文件、类型、函数/属性和截图。

## F01 启动与主导航
- 功能说明：App 注入聚合、设置、收藏环境对象，默认 Tab 包含首页、推荐、搜索、收藏、设置。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`, `output/01-ios-analyze/screenshots/png/05-for-you.png`, `output/01-ios-analyze/screenshots/png/06-search-empty.png`, `output/01-ios-analyze/screenshots/png/08-saved-empty.png`, `output/01-ios-analyze/screenshots/png/10-settings.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/NewsMobileApp.swift` -> `NewsMobileApp` -> `init, body`
  - `NewsMobile/NewsMobile/ContentView.swift` -> `ContentView` -> `body, liveContent`

## F02 RSS 新闻聚合
- 功能说明：内置多来源 RSS，按并发抓取、解析、过滤、情感/实体增强、分类、刷新时间和 breaking 状态更新。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`, `output/01-ios-analyze/screenshots/png/02-home-category.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/NewsAggregator.swift` -> `NewsAggregator` -> `fetchAllNews, fetchFeed, isBreakingNews, articles, refresh`
  - `NewsMobile/NewsMobile/Services/RSSParser.swift` -> `RSSParser/XMLParserBuffer` -> `parse, processRawItems, parseDate, cleanHTML`

## F03 分类新闻浏览
- 功能说明：新闻按 NewsCategory 归类，首页横向分类按钮切换，独立分类页显示指定分类列表。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`, `output/01-ios-analyze/screenshots/png/02-home-category.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Models/NewsModels.swift` -> `NewsCategory` -> `icon, color, id`
  - `NewsMobile/NewsMobile/Views/HomeView.swift` -> `HomeView/CategoryButton` -> `categoryPicker, body`
  - `NewsMobile/NewsMobile/Views/CategoryView.swift` -> `CategoryView` -> `body`

## F04 文章卡片与详情
- 功能说明：列表卡显示来源、时间、标题、摘要、情感、倾向和收藏按钮；详情页提供原文、保存、朗读、分享、实体标签。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`, `output/01-ios-analyze/screenshots/png/03-article-detail.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Views/Components/ArticleCard.swift` -> `ArticleCard` -> `body, sentimentColor`
  - `NewsMobile/NewsMobile/Views/ArticleDetailView.swift` -> `ArticleDetailView/SentimentBadge/BiasIndicatorBadge/EntityBadge/FlowLayout` -> `body, layout, sizeThatFits, placeSubviews`

## F05 WebView 原文阅读
- 功能说明：文章详情打开 WKWebView，展示加载态和分享操作。
- 截图：`output/01-ios-analyze/screenshots/png/04-article-webview.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Views/ArticleWebView.swift` -> `ArticleWebView/WebView/Coordinator` -> `body, makeUIView, updateUIView, makeCoordinator, didStartProvisionalNavigation, didFinish, didFail`

## F06 搜索
- 功能说明：按标题、摘要和来源名称过滤全量文章，结果行高亮命中的标题文本。
- 截图：`output/01-ios-analyze/screenshots/png/06-search-empty.png`, `output/01-ios-analyze/screenshots/png/07-search-results.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Views/SearchView.swift` -> `SearchView/SearchResultRow` -> `filteredArticles, body, emptySearchView, noResultsView, resultsList, highlightedTitle`

## F07 稍后阅读/收藏
- 功能说明：文章可加入 Watch Later，本地 UserDefaults 持久化并按需同步 iCloud，列表支持阅读标记和删除。
- 截图：`output/01-ios-analyze/screenshots/png/08-saved-empty.png`, `output/01-ios-analyze/screenshots/png/09-saved-with-article.png`, `output/01-ios-analyze/screenshots/png/03-article-detail.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/WatchLaterManager.swift` -> `WatchLaterManager` -> `add, remove, markAsRead, isInWatchLater, toggle, saveItems, loadItems, syncToCloud, syncFromCloud`
  - `NewsMobile/NewsMobile/Views/WatchLaterView.swift` -> `WatchLaterView/WatchLaterRow` -> `body, emptyView, articlesList`

## F08 个性化推荐
- 功能说明：根据阅读时长更新分类、来源、实体偏好，并按偏好与时效为文章排序生成 For You。
- 截图：`output/01-ios-analyze/screenshots/png/05-for-you.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/PersonalizationEngine.swift` -> `PersonalizationEngine` -> `recordView, updateFromFetch, normalizePreferences, saveProfile, loadProfile, resetProfile`
  - `NewsMobile/NewsMobile/Views/ForYouView.swift` -> `ForYouView` -> `body, disabledView, emptyView, articlesList`

## F09 关键词提醒
- 功能说明：设置关键词、开启/关闭提醒，刷新后检查新文章匹配，记录匹配数并发本地通知。
- 截图：`output/01-ios-analyze/screenshots/png/11-keyword-alerts.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/KeywordAlertManager.swift` -> `KeywordAlertManager` -> `addAlert, removeAlert, toggleAlert, checkAlerts, sendNotification, articles, clearMatches, clearNewMatchesFlag`
  - `NewsMobile/NewsMobile/Views/KeywordAlertsView.swift` -> `KeywordAlertsView/KeywordRow/KeywordMatchesView/ArticleRow` -> `body, highlightedTitle`

## F10 自定义 RSS 源
- 功能说明：用户可添加、验证、启停、删除自定义 RSS 源，也可一键添加建议源并查看最近文章。
- 截图：`output/01-ios-analyze/screenshots/png/12-custom-feeds.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/CustomFeedManager.swift` -> `CustomFeedManager` -> `addFeed, removeFeed, toggleFeed, fetchAllCustomFeeds, fetchFeed, validateFeedURL`
  - `NewsMobile/NewsMobile/Views/CustomFeedsView.swift` -> `CustomFeedsView/CustomFeedRow/AddFeedView` -> `body, addFeed`

## F11 本地新闻
- 功能说明：用城市或 ZIP 构造 Google News 本地 RSS 搜索，抓取后做情感分析并在本地新闻页展示。
- 截图：`output/01-ios-analyze/screenshots/png/13-local-news.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/LocalNewsService.swift` -> `LocalNewsService` -> `setLocation(zipCode:), setLocation(city:), clearLocation, loadLocation, fetchLocalNews`
  - `NewsMobile/NewsMobile/Views/LocalNewsView.swift` -> `LocalNewsView/LocationPickerView` -> `body, setupView, loadingView, emptyView, articlesList`

## F12 天气组件
- 功能说明：请求定位后调用 Open-Meteo 当前天气接口，首页天气组件显示温度、体感、湿度和天气图标。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/WeatherService.swift` -> `WeatherService` -> `requestLocation, locationManager(didUpdateLocations:), fetchWeather, weatherDescription`
  - `NewsMobile/NewsMobile/Views/Components/WeatherWidget.swift` -> `WeatherWidget` -> `body`

## F13 趋势话题
- 功能说明：用 NaturalLanguage 提取标题实体和名词，统计出现次数生成趋势条。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/TrendingTopicsEngine.swift` -> `TrendingTopicsEngine` -> `analyze, extractTopics`
  - `NewsMobile/NewsMobile/Views/Components/TrendingBar.swift` -> `TrendingBar/TrendingChip` -> `body`

## F14 多源故事聚类与视角分析
- 功能说明：用标题关键词寻找跨来源相关文章，生成主题、来源数、文章数、左右中视角和共同事实。
- 截图：`output/01-ios-analyze/screenshots/png/02-home-category.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/StoryClusterEngine.swift` -> `StoryClusterEngine` -> `clusterArticles, findRelatedArticles, extractKeywords, extractMainTopic, analyzePerspectives`
  - `NewsMobile/NewsMobile/Views/StoryClusterView.swift` -> `StoryClusterView/SourceChip/PerspectiveSection/PerspectiveCard` -> `body`

## F15 语音播报
- 功能说明：用 AVSpeechSynthesizer 朗读文章来源、标题和摘要，支持播放、暂停、继续、前后切换和自动续播。
- 截图：`output/01-ios-analyze/screenshots/png/14-audio-briefing.png`, `output/01-ios-analyze/screenshots/png/03-article-detail.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/TTSManager.swift` -> `TTSManager` -> `configureAudioSession, startBriefing, stop, pause, resume, next, previous, speakCurrentArticle, speechSynthesizer(didFinish:)`
  - `NewsMobile/NewsMobile/Views/AudioBriefingView.swift` -> `AudioBriefingView` -> `body`

## F16 设置与偏好持久化
- 功能说明：设置页控制显示、通知、音频、个性化、过滤、iCloud、后台刷新和天气，SettingsManager 用 UserDefaults 编解码持久化。
- 截图：`output/01-ios-analyze/screenshots/png/10-settings.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Views/SettingsView.swift` -> `SettingsView` -> `body`
  - `NewsMobile/NewsMobile/Services/SettingsManager.swift` -> `SettingsManager` -> `saveSettings, resetToDefaults`

## F17 iCloud 同步
- 功能说明：CloudSyncManager 用 NSUbiquitousKeyValueStore 同步设置；WatchLaterManager 也可同步收藏队列。
- 截图：`output/01-ios-analyze/screenshots/png/10-settings.png`, `output/01-ios-analyze/screenshots/png/09-saved-with-article.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/CloudSyncManager.swift` -> `CloudSyncManager` -> `syncToCloud, syncFromCloud, handleCloudUpdate, clearCloudData`
  - `NewsMobile/NewsMobile/Services/WatchLaterManager.swift` -> `WatchLaterManager` -> `syncToCloud, syncFromCloud`

## F18 通知与 breaking news
- 功能说明：启动时请求通知权限，RSS 刷新识别 breaking 关键词并通过 overlay banner 或本地通知提示。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/NotificationManager.swift` -> `NotificationManager` -> `requestPermission, checkAuthorizationStatus, sendBreakingNewsNotification, clearBadge`
  - `NewsMobile/NewsMobile/Views/Components/BreakingNewsBanner.swift` -> `BreakingNewsBanner` -> `body`

## F19 后台刷新
- 功能说明：注册 BGAppRefreshTask，提交 15 分钟后刷新请求，后台任务中调用 NewsAggregator.fetchAllNews。
- 截图：`output/01-ios-analyze/screenshots/png/10-settings.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/BackgroundRefreshManager.swift` -> `BackgroundRefreshManager` -> `registerBackgroundTasks, scheduleAppRefresh, handleAppRefresh`
  - `NewsMobile/NewsMobile/NewsMobileApp.swift` -> `NewsMobileApp` -> `init`

## F20 Widget 数据与展示
- 功能说明：主 app 通过 App Group UserDefaults 写入头条、天气、趋势，Widget timeline 读取缓存并按小/中/大组件展示。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Services/WidgetDataManager.swift` -> `WidgetDataManager` -> `updateHeadlines, updateWeather, updateTrendingTopic, refreshWidget, clearWidgetData, updateFromArticles, onNewsRefreshed`
  - `NewsMobile/NewsMobileWidget/NewsMobileWidget.swift` -> `NewsProvider/NewsWidgetEntryView/SmallNewsWidget/MediumNewsWidget/LargeNewsWidget/NewsMobileWidget` -> `placeholder, getSnapshot, getTimeline, loadCachedHeadlines, loadCachedWeather, loadTrendingTopic, body`

## F21 AI 后端检测与生成
- 功能说明：通用 AIBackendManager 检测本地/云端后端，保存配置，支持 Ollama/TinyLLM/TinyChat/OpenWebUI/MLX 生成和 fallback、连接测试、使用统计。
- 截图：`output/01-ios-analyze/screenshots/png/10-settings.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/Models/AIBackendManager.swift` -> `AIBackendManager/AIBackendSelectionView/BackendStatusRow` -> `refreshAllBackends, check*Availability, loadOllamaModels, loadConfiguration, saveConfiguration, body`
  - `NewsMobile/NewsMobile/Models/AIBackendManager+Generation.swift` -> `AIBackendManager/AIError` -> `generate, generateWithOllama, generateWithTinyLLM, generateWithTinyChat, generateWithOpenWebUI, generateWithMLX`
  - `NewsMobile/NewsMobile/Models/AIBackendManager+Enhanced.swift` -> `AIBackendManager` -> `generateWithFallback, testConnection, recordUsage, recordPerformance, startBackgroundMonitoring`

## F22 本地 Nova API 状态服务
- 功能说明：正常启动时开启 127.0.0.1:37436 TCP HTTP 服务，提供 /api/status 和 /api/ping。截图模式跳过启动。
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`
- 源码追溯：
  - `NewsMobile/NewsMobile/NovaAPIServer.swift` -> `NovaAPIServer/NovaRequest` -> `start, stop, handle, receive, route, json, http`
  - `NewsMobile/NewsMobile/NewsMobileApp.swift` -> `NewsMobileApp` -> `init`

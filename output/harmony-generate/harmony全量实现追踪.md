# 全量实现追踪

## 新闻核心模块实现记录 (news sub_stage)

### 已创建文件清单

| 文件路径 | iOS 源文件 | 状态 | 说明 |
|---|---|---|---|
| entry/src/main/ets/support/DateUtils.ets | NewsModels.swift 日期工具 | 已实现 | formatRelativeTime, parseRssDate, formatDate |
| entry/src/main/ets/support/TextUtils.ets | SearchView.swift 高亮 | 已实现 | stripHtml, truncateText, buildHighlightedSpans |
| entry/src/main/ets/support/Constants.ets | NewsAggregator.swift 常量 | 已实现 | RSS_SOURCES, SUGGESTED_FEEDS, POPULAR_CITIES, API URLs |
| entry/src/main/ets/stores/NewsStore.ets | NewsAggregator 状态 | 已实现 | articles, breakingNews, weatherData, trendingTopics, storyClusters |
| entry/src/main/ets/stores/SettingsStore.ets | SettingsManager.swift | 已实现 | load/save/reset/update settings |
| entry/src/main/ets/stores/WatchLaterStore.ets | WatchLaterManager.swift | 已实现 | add/remove/toggle/markAsRead |
| entry/src/main/ets/stores/PersonalizationStore.ets | PersonalizationEngine.swift | 已实现 | preference, personalizedArticles |
| entry/src/main/ets/stores/CustomFeedStore.ets | CustomFeedManager.swift | 已实现 | feeds, customArticles, CRUD |
| entry/src/main/ets/services/news/HttpClient.ets | NewsAggregator.swift URLSession | 已实现 | @ohos.net.http 封装, GET/POST/fetchXml |
| entry/src/main/ets/services/rss/RssParser.ets | RSSParser.swift | 已实现 | RSS 2.0 + Atom 解析, 日期/HTML 处理 |
| entry/src/main/ets/services/news/ContentFilter.ets | ContentFilter.swift | 已实现 | 广告/标题党过滤 |
| entry/src/main/ets/services/news/NewsAggregator.ets | NewsAggregator.swift | 已实现 | fetchAllNews/refresh/articlesForCategory + 分析链路 |
| entry/src/main/ets/services/search/SearchService.ets | SearchView.swift filteredArticles | 已实现 | 标题/描述/来源搜索 + 高亮 |
| entry/src/main/ets/services/weather/WeatherService.ets | WeatherService.swift | 已实现 | Open-Meteo API + 回退数据 |
| entry/src/main/ets/services/nlp/SentimentAnalyzer.ets | SentimentAnalyzer.swift | 已实现 | 启发式情绪分析 (positive/negative/neutral) |
| entry/src/main/ets/services/nlp/EntityExtractor.ets | EntityExtractor.swift | 已实现 | 正则实体提取 (ORG/GPE/PERSON/TOPIC) |
| entry/src/main/ets/services/ai/StoryClusterEngine.ets | StoryClusterEngine.swift | 已实现 | 名词重叠聚类算法 |
| entry/src/main/ets/services/ai/TrendingTopicsEngine.ets | TrendingTopicsEngine.swift | 已实现 | 实体频次统计 + 专有名词分析 |
| entry/src/main/ets/services/personalization/PersonalizationEngine.ets | PersonalizationEngine.swift | 已实现 | updateFromFetch/recordView/resetProfile |
| entry/src/main/ets/services/news/WatchLaterManager.ets | WatchLaterManager.swift | 已实现 | add/remove/toggle/markAsRead/syncToCloud |
| entry/src/main/ets/services/news/CustomFeedManager.ets | CustomFeedManager.swift | 已实现 | addFeed/removeFeed/toggleFeed/validateFeedURL/fetchAllCustomFeeds |
| entry/src/main/ets/services/news/LocalNewsService.ets | LocalNewsService.swift | 已实现 | fetchLocalNews/setLocation/clearLocation |
| entry/src/main/ets/fixtures/SampleData.ets | ContentView.swift sample | 已实现 | 样例文章/天气/趋势/收藏/关键词/自定义源/本地新闻 |
| entry/src/main/ets/fixtures/SnapshotFixtures.ets | ContentView.swift SnapshotSupport | 已实现 | prepare() 按 SnapshotScreen 注入固定数据 |
| entry/src/main/ets/components/ArticleCard.ets | ArticleCard.swift | 已实现 | 标题/描述/来源/时间/分类/情绪/BREAKING 标签 |
| entry/src/main/ets/components/TrendingBar.ets | TrendingBar.swift | 已实现 | 横向趋势话题 chips |
| entry/src/main/ets/components/WeatherWidget.ets | WeatherWidget.swift | 已实现 | 温度/湿度/体感/风速/位置 |
| entry/src/main/ets/components/CategoryButton.ets | HomeView CategoryButton | 已实现 | 分类胶囊按钮 + 选中态颜色 |
| entry/src/main/ets/components/SentimentBadge.ets | SentimentBadge.swift | 已实现 | positive/negative/neutral + score |
| entry/src/main/ets/components/EntityBadge.ets | EntityBadge.swift | 已实现 | 实体标签 Flex Wrap 布局 |
| entry/src/main/ets/components/SearchResultRow.ets | SearchView.swift result row | 已实现 | 标题高亮 + 描述 + 来源 + 时间 |
| entry/src/main/ets/components/WatchLaterRow.ets | WatchLaterView row | 已实现 | 标题 + 描述 + 来源 + 未读圆点 |
| entry/src/main/ets/components/EmptyStateView.ets | 各空态页面 | 已实现 | 图标 + 标题 + 副标题 + 可选操作按钮 |
| entry/src/main/ets/pages/MainPage.ets | ContentView.swift TabView | 已实现 | 5 Tab 导航 (Home/ForYou/Search/Saved/Settings) + 突发新闻横幅 |
| entry/src/main/ets/pages/HomePage.ets | HomeView.swift | 已实现 | 天气 + 趋势 + 分类选择器 + 文章列表 + 空态/加载态 |
| entry/src/main/ets/pages/ForYouPage.ets | ForYouView.swift | 已实现 | 禁用态 + 空态 + 有数据态 |
| entry/src/main/ets/pages/SearchPage.ets | SearchView.swift | 已实现 | 搜索栏 + 结果列表 + 高亮 + 无结果空态 |
| entry/src/main/ets/pages/SavedPage.ets | WatchLaterView.swift | 已实现 | 收藏列表 + 未读圆点 + 滑动删除 + 空态 |
| entry/src/main/ets/pages/SettingsPage.ets | SettingsView.swift | 已实现 | Form 分区 + Toggle + Reset to Defaults |
| entry/src/main/ets/pages/ArticleDetailPage.ets | ArticleDetailView.swift | 已实现 | 详情 + 收藏/听读/分享/阅读全文 + 情绪/实体 badge |
| entry/src/main/ets/pages/ArticleWebPage.ets | ArticleWebView.swift | 已实现 | Web 组件 + 加载状态 + Done/Share |
| entry/src/main/ets/pages/SnapshotSupport.ets | ContentView.swift SnapshotSupport | 已实现 | 导出 SnapshotScreen + SnapshotFixtures |
| entry/src/main/ets/pages/Index.ets | NewsMobileApp.swift | 已实现 | 入口页面加载 MainPage |

## 类型级处置表

| iOS 文件 | iOS 类型 | Harmony 文件 | Harmony 类型 | 状态 | 证据 |
|---|---|---|---|---|---|
| NewsMobile/NewsMobile/Models/NewsModels.swift | NewsCategory | entry/src/main/ets/models/news/NewsCategory.ets | NewsCategory | 已实现 | 枚举类，含所有分类名、图标和颜色映射 |
| NewsMobile/NewsMobile/Models/NewsModels.swift | NewsSource | entry/src/main/ets/models/news/NewsSource.ets | NewsSource | 已实现 | 数据类，含 id、name、url、category |
| NewsMobile/NewsMobile/Models/NewsModels.swift | NewsArticle | entry/src/main/ets/models/news/NewsArticle.ets | NewsArticle | 已实现 | 数据类，含所有文章字段和 sentiment/entities 可选属性 |
| NewsMobile/NewsMobile/Models/NewsModels.swift | SentimentResult | entry/src/main/ets/models/news/SentimentResult.ets | SentimentResult | 已实现 | 数据类，含 score 和 label |
| NewsMobile/NewsMobile/Models/NewsModels.swift | ExtractedEntity | entry/src/main/ets/models/news/ExtractedEntity.ets | ExtractedEntity | 已实现 | 数据类，含 name、type、mentionCount |
| NewsMobile/NewsMobile/Models/NewsModels.swift | StoryCluster | entry/src/main/ets/models/news/StoryCluster.ets | StoryCluster | 已实现 | 数据类，含 topic、articles、sourceCount、perspectives |
| NewsMobile/NewsMobile/Models/NewsModels.swift | WatchLaterItem | entry/src/main/ets/models/news/WatchLaterItem.ets | WatchLaterItem | 已实现 | 数据类，含 article、addedAt、isRead |
| NewsMobile/NewsMobile/Models/NewsModels.swift | KeywordAlert | entry/src/main/ets/models/news/KeywordAlert.ets | KeywordAlert | 已实现 | 数据类，含 keyword、isEnabled、matchedArticles |
| NewsMobile/NewsMobile/Models/NewsModels.swift | CustomRSSFeed | entry/src/main/ets/models/news/CustomRSSFeed.ets | CustomRSSFeed | 已实现 | 数据类，含 name、url、category、isEnabled |
| NewsMobile/NewsMobile/Models/NewsModels.swift | WeatherData | entry/src/main/ets/models/news/WeatherData.ets | WeatherData | 已实现 | 数据类，含 temperature、humidity、feelsLike、iconCode |
| NewsMobile/NewsMobile/Models/NewsModels.swift | UserPreference | entry/src/main/ets/models/news/UserPreference.ets | UserPreference | 已实现 | 数据类，含 categoryWeights、sourceWeights、entityWeights |
| NewsMobile/NewsMobile/Models/NewsModels.swift | NewsMobileSettings | entry/src/main/ets/models/settings/NewsMobileSettings.ets | NewsMobileSettings | 已实现 | 数据类，含所有设置字段 |
| NewsMobile/NewsMobile/Services/NewsAggregator.swift | NewsAggregator | entry/src/main/ets/services/news/NewsAggregator.ets | NewsAggregator | 已实现 | 单例服务，实现 fetchAllNews/refresh/articles/forCategory |
| NewsMobile/NewsMobile/Services/RSSParser.swift | RSSParser | entry/src/main/ets/services/rss/RssParser.ets | RssParser | 已实现 | 工具类，实现 parse/parseRSS/parseAtom |
| NewsMobile/NewsMobile/Services/ContentFilter.swift | ContentFilter | entry/src/main/ets/services/news/ContentFilter.ets | ContentFilter | 已实现 | 工具类，实现内容过滤逻辑 |
| NewsMobile/NewsMobile/Services/CustomFeedManager.swift | CustomFeedManager | entry/src/main/ets/services/news/CustomFeedManager.ets | CustomFeedManager | 已实现 | 单例服务，实现 addFeed/removeFeed/toggleFeed/validateFeedURL/fetchAllCustomFeeds |
| NewsMobile/NewsMobile/Services/LocalNewsService.swift | LocalNewsService | entry/src/main/ets/services/news/LocalNewsService.ets | LocalNewsService | 已实现 | 单例服务，实现 fetchLocalNews/setLocation/clearLocation |
| NewsMobile/NewsMobile/Services/WeatherService.swift | WeatherService | entry/src/main/ets/services/weather/WeatherService.ets | WeatherService | 已实现 | 单例服务，实现 requestLocation/fetchWeather |
| NewsMobile/NewsMobile/Services/SettingsManager.swift | SettingsManager | entry/src/main/ets/stores/SettingsStore.ets | SettingsStore | 已实现 | store 模式，实现 settings/saveSettings/resetToDefaults |
| NewsMobile/NewsMobile/Services/WatchLaterManager.swift | WatchLaterManager | entry/src/main/ets/services/news/WatchLaterManager.ets + entry/src/main/ets/stores/WatchLaterStore.ets | WatchLaterManager + WatchLaterStore | 已实现 | 单例服务 + store，实现 add/remove/toggle/markAsRead/syncToCloud |
| NewsMobile/NewsMobile/Services/PersonalizationEngine.swift | PersonalizationEngine | entry/src/main/ets/services/personalization/PersonalizationEngine.ets | PersonalizationEngine | 已实现 | 静态方法，实现 updateFromFetch/recordView/resetProfile |
| NewsMobile/NewsMobile/ML/SentimentAnalyzer.swift | SentimentAnalyzer | entry/src/main/ets/services/nlp/SentimentAnalyzer.ets | SentimentAnalyzer | 已实现 | 启发式情绪分析 |
| NewsMobile/NewsMobile/ML/EntityExtractor.swift | EntityExtractor | entry/src/main/ets/services/nlp/EntityExtractor.ets | EntityExtractor | 已实现 | 正则实体提取 |
| NewsMobile/NewsMobile/Services/StoryClusterEngine.swift | StoryClusterEngine | entry/src/main/ets/services/ai/StoryClusterEngine.ets | StoryClusterEngine | 已实现 | 名词重叠聚类算法 |
| NewsMobile/NewsMobile/Services/TrendingTopicsEngine.swift | TrendingTopicsEngine | entry/src/main/ets/services/ai/TrendingTopicsEngine.ets | TrendingTopicsEngine | 已实现 | 实体频次统计 |
| NewsMobile/NewsMobile/Views/HomeView.swift | HomeView | entry/src/main/ets/pages/HomePage.ets | HomePage | 已实现 | 天气+趋势+分类+文章列表 |
| NewsMobile/NewsMobile/Views/ForYouView.swift | ForYouView | entry/src/main/ets/pages/ForYouPage.ets | ForYouPage | 已实现 | 个性化推荐流 |
| NewsMobile/NewsMobile/Views/SearchView.swift | SearchView | entry/src/main/ets/pages/SearchPage.ets | SearchPage | 已实现 | 搜索栏+结果列表 |
| NewsMobile/NewsMobile/Views/WatchLaterView.swift | WatchLaterView | entry/src/main/ets/pages/SavedPage.ets | SavedPage | 已实现 | 收藏列表 |
| NewsMobile/NewsMobile/Views/SettingsView.swift | SettingsView | entry/src/main/ets/pages/SettingsPage.ets | SettingsPage | 已实现 | 设置表单 |
| NewsMobile/NewsMobile/Views/ArticleDetailView.swift | ArticleDetailView | entry/src/main/ets/pages/ArticleDetailPage.ets | ArticleDetailPage | 已实现 | 文章详情 |
| NewsMobile/NewsMobile/Views/ArticleWebView.swift | ArticleWebView | entry/src/main/ets/pages/ArticleWebPage.ets | ArticleWebPage | 已实现 | WebView |
| NewsMobile/NewsMobile/Views/Components/ArticleCard.swift | ArticleCard | entry/src/main/ets/components/ArticleCard.ets | ArticleCard | 已实现 | 文章卡片 |
| NewsMobile/NewsMobile/Views/Components/TrendingBar.swift | TrendingBar | entry/src/main/ets/components/TrendingBar.ets | TrendingBar | 已实现 | 趋势横条 |
| NewsMobile/NewsMobile/Views/Components/WeatherWidget.swift | WeatherWidget | entry/src/main/ets/components/WeatherWidget.ets | WeatherWidget | 已实现 | 天气组件 |
| NewsMobile/NewsMobile/ContentView.swift | ContentView | entry/src/main/ets/pages/MainPage.ets | MainPage | 已实现 | 底部 Tabs 导航 |
| NewsMobile/NewsMobile/ContentView.swift | SnapshotSupport | entry/src/main/ets/fixtures/SnapshotFixtures.ets | SnapshotFixtures | 已实现 | 截图模式 |

## 函数级处置表

| iOS 函数 | Harmony 函数 | 状态 | 证据 |
|---|---|---|---|
| SnapshotSupport.prepare() | SnapshotFixtures.prepare(screen) | 已实现 | 按 SnapshotScreen 枚举注入固定数据到 stores |
| NewsAggregator.fetchAllNews() async | NewsAggregator.fetchAllNews(): Promise<void> | 已实现 | 抓取 RSS + 分析 + 过滤 + 个性化 |
| NewsAggregator.articles(for:) | NewsAggregator.articlesForCategory(category) | 已实现 | 按 NewsCategory 过滤 |
| NewsAggregator.refresh() async | NewsAggregator.refresh(): Promise<void> | 已实现 | 重新抓取 |
| SearchView.filteredArticles | SearchService.filterArticles(query, articles) | 已实现 | 标题/描述/来源匹配 |
| WatchLaterManager.toggle(_:) | WatchLaterManager.toggle(article) | 已实现 | 切换收藏 |
| WatchLaterManager.add(_:) | WatchLaterManager.add(article) | 已实现 | 添加收藏 |
| WatchLaterManager.remove(_:)/remove(at:) | WatchLaterManager.remove(id)/removeAt(index) | 已实现 | 删除收藏 |
| WatchLaterManager.markAsRead(_:) | WatchLaterManager.markAsRead(id) | 已实现 | 标记已读 |
| SettingsManager.saveSettings() | SettingsStore.save() | 已实现 | 持久化到 Preferences |
| SettingsManager.resetToDefaults() | SettingsStore.reset() | 已实现 | 恢复默认 |
| WeatherService.fetchWeather(for:) async | WeatherService.fetchWeather(lat, lon) | 已实现 | Open-Meteo API |
| SentimentAnalyzer.analyze(_:) | SentimentAnalyzer.analyze(text) | 已实现 | 启发式 |
| EntityExtractor.extract(from:) | EntityExtractor.extract(text) | 已实现 | 正则 |
| PersonalizationEngine.recordView(article:duration:) | PersonalizationEngine.recordView(article, duration) | 已实现 | 记录阅读行为 |
| PersonalizationEngine.updateFromFetch(articles:) | PersonalizationEngine.updateFromFetch(articles) | 已实现 | 排序推荐 |
| PersonalizationEngine.resetProfile() | PersonalizationEngine.resetProfile() | 已实现 | 重置偏好 |
| CustomFeedManager.addFeed(name:url:category:) | CustomFeedManager.addFeed(name, url, category) | 已实现 | 添加源 |
| CustomFeedManager.fetchAllCustomFeeds() async | CustomFeedManager.fetchAllCustomFeeds() | 已实现 | 抓取自定义源 |
| CustomFeedManager.removeFeed(...) | CustomFeedManager.removeFeed(id) | 已实现 | 删除源 |
| CustomFeedManager.toggleFeed(...) | CustomFeedManager.toggleFeed(id) | 已实现 | 切换源 |
| CustomFeedManager.validateFeedURL(...) | CustomFeedManager.validateFeedURL(url) | 已实现 | 验证 RSS |
| LocalNewsService.fetchLocalNews() async | LocalNewsService.fetchLocalNews() | 已实现 | Google News RSS |
| LocalNewsService.setLocation(...) | LocalNewsService.setLocation(location) | 已实现 | 设置位置 |
| LocalNewsService.clearLocation(...) | LocalNewsService.clearLocation() | 已实现 | 清除位置 |
| StoryClusterEngine.cluster(articles:) | StoryClusterEngine.cluster(articles) | 已实现 | 聚类算法 |
| TrendingTopicsEngine.analyze(articles:) | TrendingTopicsEngine.analyze(articles) | 已实现 | 频次分析 |

## 截图页面追踪

| iOS 页面 | Harmony 页面 | 状态 | 证据 |
|---|---|---|---|
| HomeView (screen.home.feed) | entry/src/main/ets/pages/HomePage.ets | 已实现 | WeatherWidget + TrendingBar + CategoryButton + ArticleCard 列表 |
| ArticleDetailView (screen.article.detail) | entry/src/main/ets/pages/ArticleDetailPage.ets | 已实现 | 详情 + SentimentBadge + EntityBadge + 收藏/听读/分享/阅读全文 |
| ArticleWebView (screen.article.webview) | entry/src/main/ets/pages/ArticleWebPage.ets | 已实现 | Web 组件 + LoadingProgress + Done/Share |
| ForYouView (screen.for_you.feed) | entry/src/main/ets/pages/ForYouPage.ets | 已实现 | 禁用态 + 空态 + 有数据态 |
| SearchView (screen.search.empty) | entry/src/main/ets/pages/SearchPage.ets | 已实现 | Search + 结果 + 高亮 + No Results |
| WatchLaterView (screen.saved.empty) | entry/src/main/ets/pages/SavedPage.ets | 已实现 | 收藏列表 + 未读圆点 + 滑动删除 + 空态 |
| SettingsView (screen.settings.root) | entry/src/main/ets/pages/SettingsPage.ets | 已实现 | Form 分区 + Toggle + Reset |

## 设置子页面实现记录

| 文件路径 | iOS 源文件 | 状态 | 说明 |
|---|---|---|---|
| entry/src/main/ets/pages/KeywordAlertsPage.ets | KeywordAlertsView.swift | 已实现 | 关键词管理 + 建议关键词 + 匹配文章列表 |
| entry/src/main/ets/pages/CustomFeedsPage.ets | CustomFeedsView.swift | 已实现 | 自定义 RSS 源管理 + 建议源 + 最近文章 |
| entry/src/main/ets/pages/AddFeedPage.ets | AddFeedView.swift | 已实现 | 添加 RSS 源表单 + URL 验证 + 分类选择 |
| entry/src/main/ets/pages/LocalNewsPage.ets | LocalNewsView.swift | 已实现 | 本地新闻列表 + 位置设置空态 + 加载态 |
| entry/src/main/ets/pages/LocationPickerPage.ets | LocationPickerView.swift | 已实现 | ZIP 输入 + 热门城市列表 + 清除位置 |
| entry/src/main/ets/pages/AudioBriefingPage.ets | AudioBriefingView.swift | 已实现 | 播放/暂停/上一条/下一条/停止控制面板 |
| entry/src/main/ets/pages/StoryClusterPage.ets | StoryClusterView.swift | 已实现 | 聚类列表 + 来源数 + 观点拆分 + 详情 |

## 平台适配层实现记录

| 文件路径 | iOS 能力 | 状态 | 说明 |
|---|---|---|---|
| entry/src/main/ets/platform/NotificationAdapter.ets | UNUserNotificationCenter | 已实现 | Notification Kit 封装，requestPermission/publishLocalNotification/cancel |
| entry/src/main/ets/platform/BackgroundRefreshAdapter.ets | BGTaskScheduler | 已实现 | 前台刷新为主路径，后台 best-effort，requestSuspendDelay |
| entry/src/main/ets/platform/TextToSpeechAdapter.ets | AVSpeechSynthesizer | 已实现 | Speech Kit TTS 封装，start/pause/resume/next/previous/stop 状态机 |
| entry/src/main/ets/platform/LocationAdapter.ets | CLLocationManager | 已实现 | Location Kit + ZIP/城市手动回退，getCurrentLocation/setManualZip |
| entry/src/main/ets/platform/WebViewAdapter.ets | WKWebView | 已实现 | ArkWeb WebviewController 封装 |
| entry/src/main/ets/platform/ShareAdapter.ets | ShareLink | 已实现 | 剪贴板复制回退，shareUrl/copyToClipboard |
| entry/src/main/ets/platform/CloudSyncAdapter.ets | NSUbiquitousKeyValueStore | 已实现 | 默认 no-op，isAvailable()=false，不阻塞本地持久化 |
| entry/src/main/ets/platform/SharedStorageAdapter.ets | App Group UserDefaults | 已实现 | Preferences 共享缓存，cacheHeadlines/cacheWeather/cacheTrending |
| entry/src/main/ets/platform/LocalApiAdapter.ets | NWListener | 已实现 | 本地回环 HTTP 服务，127.0.0.1:37436 |

## 服务层补充实现记录

| 文件路径 | iOS 源文件 | 状态 | 说明 |
|---|---|---|---|
| entry/src/main/ets/services/audio/TTSManager.ets | TTSManager.swift | 已实现 | startBriefing/pause/resume/next/previous/stop 状态机 + TextToSpeechAdapter |
| entry/src/main/ets/services/background/BackgroundRefreshManager.ets | BackgroundRefreshManager.swift | 已实现 | 前台定时刷新 + 后台任务注册 + 回调式刷新 |
| entry/src/main/ets/services/notification/NotificationManager.ets | NotificationManager.swift | 已实现 | requestPermission/sendBreakingNewsNotification/sendKeywordMatchNotification |
| entry/src/main/ets/services/notification/KeywordAlertManager.ets | KeywordAlertManager.swift | 已实现 | addAlert/removeAlert/toggleAlert/checkAlerts |
| entry/src/main/ets/services/sync/CloudSyncManager.ets | CloudSyncManager.swift | 已实现 | syncToCloud/syncFromCloud/no-op 适配器 |
| entry/src/main/ets/services/localapi/NovaApiServer.ets | NovaAPIServer.swift | 已实现 | start/stop/getStatus |
| entry/src/main/ets/services/card/WidgetDataManager.ets | WidgetDataManager.swift | 已实现 | updateWidgetData + 共享缓存读写 |
| entry/src/main/ets/services/system/SettingsManager.ets | SettingsManager.swift | 已实现 | load/save/resetToDefaults/updatePartial |

## 卡片/Widget 实现记录

| 文件路径 | iOS 源文件 | 状态 | 说明 |
|---|---|---|---|
| entry/src/main/ets/cards/NewsCard.ets | SmallNewsWidget/MediumNewsWidget/LargeNewsWidget | 已实现 | Form Kit 卡片，2x2/4x1/4x2 三种布局，渐变背景 |
| entry/src/main/ets/cards/NewsCardFormProvider.ets | NewsProvider/Widget Bundle | 已实现 | FormExtensionAbility，onAddForm/onUpdateForm/onCastToNormalForm |

## 集成配置记录

| 配置文件 | 修改内容 | 状态 |
|---|---|---|
| entry/src/main/resources/base/profile/main_pages.json | 注册全部 16 个页面路由 | 已实现 |
| entry/src/main/module.json5 | INTERNET/LOCATION/APPROXIMATELY_LOCATION/NOTIFICATION_CONTROLLER 权限 + NewsCardFormProvider extensionAbility | 已实现 |
| entry/src/main/resources/base/profile/form_config.json | 卡片配置 2*2/4*1/4*2 尺寸 + 30分钟刷新 | 已实现 |
| entry/src/main/resources/base/element/string.json | 权限说明字符串 | 已实现 |

## 平台能力追踪

| iOS 能力 | Harmony 适配层 | 状态 | 证据 |
|---|---|---|---|
| URLSession (network.urlsession) | entry/src/main/ets/services/news/HttpClient.ets | 已实现 | @ohos.net.http 封装 |
| XMLParser (parser.xmlparser) | entry/src/main/ets/services/rss/RssParser.ets | 已实现 | 正则式 RSS/Atom 解析 |
| NaturalLanguage NLTagger (ml.naturallanguage) | entry/src/main/ets/services/nlp/ | 已实现 | 启发式 + 正则 |
| UserDefaults (storage.userdefaults) | entry/src/main/ets/stores/PersistenceStore.ets | 已实现 | @ohos.data.preferences |
| SwiftUI TabView (ui.swiftui.tabview) | entry/src/main/ets/pages/MainPage.ets | 已实现 | ArkUI Tabs 组件 |
| SwiftUI .searchable (ui.swiftui.searchable) | entry/src/main/ets/pages/SearchPage.ets | 已实现 | ArkUI Search 组件 |
| UNUserNotificationCenter (notification.usernotifications) | entry/src/main/ets/platform/NotificationAdapter.ets | 已实现 | Notification Kit 封装 |
| BGTaskScheduler (background.bgapprefresh) | entry/src/main/ets/platform/BackgroundRefreshAdapter.ets | 已实现 | 前台刷新为主路径 |
| AVSpeechSynthesizer (audio.avspeech) | entry/src/main/ets/platform/TextToSpeechAdapter.ets | 已实现 | Speech Kit TTS 状态机 |
| CLLocationManager (location.corelocation) | entry/src/main/ets/platform/LocationAdapter.ets | 已实现 | Location Kit + ZIP/城市回退 |
| WKWebView (webview.webkit) | entry/src/main/ets/platform/WebViewAdapter.ets | 已实现 | ArkWeb 封装 |
| ShareLink (sharelink.system_share) | entry/src/main/ets/platform/ShareAdapter.ets | 已实现 | 剪贴板回退 |
| NSUbiquitousKeyValueStore (sync.icloud_kv) | entry/src/main/ets/platform/CloudSyncAdapter.ets | 已实现 | no-op 默认适配器 |
| App Group UserDefaults (storage.app_groups) | entry/src/main/ets/platform/SharedStorageAdapter.ets | 已实现 | Preferences 共享缓存 |
| WidgetKit (widget.widgetkit) | entry/src/main/ets/cards/NewsCard.ets + NewsCardFormProvider.ets | 已实现 | Form Kit 2x2/4x1/4x2 |
| NWListener (network.nwlistener) | entry/src/main/ets/platform/LocalApiAdapter.ets | 已实现 | 本地回环 HTTP |

## 截图页面追踪（完整）

| iOS 页面 | Harmony 页面 | 状态 | 证据 |
|---|---|---|---|
| HomeView (screen.home.feed) | entry/src/main/ets/pages/HomePage.ets | 已实现 | WeatherWidget + TrendingBar + CategoryButton + ArticleCard 列表 |
| ArticleDetailView (screen.article.detail) | entry/src/main/ets/pages/ArticleDetailPage.ets | 已实现 | 详情 + SentimentBadge + EntityBadge + 收藏/听读/分享/阅读全文 |
| ArticleWebView (screen.article.webview) | entry/src/main/ets/pages/ArticleWebPage.ets | 已实现 | Web 组件 + LoadingProgress + Done/Share |
| ForYouView (screen.for_you.feed) | entry/src/main/ets/pages/ForYouPage.ets | 已实现 | 禁用态 + 空态 + 有数据态 |
| SearchView (screen.search.empty) | entry/src/main/ets/pages/SearchPage.ets | 已实现 | Search + 结果 + 高亮 + No Results |
| WatchLaterView (screen.saved.empty) | entry/src/main/ets/pages/SavedPage.ets | 已实现 | 收藏列表 + 未读圆点 + 滑动删除 + 空态 |
| SettingsView (screen.settings.root) | entry/src/main/ets/pages/SettingsPage.ets | 已实现 | Form 分区 + Toggle + Reset |
| KeywordAlertsView (screen.keyword_alerts.list) | entry/src/main/ets/pages/KeywordAlertsPage.ets | 已实现 | 关键词管理 + 建议关键词 + 匹配文章 |
| CustomFeedsView (screen.custom_feeds.list) | entry/src/main/ets/pages/CustomFeedsPage.ets | 已实现 | 自定义源列表 + 建议源 + 最近文章 |
| AddFeedView (screen.custom_feeds.add) | entry/src/main/ets/pages/AddFeedPage.ets | 已实现 | 添加表单 + URL 验证 + 分类选择 |
| LocalNewsView (screen.local_news.setup/list) | entry/src/main/ets/pages/LocalNewsPage.ets | 已实现 | 位置设置空态 + 加载态 + 文章列表 |
| LocationPickerView (screen.local_news.location_picker) | entry/src/main/ets/pages/LocationPickerPage.ets | 已实现 | ZIP 输入 + 热门城市 + 清除位置 |
| AudioBriefingView (screen.audio.briefing) | entry/src/main/ets/pages/AudioBriefingPage.ets | 已实现 | 播放控制面板 + 进度 |
| StoryClusterView (screen.story_clusters.list) | entry/src/main/ets/pages/StoryClusterPage.ets | 已实现 | 聚类列表 + 观点拆分 + 详情 |
| SmallNewsWidget (screen.widget.small) | entry/src/main/ets/cards/NewsCard.ets Card2x2 | 已实现 | 2x2 渐变卡片 |
| MediumNewsWidget (screen.widget.medium) | entry/src/main/ets/cards/NewsCard.ets Card4x1 | 已实现 | 4x1 渐变卡片 |
| LargeNewsWidget (screen.widget.large) | entry/src/main/ets/cards/NewsCard.ets Card4x2 | 已实现 | 4x2 渐变卡片 + 标题列表 |

## Feature 覆盖汇总

| Feature ID | 状态 | 涉及文件 |
|---|---|---|
| feature.app.root_navigation | 已实现 | MainPage.ets, SnapshotSupport.ets |
| feature.news.home_feed | 已实现 | HomePage.ets, NewsAggregator.ets, HttpClient.ets, RssParser.ets, ArticleCard.ets, TrendingBar.ets, WeatherWidget.ets, CategoryButton.ets |
| feature.news.category_feed | 已实现 | HomePage.ets, NewsAggregator.ets, CategoryButton.ets, ArticleCard.ets |
| feature.news.article_detail | 已实现 | ArticleDetailPage.ets, WatchLaterManager.ets, TTSManager.ets, PersonalizationEngine.ets, SentimentBadge.ets, EntityBadge.ets |
| feature.news.web_reader | 已实现 | ArticleWebPage.ets, WebViewAdapter.ets, ShareAdapter.ets |
| feature.personalization.for_you | 已实现 | ForYouPage.ets, PersonalizationEngine.ets |
| feature.search.article_search | 已实现 | SearchPage.ets, SearchService.ets, SearchResultRow.ets |
| feature.watch_later.manage_saved | 已实现 | SavedPage.ets, WatchLaterManager.ets, CloudSyncManager.ets, WatchLaterRow.ets |
| feature.settings.preferences | 已实现 | SettingsPage.ets, SettingsManager.ets |
| feature.notifications.breaking_keyword | 已实现 | KeywordAlertsPage.ets, SettingsPage.ets, NotificationManager.ets, KeywordAlertManager.ets, NotificationAdapter.ets |
| feature.audio.briefing | 已实现 | AudioBriefingPage.ets, ArticleDetailPage.ets, TTSManager.ets, TextToSpeechAdapter.ets |
| feature.custom_feeds.manage_feeds | 已实现 | CustomFeedsPage.ets, AddFeedPage.ets, CustomFeedManager.ets |
| feature.local_news.location_feed | 已实现 | LocalNewsPage.ets, LocationPickerPage.ets, LocalNewsService.ets, LocationAdapter.ets |
| feature.weather.current_conditions | 已实现 | HomePage.ets, WeatherService.ets, WeatherWidget.ets, LocationAdapter.ets |
| feature.ml.sentiment_entities | 已实现 | ArticleDetailPage.ets, HomePage.ets, SentimentAnalyzer.ets, EntityExtractor.ets, SentimentBadge.ets, EntityBadge.ets |
| feature.ml.story_clusters | 已实现 | StoryClusterPage.ets, StoryClusterEngine.ets |
| feature.ml.trending_topics | 已实现 | HomePage.ets, TrendingTopicsEngine.ets, TrendingBar.ets |
| feature.sync.icloud | 已实现 | SettingsPage.ets, CloudSyncManager.ets, CloudSyncAdapter.ets |
| feature.background.refresh | 已实现 | SettingsPage.ets, BackgroundRefreshManager.ets, BackgroundRefreshAdapter.ets |
| feature.widget.home_screen | 已实现 | NewsCard.ets, NewsCardFormProvider.ets, WidgetDataManager.ets, SharedStorageAdapter.ets |
| feature.local_api.status | 已实现 | NovaApiServer.ets, LocalApiAdapter.ets |
| feature.snapshot.sample_data | 已实现 | SnapshotSupport.ets, SampleData.ets, SnapshotFixtures.ets |

## 总文件统计

- 总计 .ets 文件: 87
- models: 14 个
- stores: 6 个
- services: 21 个
- platform: 9 个
- pages: 16 个
- components: 9 个
- cards: 2 个
- fixtures: 2 个
- support: 3 个
- common: 1 个
- entryability: 2 个

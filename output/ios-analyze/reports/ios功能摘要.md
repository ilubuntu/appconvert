# iOS 功能摘要

| 一级功能 | 二级功能 | 三级功能 | Feature ID | 页面 | 数据来源 | iOS 源码 | 优先级 |
|---|---|---|---|---|---|---|---|
| 应用框架 | 主导航 | 五个底部 Tab 的根导航 | `feature.app.root_navigation` | Home / For You / Search / Saved / Settings | EnvironmentObject / Snapshot 样例数据 | `ContentView.swift` | high |
| 新闻浏览 | 首页信息流 | 新闻列表加载与展示 | `feature.news.home_feed` | 首页 | RSS / 固定样例数据 | `HomeView.swift`, `NewsAggregator.swift` | high |
| 新闻浏览 | 分类浏览 | 按新闻分类筛选列表 | `feature.news.category_feed` | 首页分类 | `articlesByCategory` | `HomeView.swift`, `NewsModels.swift` | high |
| 新闻浏览 | 文章详情 | 详情阅读、收藏、听读和分享 | `feature.news.article_detail` | 文章详情 | 选中文章 | `ArticleDetailView.swift` | high |
| 新闻浏览 | 阅读全文 | 内嵌 WebView 打开原文链接 | `feature.news.web_reader` | WebView | URLRequest | `ArticleWebView.swift` | high |
| 个性化 | For You 推荐 | 基于阅读行为的推荐信息流 | `feature.personalization.for_you` | For You | 阅读偏好 / 文章列表 | `ForYouView.swift`, `PersonalizationEngine.swift` | high |
| 检索 | 文章搜索 | 按标题、摘要和来源搜索 | `feature.search.article_search` | Search | 已加载文章 | `SearchView.swift` | high |
| 个人内容 | 稍后阅读 | 收藏、阅读状态和删除 | `feature.watch_later.manage_saved` | Saved | UserDefaults / iCloud | `WatchLaterView.swift`, `WatchLaterManager.swift` | high |
| 设置 | 用户偏好 | 显示、音频、个性化、过滤、同步、后台刷新和天气设置 | `feature.settings.preferences` | Settings | UserDefaults | `SettingsView.swift`, `SettingsManager.swift` | high |
| 提醒 | 通知和关键词 | 突发新闻通知与关键词命中管理 | `feature.notifications.breaking_keyword` | Settings / Keyword Alerts | `keywordAlerts` / UserNotifications | `KeywordAlertsView.swift`, `NotificationManager.swift` | medium |
| 音频 | 新闻播报 | TTS 播放、暂停、上一条和下一条 | `feature.audio.briefing` | Audio Briefing | 文章列表 | `AudioBriefingView.swift`, `TTSManager.swift` | medium |
| 订阅源 | 自定义 RSS | 添加、启停、删除和刷新自定义源 | `feature.custom_feeds.manage_feeds` | Custom Feeds | 自定义 RSS URL | `CustomFeedsView.swift`, `CustomFeedManager.swift` | medium |
| 本地新闻 | 位置新闻 | 按 ZIP 或城市获取本地新闻 | `feature.local_news.location_feed` | Local News | Google News RSS / 城市列表 | `LocalNewsView.swift`, `LocalNewsService.swift` | medium |
| 天气 | 当前天气 | 定位和 Open-Meteo 当前天气组件 | `feature.weather.current_conditions` | Home | CoreLocation / Open-Meteo | `WeatherWidget.swift`, `WeatherService.swift` | medium |
| 智能分析 | 情绪和实体 | 文章标题情绪评分和命名实体提取 | `feature.ml.sentiment_entities` | 首页 / 详情 | NaturalLanguage | `SentimentAnalyzer.swift`, `EntityExtractor.swift` | medium |
| 智能分析 | 故事聚类 | 多来源相关文章聚合和观点拆分 | `feature.ml.story_clusters` | StoryCluster | 本地算法 | `StoryClusterView.swift`, `StoryClusterEngine.swift` | low |
| 智能分析 | 趋势话题 | 实体频次和热门话题横条 | `feature.ml.trending_topics` | 首页 | 本地算法 | `TrendingBar.swift`, `TrendingTopicsEngine.swift` | medium |
| 同步 | iCloud 同步 | 设置和收藏的云端同步 | `feature.sync.icloud` | Settings | NSUbiquitousKeyValueStore | `CloudSyncManager.swift` | medium |
| 后台能力 | 后台刷新 | 定时刷新新闻源 | `feature.background.refresh` | Settings | BGAppRefreshTask | `BackgroundRefreshManager.swift` | medium |
| 扩展 | 桌面组件 | 小/中/大新闻 Widget | `feature.widget.home_screen` | Widget | App Group cache | `NewsMobileWidget.swift` | low |
| 本地接口 | Loopback API | 本地状态和 ping 接口 | `feature.local_api.status` | 无页面 | NWListener | `NovaAPIServer.swift` | low |
| 测试支撑 | 截图样例数据 | 启动参数直达页面和固定样例数据 | `feature.snapshot.sample_data` | 多页面 | SnapshotSupport.sampleArticles | `ContentView.swift` | medium |

后续模型应以 `features.json` 为主输入，按 feature id 读取关联模块、函数、页面、能力和资源。

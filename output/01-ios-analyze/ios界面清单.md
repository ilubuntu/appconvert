# iOS 界面清单

截图均来自 `SnapshotSupport` 的自动启动参数分支；未进行人工点击。

## 01-home.png 首页新闻流
- screen：`home`
- 截图：`output/01-ios-analyze/screenshots/png/01-home.png`（1320x2868，sha256 `14012e029e90c1f07641ded504f4f8a455491491fe6fe4398ee1fc68d6606f66`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen home`
- 界面源码：`NewsMobile/NewsMobile/Views/HomeView.swift` -> `HomeView` -> `body, categoryPicker`

## 02-home-category.png 分类新闻页
- screen：`homeCategory`
- 截图：`output/01-ios-analyze/screenshots/png/02-home-category.png`（1320x2868，sha256 `3bbf036cdfd1c533d121cc3e453c86258ac25cb8b1f986a70879b5b0040b9cd7`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen homeCategory`
- 界面源码：`NewsMobile/NewsMobile/Views/CategoryView.swift` -> `CategoryView` -> `body`

## 03-article-detail.png 文章详情
- screen：`articleDetail`
- 截图：`output/01-ios-analyze/screenshots/png/03-article-detail.png`（1320x2868，sha256 `2499265b81263fc0243b8619df26e057b6ceccfb12e833de31ba22e75e8402d5`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen articleDetail`
- 界面源码：`NewsMobile/NewsMobile/Views/ArticleDetailView.swift` -> `ArticleDetailView` -> `body, SentimentBadge, BiasIndicatorBadge, EntityBadge`

## 04-article-webview.png 文章原文 WebView
- screen：`articleWebView`
- 截图：`output/01-ios-analyze/screenshots/png/04-article-webview.png`（1320x2868，sha256 `8910c9e4b90afe43a6b471b6fadcba1fac736414ff094908e075fb4628fd44e4`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen articleWebView`
- 界面源码：`NewsMobile/NewsMobile/Views/ArticleWebView.swift` -> `ArticleWebView/WebView` -> `body, makeUIView, updateUIView, Coordinator`

## 05-for-you.png For You 推荐流
- screen：`forYou`
- 截图：`output/01-ios-analyze/screenshots/png/05-for-you.png`（1320x2868，sha256 `5ced0f9f7253bdff55c1e1c9285554b384e1e7662b6c1d2cb0604169ea3dc8aa`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen forYou`
- 界面源码：`NewsMobile/NewsMobile/Views/ForYouView.swift` -> `ForYouView` -> `body, disabledView, emptyView, articlesList`

## 06-search-empty.png 搜索空态
- screen：`searchEmpty`
- 截图：`output/01-ios-analyze/screenshots/png/06-search-empty.png`（1320x2868，sha256 `e0449de3b37e72e6beb1b2f3fb736c91bbe4029c48fc590c4f1ef5a35372ee0c`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen searchEmpty`
- 界面源码：`NewsMobile/NewsMobile/Views/SearchView.swift` -> `SearchView` -> `body, emptySearchView`

## 07-search-results.png 搜索结果
- screen：`searchResults`
- 截图：`output/01-ios-analyze/screenshots/png/07-search-results.png`（1320x2868，sha256 `25ab429f34903c991edec551aa16d64341d274a00948b98fe0c15fcd8bf34cf2`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen searchResults`
- 界面源码：`NewsMobile/NewsMobile/Views/SearchView.swift` -> `SearchView/SearchResultRow` -> `filteredArticles, resultsList, highlightedTitle`

## 08-saved-empty.png 收藏空态
- screen：`savedEmpty`
- 截图：`output/01-ios-analyze/screenshots/png/08-saved-empty.png`（1320x2868，sha256 `07695304432ae3d46c20e774fb5f881fa5cc83162dec0a391a9e770ec6281bb5`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen savedEmpty`
- 界面源码：`NewsMobile/NewsMobile/Views/WatchLaterView.swift` -> `WatchLaterView` -> `body, emptyView`

## 09-saved-with-article.png 收藏有数据
- screen：`savedWithArticle`
- 截图：`output/01-ios-analyze/screenshots/png/09-saved-with-article.png`（1320x2868，sha256 `0c6c7783a664bc7065b2e377e5f1f7497513332e5aee47e9cdc1e6ef71ea5b58`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen savedWithArticle`
- 界面源码：`NewsMobile/NewsMobile/Views/WatchLaterView.swift` -> `WatchLaterView/WatchLaterRow` -> `articlesList, WatchLaterRow.body`

## 10-settings.png 设置页
- screen：`settings`
- 截图：`output/01-ios-analyze/screenshots/png/10-settings.png`（1320x2868，sha256 `cefd1896c97e6fb55af9688d484e86fd7f7abbf8e640f843f9d89dec102e9dc2`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen settings`
- 界面源码：`NewsMobile/NewsMobile/Views/SettingsView.swift` -> `SettingsView` -> `body`

## 11-keyword-alerts.png 关键词提醒
- screen：`keywordAlerts`
- 截图：`output/01-ios-analyze/screenshots/png/11-keyword-alerts.png`（1320x2868，sha256 `a6cd83a29b45ed29f19ca5074868eb85b44129112274a9d0bafb757384b290b3`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen keywordAlerts`
- 界面源码：`NewsMobile/NewsMobile/Views/KeywordAlertsView.swift` -> `KeywordAlertsView` -> `body, KeywordRow.body`

## 12-custom-feeds.png 自定义订阅源
- screen：`customFeeds`
- 截图：`output/01-ios-analyze/screenshots/png/12-custom-feeds.png`（1320x2868，sha256 `ce7a7272e3c05eaa039ab3ce0375073ed2280ecdabb8b5226f4156dd2e69181a`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen customFeeds`
- 界面源码：`NewsMobile/NewsMobile/Views/CustomFeedsView.swift` -> `CustomFeedsView/AddFeedView` -> `body, AddFeedView.addFeed`

## 13-local-news.png 本地新闻
- screen：`localNews`
- 截图：`output/01-ios-analyze/screenshots/png/13-local-news.png`（1320x2868，sha256 `7e8c7acac3bbd385b2c8830fc47585477e567da8f5e9bf78c04de00e84aedd54`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen localNews`
- 界面源码：`NewsMobile/NewsMobile/Views/LocalNewsView.swift` -> `LocalNewsView/LocationPickerView` -> `body, setupView, articlesList`

## 14-audio-briefing.png 语音播报
- screen：`audioBriefing`
- 截图：`output/01-ios-analyze/screenshots/png/14-audio-briefing.png`（1320x2868，sha256 `2a60a58dc427c61ed37fecaa57bdd52deb01450133e6c2be44cfa9397972a4e2`）
- 启动参数：`-uiSnapshotMode true -snapshotScreen audioBriefing`
- 界面源码：`NewsMobile/NewsMobile/Views/AudioBriefingView.swift` -> `AudioBriefingView` -> `body`

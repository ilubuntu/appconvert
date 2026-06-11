# iOS 界面摘要

| Screen ID | 页面 | iOS View | 关联功能 | 截图建议 |
|---|---|---|---|---|
| `screen.home.feed` | 首页新闻流 | `HomeView` | 首页、分类、趋势、天气 | 必需 |
| `screen.home.category` | 分类新闻流 | `HomeView.CategoryButton` | 分类浏览 | 可选 |
| `screen.article.detail` | 文章详情 | `ArticleDetailView` | 详情、收藏、听读、分享 | 必需 |
| `screen.article.webview` | 文章 WebView | `ArticleWebView` | 阅读全文 | 必需 |
| `screen.for_you.feed` | For You 推荐 | `ForYouView` | 个性化推荐 | 必需 |
| `screen.for_you.empty` | For You 空态 | `ForYouView` | 个性化推荐 | 可选 |
| `screen.for_you.disabled` | For You 禁用态 | `ForYouView` | 个性化推荐 | 可选 |
| `screen.search.empty` | 搜索空态 | `SearchView` | 文章搜索 | 必需 |
| `screen.search.results` | 搜索结果 | `SearchView` | 文章搜索 | 可选 |
| `screen.search.no_results` | 搜索无结果 | `SearchView` | 文章搜索 | 可选 |
| `screen.saved.empty` | Saved 空态 | `WatchLaterView` | 稍后阅读 | 必需 |
| `screen.saved.list` | Saved 列表 | `WatchLaterView` | 稍后阅读 | 可选 |
| `screen.settings.root` | 设置中心 | `SettingsView` | 设置、通知、同步、后台、天气 | 必需 |
| `screen.keyword_alerts.list` | 关键词提醒 | `KeywordAlertsView` | 关键词提醒 | 可选 |
| `screen.keyword_alerts.matches` | 关键词匹配结果 | `KeywordMatchesView` | 关键词提醒 | 可选 |
| `screen.custom_feeds.list` | 自定义订阅源 | `CustomFeedsView` | 自定义 RSS | 可选 |
| `screen.custom_feeds.add` | 添加订阅源 | `AddFeedView` | 自定义 RSS | 可选 |
| `screen.local_news.setup` | 本地新闻 | `LocalNewsView` | 本地新闻 | 可选 |
| `screen.local_news.list` | 本地新闻列表 | `LocalNewsView` | 本地新闻 | 可选 |
| `screen.local_news.location_picker` | 位置选择 | `LocationPickerView` | 本地新闻 | 可选 |
| `screen.audio.briefing` | 音频播报 | `AudioBriefingView` | TTS | 可选 |
| `screen.story_clusters.list` | 故事聚类 | `StoryClusterView` | 聚类 | 可选 |
| `screen.widget.small` | 小组件 | `SmallNewsWidget` | Widget | 可选 |
| `screen.widget.medium` | 中组件 | `MediumNewsWidget` | Widget | 可选 |
| `screen.widget.large` | 大组件 | `LargeNewsWidget` | Widget | 可选 |

本次没有采集截图，`screens.json` 中保留了动态截图计划。下一步如要做 UI 复刻，应优先采集 `screenshot_required=true` 的页面。

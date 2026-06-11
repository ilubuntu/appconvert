# NewsMobile iOS 到 HarmonyOS NEXT 能力映射

迁移口径：全量迁移。所有能力都进入当前迁移目标，每项能力必须给出鸿蒙侧落点；差异只区分为 `平台直迁`、`等价替代`、`配套服务`。

| iOS 能力 | 使用位置 | 行为 | HarmonyOS NEXT 方向 | 实现类型 | 实现备注 |
| --- | --- | --- | --- | --- | --- |
| SwiftUI `App` 生命周期 | `NewsMobileApp.swift` | 初始化共享状态、启动服务、注册后台任务、进入根页面 | Stage 模型，`EntryAbility` + ArkUI 根页面 | 平台直迁 | 在 `EntryAbility` 初始化服务；根页面承载 Tabs。 |
| SwiftUI `TabView` | `ContentView.swift` | Home / For You / Search / Saved / Settings 五 Tab | ArkUI `Tabs` / `TabContent` | 平台直迁 | 保留五 Tab 信息架构和图标语义。 |
| SwiftUI `NavigationStack` / `sheet` | 多个 `Views/*.swift` | 页面导航、弹窗式详情、设置子页 | ArkUI `Navigation` / 路由栈 / 弹窗容器 | 平台直迁 | 文章详情、WebView、设置子页都要保留入口。 |
| SwiftUI `Form` / `List` / `ScrollView` | `SettingsView`、`SearchView`、`WatchLaterView`、`HomeView` | 表单、列表、滚动内容 | ArkUI `List`、`Scroll`、自定义分组设置项 | 平台直迁 | 设置页保持分区密度；新闻卡片用自定义组件。 |
| SwiftUI `.searchable` | `SearchView.swift` | 本地文章搜索 | ArkUI 搜索框 + 本地过滤状态 | 等价替代 | 输入框绑定查询词，过滤标题、描述和来源。 |
| `URLSession` | `NewsAggregator`、`CustomFeedManager`、`LocalNewsService`、`WeatherService` | RSS、天气、本地新闻、自定义订阅源网络请求 | Harmony 网络请求能力 / HTTP 客户端 | 平台直迁 | 统一封装 `NetworkService`，支持超时、错误、重试和 fixture 兜底。 |
| `XMLParser` | `RSSParser.swift` | RSS/Atom XML 解析 | ArkTS XML 解析库或轻量 RSS 解析器 | 等价替代 | 保持 `NewsArticle` 字段：title、description、link、pubDate、source、category、imageURL。 |
| `UserDefaults` | `SettingsManager`、`WatchLaterManager`、`PersonalizationEngine` | 设置、收藏、个性化偏好本地持久化 | Preferences / 本地键值存储 | 平台直迁 | settings、saved articles、preference profile 独立 key 存储。 |
| `NSUbiquitousKeyValueStore` / iCloud KV | `WatchLaterManager`、`CloudSyncManager`、entitlements | 设置和收藏跨设备同步 | 云同步服务 / AGC 云数据库 / 自建同步 API | 配套服务 | 鸿蒙工程需要定义 `CloudSyncService` 接口；本地先落 Preferences，云侧通过适配器同步。 |
| App Groups | App 与 Widget entitlements | App 和 Widget 共享新闻数据 | AppStorage / 卡片数据共享机制 | 配套服务 | 为鸿蒙卡片准备共享数据写入模块，例如 `WidgetDataStore`。 |
| WidgetKit | `NewsMobileWidget/NewsMobileWidget.swift` | 小/中/大 Widget 展示头条、情感点、天气、趋势 | Harmony 卡片 / 元服务卡片能力 | 配套服务 | 需要生成卡片页面和卡片数据更新链路，不省略。 |
| BackgroundTasks `BGAppRefreshTask` | `BackgroundRefreshManager.swift` | 周期性后台刷新新闻 | 后台任务/代理提醒/系统调度能力 | 配套服务 | 实现后台刷新注册、调度、失败重试；若系统策略受限，记录配置要求。 |
| UserNotifications | `NotificationManager.swift`、`KeywordAlertManager.swift` | 通知授权、突发新闻、关键词提醒 | Notification Kit / 通知能力 | 平台直迁 | 实现授权、即时通知、关键词匹配通知、badge/清理等对应行为。 |
| APS entitlement | `NewsMobile.entitlements` | APNs development 标识 | 推送服务配置 / 本地通知替代远程推送 | 配套服务 | 原项目主要是本地通知；如要远程推送，需要鸿蒙推送服务配置。 |
| CoreLocation | `WeatherService.swift` | 请求定位，获取经纬度用于天气 | Location Kit / 位置能力 | 平台直迁 | 实现定位授权、当前位置、失败态；天气卡片依赖该服务。 |
| Open-Meteo API | `WeatherService.swift` | 根据经纬度获取天气 | Harmony HTTP + Open-Meteo 请求 | 平台直迁 | 无 API Key；保留 temperature、condition、humidity、feelsLike。 |
| WebKit / `WKWebView` | `ArticleWebView.swift` | 应用内打开新闻原文 URL | ArkUI Web 组件 | 平台直迁 | 保留加载态、关闭、分享入口。 |
| `AVSpeechSynthesizer` | `TTSManager.swift` | 朗读新闻来源、标题、摘要 | Text-to-Speech / 语音播报能力 | 平台直迁 | 实现播放、暂停、继续、上一条、下一条、停止和语速设置。 |
| `AVAudioSession` | `TTSManager.swift` | 配置音频播放类别和 duckOthers | 音频会话/媒体播放管理 | 等价替代 | 鸿蒙侧按系统音频焦点机制处理播放焦点和中断。 |
| NaturalLanguage `NLTagger` 情感分析 | `SentimentAnalyzer.swift` | 标题情感正/负/中性 | 端侧 NLP 能力或规则/模型服务 | 等价替代 | 需要保留情感 badge；可先实现词典/规则算法，再接端侧模型。 |
| NaturalLanguage 实体抽取 | `EntityExtractor.swift` | 抽取人名、组织、地点 | 端侧 NLP 能力或规则/模型服务 | 等价替代 | 需要保留 Mentioned 实体标签。 |
| NaturalLanguage 话题抽取 | `TrendingTopicsEngine.swift` | 统计热门实体和名词生成趋势话题 | 规则算法 / NLP 服务 | 等价替代 | 需要输出趋势 topic、数量、分类。 |
| Story clustering | `StoryClusterEngine.swift` | 按相似词聚合相关新闻，展示观点差异 | ArkTS 聚类算法 / NLP 服务 | 等价替代 | 保留聚类数据结构、source count、perspective breakdown。 |
| ShareLink | `ArticleDetailView`、`ArticleWebView` | 分享文章 URL | 系统分享能力 / share picker | 平台直迁 | 详情页和 WebView 均保留分享入口。 |
| Network / `NWListener` | `NovaAPIServer.swift` | 监听 `127.0.0.1:37436`，提供本地 API | 本地网络服务 / 应用内 HTTP 服务能力 | 配套服务 | 需要实现 `/api/status`、`/api/ping`；如系统不允许监听，提供等价本地调试接口。 |
| RSS 内置源 | `NewsAggregator.sources` | 16 个内置公开 RSS 源 | ArkTS 常量源列表 + RSS service | 平台直迁 | 保留分类、source bias、reliability。 |
| Custom feeds | `CustomFeedManager.swift` | 添加、校验、启停、刷新用户 RSS 源 | ArkTS 服务 + Preferences + RSS parser | 平台直迁 | Add Feed 表单、推荐源、Recent Articles 全部保留。 |
| Local News | `LocalNewsService.swift` | 城市/ZIP 转 Google News RSS 查询 | ArkTS 服务 + RSS parser | 平台直迁 | 保留 popularCities、设置/清除位置、本地新闻列表。 |
| Content filtering | `ContentFilter.swift` | 过滤广告、赞助、标题党、排除来源 | ArkTS 过滤规则 | 等价替代 | 规则和开关必须保留。 |
| AI backend manager | `AIBackendManager*.swift` | 检测本地 AI 后端、生成摘要/状态等扩展能力 | ArkTS AI 后端适配层 | 配套服务 | 定义后端接口；支持本地/远端 AI 服务配置和连接检测。 |
| XCTest 单元测试 | `NewsMobileTests.swift` | 模型、安全、性能测试 | Harmony 单元测试 / 工程测试 | 等价替代 | 鸿蒙工程需要补对应模型和服务测试。 |
| 截图模式 | `SnapshotSupport`、`capture_ios_snapshots.py` | 记录 UI 证据 | 鸿蒙侧也需要截图/预览验收脚本 | 等价替代 | 迁移完成后用同名页面截图做 iOS/Harmony 对比。 |

## 全量实现要求

- 主 App、卡片/Widget、云同步、后台刷新、本地 API、NLP 能力都属于迁移目标。
- 对需要平台开通或外部服务的能力，不标记为不做；必须实现工程侧接口、配置位和调用链，并在 `外部配套要求` 中说明。
- Harmony 工程生成阶段必须读取本文件，逐项追踪实现状态。

## 外部配套要求

- 云同步：需要选择 AGC 云数据库、云函数、自建 API 或其他同步服务。
- 远程推送：如果从本地通知扩展为远程推送，需要申请并配置鸿蒙推送服务。
- 卡片：需要按 Harmony 卡片机制创建卡片页面、卡片数据源和更新策略。
- 后台刷新：需要按目标 HarmonyOS NEXT API 版本确认后台任务策略和权限限制。
- 本地 API server：需要确认 HarmonyOS NEXT 对应用内监听 loopback HTTP 服务的限制；若不可行，提供等价调试接口。

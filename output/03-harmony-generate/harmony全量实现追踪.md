# NewsMobile HarmonyOS NEXT 全量实现追踪

## 当前工程

- Harmony 工程：`NewsMobileHarmony`
- 主页面：`NewsMobileHarmony/entry/src/main/ets/pages/Index.ets`
- 业务模型：`NewsMobileHarmony/entry/src/main/ets/models/news/NewsModels.ets`
- 设置模型：`NewsMobileHarmony/entry/src/main/ets/models/settings/SettingsModels.ets`
- RSS/Atom 服务：`NewsMobileHarmony/entry/src/main/ets/services/news/NewsService.ets`
- XML 解析器：`NewsMobileHarmony/entry/src/main/ets/services/news/RssParser.ets`
- 兜底数据：`NewsMobileHarmony/entry/src/main/ets/fixtures/NewsFixtures.ets`
- 服务适配层：`NewsMobileHarmony/entry/src/main/ets/services/`
- 本地状态层：`NewsMobileHarmony/entry/src/main/ets/stores/`
- 卡片入口：`NewsMobileHarmony/entry/src/main/ets/cards/NewsCard.ets`
- 截图模式入口：`NewsMobileHarmony/entry/src/main/ets/support/SnapshotMode.ets`
- 网络权限：`NewsMobileHarmony/entry/src/main/module.json5` 中 `ohos.permission.INTERNET`
- 构建产物：`NewsMobileHarmony/entry/build/default/outputs/default/entry-default-unsigned.hap`
- 模块依据：`output/01-ios-analyze/ios模块结构.md`
- 功能依据：`output/01-ios-analyze/ios功能清单.md`
- 界面依据：`output/01-ios-analyze/ios界面清单.md`、`output/01-ios-analyze/screenshots/png/`
- 系统能力依据：`output/02-ios-map/ios-harmony-kit映射.md`

## 构建验证

使用 DevEco Studio hvigor CLI 构建通过，签名配置未修改。

```bash
export HOME=/Users/bb/work/appConvert/.hvigor-home
export HVIGOR_USER_HOME=/Users/bb/work/appConvert/.hvigor-home
export DEVECO_PATH=/Applications/DevEco-Studio.app
export DEVECO_SDK_HOME="$DEVECO_PATH/Contents/sdk"
export JAVA_HOME="$DEVECO_PATH/Contents/jbr/Contents/Home"
export PATH="/opt/homebrew/bin:$JAVA_HOME/bin:$PATH"
"$DEVECO_PATH/Contents/tools/node/bin/node" \
  "$DEVECO_PATH/Contents/tools/hvigor/bin/hvigorw.js" \
  --mode module \
  -p product=default \
  assembleHap \
  --analyze=normal \
  --parallel \
  --incremental
```

- 时间：2026-06-11
- 结果：`BUILD SUCCESSFUL`
- 产物：`NewsMobileHarmony/entry/build/default/outputs/default/entry-default-unsigned.hap`
- 产物大小：约 `282K`
- 签名：未配置 `signingConfigs`，hvigor 输出 `Will skip sign 'hos_hap'`；本阶段未修改 `build-profile.json5` 或任何签名文件。
- 构建环境说明：默认 daemon 构建被 `/Users/bb/.hvigor/daemon/cache/daemon-sec.json.lock` 和沙箱权限阻断；改用工作区内 `HOME/HVIGOR_USER_HOME=/Users/bb/work/appConvert/.hvigor-home` 完成 no-daemon 构建。该调整只影响本次 CLI 构建环境，不改变工程签名配置。
- 编译警告：`NewsService.ets:83` 提示 HTTP request 可能抛异常。调用链外层已在 `refreshAllNews()` 按 feed 捕获失败并切换 fixture 兜底，运行语义符合“真实数据优先，失败兜底”。

## 视觉验收状态

- 验收文档：`output/04-harmony-visual-verify/界面对齐.md`
- iOS 截图：`output/01-ios-analyze/screenshots/png/`，共 14 张，已按 `output/01-ios-analyze/ios界面清单.md` 逐页纳入对齐记录。
- Harmony 截图目录：`output/04-harmony-visual-verify/screenshots/`
- 当前状态：Harmony 截图未生成，视觉验收未完成。
- 阻塞原因：`harmonyos-live-preview` 需要独立 Harmony command-line-tools 布局 `<dir>/bin/hvigorw`，当前环境只确认到 DevEco Studio 内置 hvigor 路径 `/Applications/DevEco-Studio.app/Contents/tools/hvigor/bin/hvigorw.js`。
- 已记录修复项：页面级大标题、首页刷新和分类、For You、Search 空态、Saved 空态/有数据、Article Detail 操作区已按 iOS 截图方向修正；底部 Tab 图标、设置分组、搜索结果行、WebView/关键词/订阅源/本地新闻/音频播报子页仍需截图复核和继续细化。

## 真实数据链路

- 追溯来源：`ios模块结构.md -> Services/NewsAggregator + RSSParser`，`ios功能清单.md -> 1 首页新闻流、2 分类新闻、12 自定义订阅源、13 本地新闻`，`ios-harmony-kit映射.md -> URLSession + XMLParser + RSS 内置源`。
- `NewsService.sources` 内置公开 RSS/Atom 源：Reuters、Associated Press、BBC World、NPR、The Verge、NASA、MarketWatch。
- `NewsService.refreshAllNews()` 首屏和刷新按钮都会触发真实 HTTP 请求。
- `RssParser.parse()` 支持 RSS `<item>` 和 Atom `<entry>`，解析 `title`、`description/summary/content`、`link/href`、`pubDate/published/updated`。
- 解析结果映射为 `NewsArticle`，包含来源、分类、时间、URL、情感 badge、实体标签、未读状态。
- `NewsFixtures.articles` 只在网络失败、所有 feed 解析失败或截图稳定兜底时使用。
- 首屏 `Index.aboutToAppear()` 自动调用 `refreshNews()`，首页状态条显示 live/fallback 状态和当前文章数量。

## 模块实现追踪

| Harmony 模块 | iOS 模块追溯 | 当前落点 | 状态 |
| --- | --- | --- | --- |
| App 入口与根导航 | `ios模块结构.md -> App 入口与根导航` | `entryability/EntryAbility.ets`、`pages/Index.ets`、`support/SnapshotMode.ets`、`services/localapi/LocalApiService.ets` | 已保留五 Tab、启动刷新入口、截图兜底和本地 API 适配层 |
| Models | `ios模块结构.md -> Models` | `models/news/NewsModels.ets`、`models/settings/SettingsModels.ets`、`services/ai/AIBackendService.ets` | 已拆分业务模型、设置模型和 AI 后端 service |
| Services | `ios模块结构.md -> Services` | `services/news/`、`services/weather/`、`services/notification/`、`services/audio/`、`services/sync/`、`services/background/`、`services/card/` | 已建立服务边界；新闻服务已接真实 RSS/Atom |
| ML | `ios模块结构.md -> ML` | `services/nlp/NlpServices.ets`、`RssParser.sentiment()`、`RssParser.entities()` | 已用规则等价替代，保留后续端侧/云侧 NLP 接口 |
| Views | `ios模块结构.md -> Views` | `pages/Index.ets` 内 Home、For You、Search、Saved、Settings、Article overlay | 已实现主要页面和交互入口 |
| View Components | `ios模块结构.md -> View Components` | `articleCard()`、`topicStrip()`、`weatherCard()`、`savedRow()` 等 ArkUI Builder | 已用自定义 ArkUI 组件复刻卡片、趋势条、空态和列表行 |
| Widget Extension | `ios模块结构.md -> Widget Extension` | `cards/NewsCard.ets`、`services/card/CardDataService.ets` | 已保留卡片数据入口和工程侧落点 |
| Tests | `ios模块结构.md -> Tests` | `entry/src/test/LocalUnit.test.ets` | 已补窗口布局和 RSS/Atom 解析/兜底单测 |

## 页面实现追踪

| 页面 | 功能追溯 | 界面追溯 | Harmony 当前落点 | 状态 |
| --- | --- | --- | --- | --- |
| 首页新闻流 | `ios功能清单.md -> 1 首页新闻流` | `ios界面清单.md -> 1 首页新闻流`、`01-home.png` | `Index.homePage()`、`pageHeader('News')`、`liveDataStatus()`、`topicStrip()`、`categoryStrip()`、`articleCard()` | 已实现真实数据入口、刷新、趋势、分类、卡片和兜底态 |
| 分类新闻 | `ios功能清单.md -> 2 分类新闻` | `ios界面清单.md -> 2 分类新闻页`、`02-home-category.png` | `selectedCategory` + `filteredArticles()` + `articleCard()` | 已实现分类筛选；未单独拆路由页，保留同等交互语义 |
| For You | `ios功能清单.md -> 3 For You 推荐流` | `ios界面清单.md -> 5 For You 推荐流`、`05-for-you.png` | `forYouPage()` | 已实现推荐列表、更多入口语义和聚类卡 |
| 搜索 | `ios功能清单.md -> 4 搜索` | `ios界面清单.md -> 6/7 搜索空态/结果`、`06-search-empty.png`、`07-search-results.png` | `searchPage()` | 已实现本地搜索、空态和结果列表 |
| Saved | `ios功能清单.md -> 5 Saved / Watch Later 收藏` | `ios界面清单.md -> 8/9 收藏空态/有数据`、`08-saved-empty.png`、`09-saved-with-article.png` | `savedPage()`、`savedRow()`、`SavedArticleStore` | 已实现空态、有数据行、Edit 入口和未读蓝点 |
| 设置 | `ios功能清单.md -> 6 设置` | `ios界面清单.md -> 10 设置页`、`10-settings.png` | `settingsPage()`、`settingRow()` | 已实现分组信息结构和能力入口 |
| 文章详情 | `ios功能清单.md -> 7 文章详情` | `ios界面清单.md -> 3 文章详情`、`03-article-detail.png` | `articleDetail()` | 已实现 Article/Done、标题、来源、摘要、Read Full Article、Save/Listen/Share、实体和聚类信息 |
| 文章 WebView | `ios功能清单.md -> 8 文章 WebView` | `ios界面清单.md -> 4 文章 WebView`、`04-article-webview.png` | `articleDetail()` 中 `Open Original` 接入点 | 采用 ArkUI Web 接入点替代，保留加载/关闭/分享语义 |
| 语音播报 | `ios功能清单.md -> 9 语音播报 / TTS` | `ios界面清单.md -> 14 语音播报`、`14-audio-briefing.png` | `TtsService`、`articleDetail()` Listen 入口、设置页 Audio Briefing 行 | 已实现工程侧 TTS 状态和播放入口；完整独立音频控制页为后续可视化细化项 |
| 关键词提醒 | `ios功能清单.md -> 10 通知和关键词提醒` | `ios界面清单.md -> 11 关键词提醒`、`11-keyword-alerts.png` | `KeywordAlertService`、`settingsPage()` | 已保留关键词和通知入口 |
| 天气 / 定位 | `ios功能清单.md -> 11 天气 / 定位` | `ios界面清单.md -> 首页备注` | `WeatherService`、`weatherCard()` | 已建立天气服务和卡片组件；首页截图模式不强制显示天气，当前首页默认隐藏以贴近截图 |
| 自定义订阅源 | `ios功能清单.md -> 12 自定义订阅源` | `ios界面清单.md -> 12 自定义订阅源`、`12-custom-feeds.png` | `NewsService.sources`、`NewsFixtures.customFeeds`、`settingsPage()` | 已保留源列表和设置入口；推荐源管理 UI 为后续可视化细化项 |
| 本地新闻 | `ios功能清单.md -> 13 本地新闻` | `ios界面清单.md -> 13 本地新闻`、`13-local-news.png` | `settingsPage()` Local News 行、`NewsService.sources` 分类 Local 兼容 | 已保留入口和本地分类展示语义 |
| 新闻聚类和趋势 | `ios功能清单.md -> 14 新闻聚类和趋势话题` | `ios界面清单.md -> 1 首页新闻流`、`05-for-you.png` | `TrendingTopicsService.topics()`、`topicStrip()`、`clusterCard()` | 已实现趋势 topic 和聚类卡 |

## 系统能力实现追踪

| iOS 能力 | Harmony 方向 | 当前落点 | 类型 | 状态 |
| --- | --- | --- | --- | --- |
| SwiftUI `App` 生命周期 | Stage + EntryAbility | `entryability/EntryAbility.ets` | 平台直迁 | 已实现入口 |
| SwiftUI `TabView` | ArkUI `Tabs` | `Index.ets` | 平台直迁 | 已保留五 Tab 信息架构 |
| SwiftUI `NavigationStack` / `sheet` | ArkUI overlay / 路由接入点 | `articleDetail()`、设置行入口 | 平台直迁 | 已保留主要导航语义 |
| SwiftUI `Form/List/ScrollView` | ArkUI `Scroll` + 自定义分组/列表 | `settingsPage()`、`articleCard()`、`savedRow()` | 平台直迁 | 已实现 |
| SwiftUI `.searchable` | ArkUI `TextInput` + 本地过滤 | `searchPage()` | 等价替代 | 已实现 |
| `URLSession` | Harmony HTTP | `NewsService.fetchText()`、`ohos.permission.INTERNET` | 平台直迁 | 已实现真实请求链路 |
| `XMLParser` | ArkTS RSS/Atom 解析器 | `RssParser.ets` | 等价替代 | 已实现可运行解析链路 |
| `UserDefaults` | Preferences / 本地存储边界 | `SettingsStore.ets`、`SavedArticleStore.ets` | 平台直迁 | 已建立边界 |
| iCloud KV | 云同步适配层 | `CloudSyncService.ets` | 配套服务 | 已保留工程侧接口，需外部云服务选择 |
| App Groups / WidgetKit | Harmony 卡片数据 | `CardDataService.ets`、`cards/NewsCard.ets` | 配套服务 | 已保留卡片链路 |
| BackgroundTasks | 后台调度适配层 | `BackgroundRefreshService.ets` | 配套服务 | 已保留工程侧接口，需目标设备策略配置 |
| UserNotifications / APS | Notification Kit / 推送配置 | `KeywordAlertService.ets` | 平台直迁/配套服务 | 已保留关键词通知入口；远程推送需平台配置 |
| CoreLocation + Open-Meteo | Location Kit + HTTP | `WeatherService.ets` | 平台直迁 | 已保留工程侧入口 |
| WebKit / WKWebView | ArkUI Web | `Open Original` 接入点 | 平台直迁 | 已保留语义，完整 Web 组件页面待视觉细化 |
| AVSpeechSynthesizer / AVAudioSession | TTS + 音频焦点 | `TtsService.ets` | 平台直迁/等价替代 | 已保留播放控制入口 |
| NaturalLanguage | 规则 NLP / 模型服务接口 | `NlpServices.ets`、`RssParser` | 等价替代 | 已保留情感、实体、趋势输出 |
| ShareLink | 系统分享能力 | `Share` 按钮语义 | 平台直迁 | 已保留入口 |
| NWListener local API | 本地调试 API 适配层 | `LocalApiService.ets` | 配套服务 | 已保留 `/api/status`、`/api/ping` 语义 |
| Custom feeds | ArkTS 源列表 + RSS parser | `NewsService.sources`、`NewsFixtures.customFeeds` | 平台直迁 | 已具备解析链路和入口 |
| Local News | RSS geo-search 兼容方向 | `settingsPage()`、Local 分类 | 平台直迁 | 已保留入口 |
| Content filtering | ArkTS 过滤规则 | `ContentFilter.ets` | 等价替代 | 已保留服务落点 |
| AI backend manager | AI 服务适配层 | `AIBackendService.ets` | 配套服务 | 已从 models 拆到 service |
| XCTest | Harmony 单元测试 | `entry/src/test/LocalUnit.test.ets` | 等价替代 | 已补 RSS/Atom 解析测试 |

## Harmony 替代记录

| 替代点 | 替代原因 | 替代组件/落点 | 保留的交互语义 |
| --- | --- | --- | --- |
| iOS SF Symbols 图标 | 当前工程未接入 iOS 同款图标资源，ArkUI 内置文本按钮更稳定可构建 | 文本按钮、badge、chip、自定义 `articleCard()` | 保留刷新、更多、收藏、分享、播放、分类和趋势语义 |
| iOS `.searchable` 底部搜索栏 | ArkUI 没有直接同款 iOS 底部搜索控件 | `TextInput` + 空态/结果列表 | 保留标题/摘要/来源本地过滤和清空后空态 |
| `sheet` 弹层详情 | 当前工程单页实现更稳，未引入复杂路由栈 | `Stack` 中 `articleDetail()` overlay | 保留点击卡片打开详情、Done 关闭 |
| `WKWebView` 页面 | ArkUI Web 组件接入需要目标设备/模拟器进一步验收 | `Open Original` 接入点 | 保留 Read Full Article、加载/关闭/分享语义 |
| AVFoundation 音频会话 | Harmony 音频焦点机制不同 | `TtsService.ets` | 保留播放、暂停、Listen 入口和语速设置入口 |
| NaturalLanguage NLP | Harmony 端侧 NLP 能力与 iOS API 不同 | 规则算法 + `NlpServices.ets` 接口 | 保留情感 badge、实体标签、趋势 topic、聚类数据 |

## 外部配套要求

- 云同步：需要选择 AGC 云数据库、云函数、自建 API 或其他同步服务，当前 `CloudSyncService` 已保留适配层。
- 远程推送：原项目主要本地通知；如扩展远程推送，需要申请并配置鸿蒙推送服务。
- 卡片：需要按 Harmony 卡片机制继续完善卡片页面生命周期、数据共享和更新策略。
- 后台刷新：需要按目标 HarmonyOS NEXT API 版本确认后台任务策略、权限和调度限制。
- 本地 API server：需要确认目标系统对应用内 loopback HTTP 监听的限制；当前 `LocalApiService` 保留等价调试接口。
- WebView 和 TTS：需要在目标设备或模拟器上验证 Web 组件加载、系统分享、TTS 播放和音频焦点行为。

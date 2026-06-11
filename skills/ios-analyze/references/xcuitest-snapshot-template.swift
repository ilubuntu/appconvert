import XCTest

final class AppSnapshotTests: XCTestCase {
    private var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = [
            "-uiSnapshotMode", "true",
            "-resetSnapshotState", "true"
        ]
        app.launch()
    }

    func testCaptureCoreScreens() throws {
        capture("01-home")

        tapIfExists("home.category.technology")
        capture("02-home-category")

        tapIfExists("home.articleCard.0")
        capture("03-article-detail")

        tapIfExists("article.openWebView")
        capture("04-article-webview")
        app.navigationBars.buttons.element(boundBy: 0).tap()
        app.navigationBars.buttons.element(boundBy: 0).tap()

        tapIfExists("tab.forYou")
        capture("05-for-you")

        tapIfExists("tab.search")
        capture("06-search-empty")
        let searchField = app.searchFields.firstMatch
        if searchField.waitForExistence(timeout: 2) {
            searchField.tap()
            searchField.typeText("climate")
        }
        capture("07-search-results")

        tapIfExists("tab.saved")
        capture("08-saved-empty")

        tapIfExists("tab.settings")
        capture("10-settings")

        tapIfExists("settings.keywordAlerts")
        capture("11-keyword-alerts")
        app.navigationBars.buttons.element(boundBy: 0).tap()

        tapIfExists("settings.customFeeds")
        capture("12-custom-feeds")
        app.navigationBars.buttons.element(boundBy: 0).tap()

        tapIfExists("settings.localNews")
        capture("13-local-news")
    }

    private func tapIfExists(_ identifier: String, timeout: TimeInterval = 5) {
        let element = app.descendants(matching: .any)[identifier]
        XCTAssertTrue(element.waitForExistence(timeout: timeout), "Missing UI element: \(identifier)")
        element.tap()
    }

    private func capture(_ name: String) {
        let attachment = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}

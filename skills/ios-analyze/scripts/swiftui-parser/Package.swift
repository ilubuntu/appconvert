// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "SwiftUIParser",
    platforms: [.macOS(.v14)],
    dependencies: [
        .package(url: "https://github.com/apple/swift-syntax.git", from: "600.0.0"),
    ],
    targets: [
        .executableTarget(
            name: "SwiftUIParser",
            dependencies: [
                .product(name: "SwiftSyntax", package: "swift-syntax"),
                .product(name: "SwiftParser", package: "swift-syntax"),
            ]
        )
    ]
)

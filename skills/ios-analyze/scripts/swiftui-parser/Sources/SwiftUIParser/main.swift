import Foundation
import SwiftSyntax
import SwiftParser

// MARK: - Known SwiftUI types

let containerTypes: Set<String> = [
    "VStack", "HStack", "ZStack", "ScrollView", "List", "LazyVStack", "LazyHStack",
    "LazyVGrid", "LazyHGrid", "NavigationStack", "NavigationView", "TabView",
    "Group", "Form", "Section", "Grid", "GridRow", "OutlineGroup",
    "DisclosureGroup", "ScrollViewReader", "HSplitView", "VSplitView"
]

let elementTypes: Set<String> = [
    "Text", "Image", "Button", "Toggle", "TextField", "SecureField", "Slider",
    "Stepper", "DatePicker", "Picker", "ProgressView", "Spacer", "Divider",
    "Label", "Link", "Menu", "NavigationLink", "AsyncImage", "ShareLink",
    "Color", "RoundedRectangle", "Capsule", "Circle", "Rectangle",
    "Ellipse", "Canvas", "Gauge"
]

let navigationModifiers: Set<String> = [
    "sheet", "fullScreenCover", "navigationTitle", "navigationBarTitle",
    "toolbar", "tabItem", "refreshable", "onAppear", "onDisappear",
    "navigationBarItems", "popover", "overlay", "background",
    "navigationBarTitleDisplayMode", "tabViewStyle", "onTapGesture",
    "onSubmit", "onChange", "onReceive", "task"
]

let styleModifiers: Set<String> = [
    "font", "foregroundColor", "foregroundStyle", "background",
    "padding", "frame", "cornerRadius", "clipShape", "shadow", "opacity",
    "border", "tint", "accentColor", "lineLimit", "multilineTextAlignment",
    "truncationMode", "italic", "bold", "strikethrough", "underline",
    "kerning", "tracking", "baselineOffset", "rotationEffect", "scaleEffect",
    "offset", "zIndex", "blur", "brightness", "contrast", "grayscale",
    "hueRotation", "saturation", "colorInvert", "colorMultiply",
    "aspectRatio", "ignoresSafeArea", "fixedSize",
    "layoutPriority", "position", "transformEffect"
]

// MARK: - Output model

struct ViewNode: Codable {
    var type: String
    var isContainer: Bool = false
    var isElement: Bool = false
    var isCustom: Bool = false
    var isConditional: Bool = false
    var isForEach: Bool = false
    var args: [String: ArgValue] = [:]
    var modifiers: [ModifierNode] = []
    var children: [ViewNode] = []
    var condition: String? = nil
    var forEachSource: String? = nil
    var forEachVar: String? = nil
    var stringLiteral: String? = nil
    var sfSymbol: String? = nil

    enum ArgValue: Codable {
        case string(String)
        case number(Double)
        case integer(Int)
        case boolean(Bool)
        case symbol(String)
        case enumValue(String)
        case other(String)

        func encode(to encoder: Encoder) throws {
            var c = encoder.singleValueContainer()
            switch self {
            case .string(let v): try c.encode(v)
            case .number(let v): try c.encode(v)
            case .integer(let v): try c.encode(v)
            case .boolean(let v): try c.encode(v)
            case .symbol(let v): try c.encode(v)
            case .enumValue(let v): try c.encode(v)
            case .other(let v): try c.encode(v)
            }
        }

        init(from decoder: Decoder) throws {
            let c = try decoder.singleValueContainer()
            if let v = try? c.decode(Bool.self) { self = .boolean(v) }
            else if let v = try? c.decode(Int.self) { self = .integer(v) }
            else if let v = try? c.decode(Double.self) { self = .number(v) }
            else if let v = try? c.decode(String.self) { self = .string(v) }
            else { self = .other("unknown") }
        }
    }
}

struct ModifierNode: Codable {
    var name: String
    var category: String
    var args: [String: ViewNode.ArgValue] = [:]
    var hasTrailingClosure: Bool = false
    var closureSummary: String? = nil
}

struct PropertyInfo: Codable {
    var name: String
    var decorator: String?
    var typeName: String
    var isBinding: Bool = false
}

struct ViewStruct: Codable {
    var name: String
    var file: String
    var conformances: [String] = []
    var properties: [PropertyInfo] = []
    var body: ViewNode? = nil
}

// MARK: - Helper: extract identifier text from pattern

func patternIdentifier(_ pattern: PatternSyntax) -> String {
    if let idPattern = pattern.as(IdentifierPatternSyntax.self) {
        return idPattern.identifier.text
    }
    return pattern.trimmedDescription
}

// MARK: - Parser

class SwiftUIExtractor {
    let filePath: String

    init(filePath: String) {
        self.filePath = filePath
    }

    func extract() throws -> [ViewStruct] {
        let url = URL(fileURLWithPath: filePath)
        let source = try String(contentsOf: url, encoding: .utf8)
        let tree = Parser.parse(source: source)

        let visitor = FileVisitor(filePath: filePath)
        visitor.walk(tree)
        return visitor.viewStructs
    }
}

// MARK: - Syntax walking

class FileVisitor: SyntaxAnyVisitor {
    let filePath: String
    var viewStructs: [ViewStruct] = []

    init(filePath: String) {
        self.filePath = filePath
        super.init(viewMode: .sourceAccurate)
    }

    override func visit(_ node: StructDeclSyntax) -> SyntaxVisitorContinueKind {
        let name = node.name.text
        let conformances = node.inheritanceClause.map { inh in
            inh.inheritedTypes.map { $0.type.trimmedDescription }
        } ?? []

        let isView = conformances.contains { $0.contains("View") }

        var props: [PropertyInfo] = []
        for member in node.memberBlock.members {
            guard let varDecl = member.decl.as(VariableDeclSyntax.self) else { continue }
            var decorator: String? = nil
            for attr in varDecl.attributes {
                switch attr {
                case .attribute(let a):
                    decorator = a.attributeName.trimmedDescription
                case .ifConfigDecl:
                    break
                }
            }
            for binding in varDecl.bindings {
                let propName = patternIdentifier(binding.pattern)
                if propName.isEmpty { continue }
                let typeName = binding.typeAnnotation?.type.trimmedDescription
                    ?? binding.initializer?.value.trimmedDescription ?? ""
                let isBinding = typeName.hasPrefix("$") || typeName.contains("Binding<")
                props.append(PropertyInfo(name: propName, decorator: decorator, typeName: typeName, isBinding: isBinding))
            }
        }

        var viewStruct = ViewStruct(name: name, file: filePath, conformances: conformances, properties: props)

        if isView {
            for member in node.memberBlock.members {
                guard let varDecl = member.decl.as(VariableDeclSyntax.self) else { continue }
                for binding in varDecl.bindings {
                    let propName = patternIdentifier(binding.pattern)
                    if propName != "body" { continue }
                    if let accessorBlock = binding.accessorBlock {
                        switch accessorBlock.accessors {
                        case .accessors(let accessorList):
                            for accessor in accessorList {
                                if accessor.accessorSpecifier.tokenKind == .keyword(.get) {
                                    if let body = accessor.body,
                                       let firstStmt = body.statements.first {
                                        viewStruct.body = extractViewNode(firstStmt.item)
                                    }
                                }
                            }
                        case .getter(let getterBody):
                            if let firstStmt = getterBody.statements.first {
                                viewStruct.body = extractViewNode(firstStmt.item)
                            }
                        }
                    } else if let initializer = binding.initializer {
                        viewStruct.body = extractViewNode(initializer.value)
                    }
                }
            }
        }

        viewStructs.append(viewStruct)
        return .visitChildren
    }

    // MARK: - Expression extraction

    func extractViewNode(_ item: SyntaxProtocol) -> ViewNode? {
        if let codeItem = item.as(CodeBlockItemSyntax.self) {
            return extractViewNode(codeItem.item)
        }
        if let expr = Syntax(item).as(ExprSyntax.self) {
            return extractExpr(expr)
        }
        let desc = item.trimmedDescription
        if desc.isEmpty { return nil }
        return ViewNode(type: "raw", args: ["source": .other(String(desc.prefix(200)))])
    }

    func extractExpr(_ expr: ExprSyntax) -> ViewNode? {
        if let ifExpr = expr.as(IfExprSyntax.self) {
            return extractConditional(ifExpr)
        }
        if let callExpr = expr.as(FunctionCallExprSyntax.self) {
            return extractFunctionCall(callExpr)
        }
        if let memberAccess = expr.as(MemberAccessExprSyntax.self) {
            return ViewNode(type: "value", args: ["value": .enumValue("." + memberAccess.declName.trimmedDescription)])
        }
        return ViewNode(type: "raw", args: ["source": .other(String(expr.trimmedDescription.prefix(200)))])
    }

    func extractFunctionCall(_ callExpr: FunctionCallExprSyntax) -> ViewNode {
        let called = callExpr.calledExpression

        // Modifier chain: base.modifierName(args)
        if let memberAccess = called.as(MemberAccessExprSyntax.self) {
            let modifierName = memberAccess.declName.trimmedDescription
            if let baseExpr = memberAccess.base, let baseCall = baseExpr.as(FunctionCallExprSyntax.self) {
                var node = extractFunctionCall(baseCall)
                let category = categorizeModifier(modifierName)
                var modifier = ModifierNode(name: modifierName, category: category)
                for arg in callExpr.arguments {
                    let label = arg.label?.text ?? "_"
                    modifier.args[label] = extractArgValue(arg.expression)
                }
                if let trailingClosure = callExpr.trailingClosure {
                    modifier.hasTrailingClosure = true
                    modifier.closureSummary = summarizeClosure(trailingClosure)
                }
                node.modifiers.append(modifier)
                return node
            }
        }

        // View constructor: ViewName(args) { closure }
        let typeName: String
        if let memberAccess = called.as(MemberAccessExprSyntax.self) {
            typeName = memberAccess.declName.trimmedDescription
        } else {
            typeName = called.trimmedDescription
        }

        var node = ViewNode(type: typeName)
        node.isContainer = containerTypes.contains(typeName)
        node.isElement = elementTypes.contains(typeName)
        node.isCustom = !node.isContainer && !node.isElement && (typeName.first?.isUppercase == true)

        if typeName == "ForEach" {
            node.isForEach = true
            let argList = Array(callExpr.arguments)
            if argList.count >= 1 {
                node.forEachSource = argList[0].expression.trimmedDescription
            }
            if argList.count >= 3 {
                node.forEachVar = argList[1].expression.trimmedDescription
            }
        }

        for arg in callExpr.arguments {
            let label = arg.label?.text ?? "_"
            let value = extractArgValue(arg.expression)
            node.args[label] = value
            if label == "systemName", case .string(let s) = value {
                node.sfSymbol = s
            }
            if case .string(let s) = value, node.stringLiteral == nil {
                node.stringLiteral = s
            }
        }

        if let trailingClosure = callExpr.trailingClosure {
            node.children.append(contentsOf: extractClosureChildren(trailingClosure))
        }

        return node
    }

    func extractConditional(_ ifExpr: IfExprSyntax) -> ViewNode {
        var node = ViewNode(type: "conditional", isConditional: true)
        node.condition = ifExpr.conditions.map { $0.trimmedDescription }.joined(separator: ", ")

        for stmt in ifExpr.body.statements {
            if let child = extractViewNode(stmt.item) {
                node.children.append(child)
            }
        }

        if let elseBody = ifExpr.elseBody {
            if let elseBlock = elseBody.as(CodeBlockSyntax.self) {
                for stmt in elseBlock.statements {
                    if let child = extractViewNode(stmt.item) {
                        var elseChild = child
                        elseChild.condition = "else"
                        node.children.append(elseChild)
                    }
                }
            } else if let elseIf = elseBody.as(IfExprSyntax.self) {
                var elseChild = extractConditional(elseIf)
                elseChild.condition = "else-if"
                node.children.append(elseChild)
            }
        }

        return node
    }

    func extractClosureChildren(_ closure: ClosureExprSyntax) -> [ViewNode] {
        var children: [ViewNode] = []
        for stmt in closure.statements {
            if let child = extractViewNode(stmt.item) {
                children.append(child)
            }
        }
        return children
    }

    func extractArgValue(_ expr: ExprSyntax) -> ViewNode.ArgValue {
        let trimmed = expr.trimmedDescription

        if let stringLit = expr.as(StringLiteralExprSyntax.self) {
            var value = ""
            for segment in stringLit.segments {
                if let strSeg = segment.as(StringSegmentSyntax.self) {
                    value += strSeg.content.text
                }
            }
            return .string(value)
        }

        if let intLit = expr.as(IntegerLiteralExprSyntax.self) {
            if let v = Int(intLit.literal.text) { return .integer(v) }
            return .other(trimmed)
        }

        if let floatLit = expr.as(FloatLiteralExprSyntax.self) {
            if let v = Double(floatLit.literal.text) { return .number(v) }
            return .other(trimmed)
        }

        if trimmed == "true" { return .boolean(true) }
        if trimmed == "false" { return .boolean(false) }

        if let memberAccess = expr.as(MemberAccessExprSyntax.self) {
            return .enumValue("." + memberAccess.declName.trimmedDescription)
        }

        // Color(hex: "FF9500") pattern
        if let callExpr = expr.as(FunctionCallExprSyntax.self) {
            if let memberAccess = callExpr.calledExpression.as(MemberAccessExprSyntax.self) {
                let funcName = memberAccess.declName.trimmedDescription
                if funcName == "hex" {
                    if let firstArg = callExpr.arguments.first {
                        let argVal = extractArgValue(firstArg.expression)
                        if case .string(let hex) = argVal {
                            let clean = hex.hasPrefix("#") ? hex : "#\(hex)"
                            return .string(clean)
                        }
                    }
                }
            }
        }

        if trimmed.hasPrefix("$") { return .symbol(trimmed) }

        return .other(String(trimmed.prefix(150)))
    }

    func summarizeClosure(_ closure: ClosureExprSyntax) -> String {
        let count = closure.statements.count
        if count == 0 { return "empty" }
        let firstStmt = closure.statements.first?.item.trimmedDescription ?? ""
        return "\(count) stmt(s): \(String(firstStmt.prefix(120)))"
    }

    func categorizeModifier(_ name: String) -> String {
        if navigationModifiers.contains(name) { return "navigation" }
        if styleModifiers.contains(name) { return "style" }
        return "other"
    }
}

// MARK: - Main

func main() throws {
    let args = CommandLine.arguments
    var projectRoot = "."
    var outputDir = "."
    var verbose = false
    var i = 1
    while i < args.count {
        switch args[i] {
        case "--project-root": projectRoot = args[i + 1]; i += 2
        case "--output-dir": outputDir = args[i + 1]; i += 2
        case "--verbose": verbose = true; i += 1
        default: i += 1
        }
    }

    let rootURL = URL(fileURLWithPath: projectRoot).resolvingSymlinks()
    let outputURL = URL(fileURLWithPath: outputDir).resolvingSymlinks()
    let fm = FileManager.default

    var swiftFiles: [URL] = []
    let excludedDirs: Set<String> = [".build", ".git", "build", "DerivedData", "Pods", "Carthage", ".swiftpm", "Tests", "NewsMobileTests", "NewsMobileWidget"]

    func walk(_ dir: URL) {
        guard let entries = try? fm.contentsOfDirectory(at: dir, includingPropertiesForKeys: nil) else { return }
        for entry in entries {
            let name = entry.lastPathComponent
            if excludedDirs.contains(name) { continue }
            var isDir: ObjCBool = false
            fm.fileExists(atPath: entry.path, isDirectory: &isDir)
            if isDir.boolValue {
                walk(entry)
            } else if name.hasSuffix(".swift") {
                swiftFiles.append(entry)
            }
        }
    }
    walk(rootURL)
    swiftFiles.sort()
    if verbose { print("Found \(swiftFiles.count) Swift files") }

    var allViews: [ViewStruct] = []
    var errors: [(String, String)] = []

    for fileURL in swiftFiles {
        let relative = fileURL.path.replacingOccurrences(of: rootURL.path + "/", with: "")
        let extractor = SwiftUIExtractor(filePath: fileURL.path)
        do {
            var views = try extractor.extract()
            for i in 0..<views.count { views[i].file = relative }
            allViews.append(contentsOf: views)
            if verbose { print("  Parsed \(relative): \(views.count) structs") }
        } catch {
            errors.append((relative, String(describing: error)))
        }
    }

    // Build output
    let viewsArray: [[String: Any]] = allViews.map { view in
        var dict: [String: Any] = [
            "name": view.name,
            "file": view.file,
            "conformances": view.conformances,
            "is_view": view.conformances.contains { $0.contains("View") },
        ]
        if !view.properties.isEmpty {
            dict["properties"] = view.properties.map { p -> [String: Any] in
                var d: [String: Any] = ["name": p.name, "type": p.typeName]
                if let dec = p.decorator { d["decorator"] = dec }
                if p.isBinding { d["is_binding"] = true }
                return d
            }
        }
        if let body = view.body {
            let encoder = JSONEncoder()
            if let data = try? encoder.encode(body),
               let bodyDict = try? JSONSerialization.jsonObject(with: data) {
                dict["body"] = bodyDict
            }
        }
        return dict
    }

    let output: [String: Any] = [
        "project_root": rootURL.path,
        "file_count": swiftFiles.count,
        "view_count": allViews.count,
        "error_count": errors.count,
        "views": viewsArray,
        "errors": errors.map { ["file": $0.0, "error": $0.1] },
    ]

    let scanDir = outputURL.appendingPathComponent("scan")
    try? fm.createDirectory(at: scanDir, withIntermediateDirectories: true)

    let outputPath = scanDir.appendingPathComponent("swiftui_view_tree.json")
    let data = try JSONSerialization.data(withJSONObject: output, options: [.prettyPrinted])
    try data.write(to: outputPath)

    print("Parsed \(allViews.count) structs from \(swiftFiles.count) files (\(errors.count) errors)")
    print("Output: \(outputPath.path)")
}

try main()

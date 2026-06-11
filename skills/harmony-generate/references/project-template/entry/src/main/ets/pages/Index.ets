@Entry
@Component
struct Index {
  @State message: string = 'Ready';

  build() {
    Column({ space: 16 }) {
      Text(this.message)
        .fontSize(24)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}

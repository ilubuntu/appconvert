export enum WindowSizeClass {
  COMPACT = 'compact',
  MEDIUM = 'medium',
  EXPANDED = 'expanded'
}

export interface LayoutPolicy {
  sizeClass: WindowSizeClass;
  columns: number;
  useSideNavigation: boolean;
}

export function getWindowSizeClass(widthVp: number): WindowSizeClass {
  if (widthVp >= 840) {
    return WindowSizeClass.EXPANDED;
  }

  if (widthVp >= 600) {
    return WindowSizeClass.MEDIUM;
  }

  return WindowSizeClass.COMPACT;
}

export function createLayoutPolicy(widthVp: number): LayoutPolicy {
  const sizeClass = getWindowSizeClass(widthVp);

  if (sizeClass === WindowSizeClass.EXPANDED) {
    return {
      sizeClass,
      columns: 3,
      useSideNavigation: true
    };
  }

  if (sizeClass === WindowSizeClass.MEDIUM) {
    return {
      sizeClass,
      columns: 2,
      useSideNavigation: true
    };
  }

  return {
    sizeClass,
    columns: 1,
    useSideNavigation: false
  };
}

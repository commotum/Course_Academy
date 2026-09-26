---
title: "Ribbon actions"
source: "https://docs.obsidian.md/Plugins/User+interface/Ribbon+actions"
author:
published:
created: 2026-05-05
description: "Home - Developer Documentation"
tags:
  - "clippings"
---
The sidebar on the left side of the Obsidian interface is mainly known as the *ribbon*. The purpose of the ribbon is to host actions defined by plugins.

To add an action to the ribbon, use the [addRibbonIcon()](https://docs.obsidian.md/Reference/TypeScript+API/Plugin/addRibbonIcon) method:

```ts
import { Plugin } from 'obsidian';

export default class ExamplePlugin extends Plugin {
  async onload() {
    this.addRibbonIcon('dice', 'Print to console', () => {
      console.log('Hello, you!');
    });
  }
}
```

The first argument specifies which icon to use. For more information on the available icons, and how to add your own, refer to [Icons](https://docs.obsidian.md/Plugins/User+interface/Icons).

> [!note] Note
> Users can remove your plugin's icon from the ribbon, or even opt to hide the ribbon entirely. Therefore it's advisable to include alternate ways of accessing functionality that's in the ribbon, such as creating a [command](https://docs.obsidian.md/Plugins/User+interface/Commands). It is also recommended that plugins do not add their own toggles for ribbon items.

Save
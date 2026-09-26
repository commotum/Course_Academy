---
title: "Embed files"
source: "https://help.obsidian.md/embeds"
author:
  - "[[Obsidian Help]]"
published:
created: 2026-01-08
description: "Variables - Obsidian Help"
tags:
  - "clippings"
---
Learn how you can embed other notes and media into your notes. By embedding files in your notes, you can reuse content across your vault.

To embed a file in your vault, add an exclamation mark (`!`) in front of an [Internal link](https://help.obsidian.md/links). You can embed files in any of the [Accepted file formats](https://help.obsidian.md/file-formats).

Drag and Drop embed

On desktop, you can also drag and drop supported files directly into your note to embed them automatically.

## Embed a note in another note

To embed a note:

```md
![[Internal links]]
```

You can also embed links to [headings](https://help.obsidian.md/links#Link%20to%20a%20heading%20in%20a%20note) and [blocks](https://help.obsidian.md/links#Link%20to%20a%20block%20in%20a%20note).

```md
![[Internal links#^b15695]]
```

The text below is an example of an embedded block:

Learn how to link to notes, attachments, and other files from your notes, using *internal links*. By linking notes, you can create a network of knowledge.

## Embed an image in a note

To embed an image:

```md
![[Engelbart.jpg]]
```

![Engelbart.jpg > outline](https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/Engelbart.jpg)

Engelbart.jpg > outline

You can change the image dimensions, by adding `|640x480` to the link destination, where 640 is the width and 480 is the height.

```md
![[Engelbart.jpg|100x145]]
```

If you only specify the width, the image scales according to its original aspect ratio. For example, `![[Engelbart.jpg|100]]`.

![Engelbart.jpg#outline](https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/Engelbart.jpg)

Engelbart.jpg#outline

You can also embed an externally hosted image by using a markdown link. You can control the width and height the same way as a wikilink.

```md
250
```

![250](https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/Engelbart.jpg)

## Embed an audio file in a note

To embed an audio file:

```md
![[Excerpt from Mother of All Demos (1968).ogg]]
```

<audio controls="" src="https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/audio/Excerpt%20from%20Mother%20of%20All%20Demos%20(1968).ogg"></audio>

## Embed a PDF in a note

To embed a PDF:

```md
![[Document.pdf]]
```

You can also open a specific page in the PDF, by adding `#page=N` to the link destination, where `N` is the number of the page:

```md
![[Document.pdf#page=3]]
```

You can also specify the height in pixels for the embedded PDF viewer, by adding `#height=[number]` to the link. For example:

```md
![[Document.pdf#height=400]]
```

## Embed a list in a note

To embed a list from a different note, first add a [block identifier](https://help.obsidian.md/links#Link%20to%20a%20block%20in%20a%20note) to your list:

```md
- list item 1
- list item 2

^my-list-id
```

Then link to the list using the block identifier:

```md
![[My note#^my-list-id]]
```

## Embed search results

![search-query-rendered.png](https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/search-query-rendered.png)

Obsidian Publish
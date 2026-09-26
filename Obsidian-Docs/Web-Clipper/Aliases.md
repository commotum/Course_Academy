---
title: "Aliases"
source: "https://help.obsidian.md/aliases"
author:
  - "[[Obsidian Help]]"
published:
created: 2026-01-08
description: "Variables - Obsidian Help"
tags:
  - "clippings"
---
If you want to reference a file using different names, consider adding *aliases* to the note. An alias is an alternative name for a note.

Use aliases for things like acronyms, nicknames, or to refer to a note in a different language.

If you're only trying to change how a link looks in one place, see how to [Change the link display text](https://help.obsidian.md/links#Change%20the%20link%20display%20text) instead.

Tip

Use [link display text](https://help.obsidian.md/links#Change%20the%20link%20display%20text) when you want to customize how a link looks *in a specific place*.

Use [aliases](https://help.obsidian.md/aliases) when you want to refer to the same note using *different names* throughout your vault.  

## Add an alias to a note

To add an alias for a note, add `aliases` property in the note [Properties](https://help.obsidian.md/properties). Aliases should always be formatted as a list in YAML.

```md
---
aliases:
  - Doggo
  - Woofer
  - Yapper
---

# Dog
```

## Link to a note using an alias

To link to a note using an alias:

1. Start typing the alias in an [internal link](https://help.obsidian.md/links). Any alias shows up in the list of suggestions, with a curved arrow icon next to it.
2. Press `Enter` to select the alias.

Obsidian creates the link with the alias as its custom display text, for example `[[Artificial Intelligence|AI]]`.

Note

Rather than just using the alias as the link destination (`[[AI]]`), Obsidian uses the `[[Artificial Intelligence|AI]]` link format to ensure interoperability with other applications using the Wikilink format.

## Find unlinked mentions for an alias

By using [Backlinks](https://help.obsidian.md/plugins/backlinks), you can find unlinked mentions of aliases.

For example, after setting "AI" as an alias for "Artificial intelligence", you can see mentions of "AI" in other notes.

If you link an unlinked mention to an alias, Obsidian turns the mention into an [internal link](https://help.obsidian.md/links) with the alias as its display text.
# Quiz Blocks Local Install and Build Guide

This guide is for Codex or a developer installing this local version of the Obsidian plugin on a Mac after making changes.

## What This Plugin Builds

The plugin id is `quiz-blocks`, from `manifest.json`.

The files Obsidian needs are:

- `main.js`
- `styles.css`
- `manifest.json`

After a production build, those files live in the repo root.

## Install Dependencies

From the repo root:

```bash
cd /path/to/obsidian-quiz-blocks
corepack enable
pnpm install
```

This repo has a `pnpm-lock.yaml`, so prefer `pnpm`. If `pnpm` is not available, install it through Corepack rather than creating a new lockfile with another package manager.

## Build

For a production build:

```bash
pnpm run build
```

This runs:

```bash
vite build --mode production
```

Production output is written to the repo root:

- `main.js`
- `styles.css`

`manifest.json` is already at the repo root.

## Install Into an Obsidian Vault on Mac

Create the plugin folder inside the target vault:

```bash
mkdir -p "$VAULT/.obsidian/plugins/quiz-blocks"
```

Copy the built files:

```bash
cp main.js styles.css manifest.json "$VAULT/.obsidian/plugins/quiz-blocks/"
```

Common Mac vault paths:

```bash
# Local vault example
VAULT="$HOME/Documents/My Vault"

# iCloud Obsidian vault example
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My Vault"
```

Keep quotes around `$VAULT` because vault paths often contain spaces.

Then open Obsidian:

1. Open the target vault.
2. Go to Settings > Community plugins.
3. Make sure restricted mode is off.
4. Reload plugins, restart Obsidian, or disable and re-enable "Quiz blocks".
5. Enable "Quiz blocks" if it is not already enabled.

## Update After Code Changes

Use this loop after editing the plugin:

```bash
pnpm run lint
pnpm run build
cp main.js styles.css manifest.json "$VAULT/.obsidian/plugins/quiz-blocks/"
```

Then reload the plugin in Obsidian. If the UI still shows stale behavior, fully restart Obsidian.

## Development Watch Mode

For local development:

```bash
pnpm run dev
```

This runs:

```bash
vite build --mode development --watch
```

Important: the Vite config writes development builds to:

```text
_test-vault/.obsidian/plugins/quiz-blocks
```

That is useful for the repo's test vault, but it does not automatically update a real Mac vault. For the actual vault, run the production build and copy the three plugin files, or adjust the workflow intentionally.

## Useful Obsidian Docs

The most useful docs for this plugin work were:

- `Build a plugin.md`: explains the build output Obsidian expects, especially `main.js`, `manifest.json`, and the plugin folder under `.obsidian/plugins/`.
- `Anatomy of a plugin.md`: explains `Plugin`, `onload`, `onunload`, commands, and how plugin registration fits together. This is the best reference for `src/main.ts`.
- `Development workflow.md`: explains the edit, build, reload cycle and why Obsidian needs the built files copied into the vault plugin directory.
- `Use Svelte in your plugin.md`: explains how Svelte components are mounted inside Obsidian UI containers and why cleanup matters.

The UI docs under `Obsidian-Docs/Plugins/User interface` are useful when changing visual behavior, theme integration, or Obsidian-native controls. For this plugin, theme-aware colors and UI consistency matter most when editing the Svelte components and CSS.

## Repo Files to Know

- `src/main.ts`: registers the plugin, commands, and Markdown code block processor.
- `src/renderer.ts`: parses the YAML inside ```quiz code blocks and mounts the Svelte renderer.
- `src/schemas.ts`: defines valid quiz types and fields.
- `src/ui/QuizRenderer.svelte`: routes each parsed quiz to the concrete quiz component.
- `src/ui/QuizRadio.svelte`, `QuizCheckbox.svelte`, `QuizChoice.svelte`, `QuizNoodle.svelte`, `QuizText.svelte`, `QuizPrompt.svelte`: quiz type UI components. `QuizChoice.svelte` renders both `select` and `multi-select`.
- `src/ui/__variables.css`: shared quiz colors and CSS variables.

## Current Quiz Type Names

Valid quiz types are:

- `radio`
- `checkbox`
- `select`
- `multi-select`
- `noodle`
- `free`
- `blank`

The old names are intentionally not aliases:

- `choice` should be changed to `select`
- `text` should be changed to `free`
- `prompt` should be changed to `blank`

## Quick Command Summary

```bash
cd /path/to/obsidian-quiz-blocks
corepack enable
pnpm install
pnpm run lint
pnpm run build

VAULT="$HOME/Documents/My Vault"
mkdir -p "$VAULT/.obsidian/plugins/quiz-blocks"
cp main.js styles.css manifest.json "$VAULT/.obsidian/plugins/quiz-blocks/"
```

Reload or restart Obsidian after copying the files.

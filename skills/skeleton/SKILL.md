---
name: skeleton
description: Create Obsidian assignment skeletons in this study vault. Use when the user provides a course folder target, a document or assignment name, and a problem count and wants a WHW-style folder with Prerequisites, Lessons, Source/document-name/Images, and a same-name markdown index generated from util/Skeleton.
---

# Skeleton

## Quick Start

Run the CLI from the study repo root:

```bash
python3 util/create_skeleton.py 253 WHW-2 5
```

This creates:

```text
vault/253/WHW-2/
|-- Lessons/
|-- Prerequisites/
|-- Source/
|   `-- WHW-2/
|       `-- Images/
`-- WHW-2.md
```

## Workflow

1. Accept three required values: course folder target, document name, and problem count.
2. Prefer the wrapper at `util/create_skeleton.py`; it delegates to `util/skills/skeleton/scripts/create_skeleton.py`.
3. Treat a bare course target such as `253` as `vault/253`. Also accept relative paths such as `vault/253` and absolute course folder paths.
4. Let the CLI create the document folder, `Prerequisites`, `Lessons`, `Source/<document-name>/Images`, and the same-name markdown file.
5. Verify the result with `find <document-folder> -maxdepth 3 -print` and inspect the first part of the generated markdown.

## CLI Options

Use these only when needed:

- `--create-course`: create the course folder if it does not exist.
- `--exist-ok`: allow the document folder to already exist.
- `--overwrite`: replace the same-name markdown file if it already exists.
- `--vault-root PATH`: use a non-default vault root for bare course names.
- `--template-dir PATH`: use a different skeleton template folder.

The CLI refuses to overwrite existing folders or markdown by default. Do not manually recreate the skeleton unless the script is missing or broken.

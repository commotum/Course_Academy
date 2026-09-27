# Build Lessons

Generate Math Academy-style lesson artifacts from prepared ECE course data.

Hierarchy:

```text
COURSE > UNIT > MODULE > TOPIC > STEP > QUESTIONS
```

Legacy JSON field names are still present: `lesson_*` means topic and
`section_*` means step.

## Stage Graph

```text
1-Build-Course-Data/5-Step-Identification state
  -> 1-Step-Outline/*-Step-Outline.json
  -> 2-Tutorial-Example-Generation/*-Tutorial-Examples.json
  -> 3-Question-Generation/*-Questions.json
  -> 4-Image-Generation/*-Images.json + rendered assets + image backlog
  -> 5-Compile/<Lesson Package>/
```

Stages:

- `1-Step-Outline`: convert upstream topic/step policy into topic-level lesson outlines.
- `2-Tutorial-Example-Generation`: generate tutorial and worked-example content.
- `3-Question-Generation`: generate practice questions from worked examples.
- `4-Image-Generation`: classify image slots against the matplotlib style guide and generate covered figures.
- `5-Compile`: compile final lesson package folders.

## Worker Loop

The LLM-backed stages are designed around this loop:

```text
prompt -> generate -> validate -> continue or fix -> revalidate
```

Each stage validates generated JSON before committing canonical artifacts. The
tutorial/example and question stages also invoke the fail-safe repair flow when
a section output exists but does not validate. Successful runs write structured
validation reports under each stage's `2-Runtime/2-State/validation-reports/`.

## Cache Rules

Stages 1 through 4 use strict cache reuse by default. A target is reused only
when the output exists, validates, and its recorded cache key matches the
current inputs, prompt/schema/style/example signature, runner version, model,
reasoning effort, and stage options.

Useful flags:

- `--overwrite`: rebuild even if the cache is valid.
- `--reuse-stale`: reuse structurally valid output even when cache metadata changed.
- `--cache-report`: print the cache hit or miss reason per target.
- `--subset-output`: write filtered results to `*.subset.json` instead of touching the canonical artifact.

Compile packages also record a cache key in each package source JSON. Existing
packages without the current cache key are rebuilt.

## Filtered Reruns

Filtered reruns are safe by default. When `--topic`, `--step`, `--slot`, or
their aliases are used, the stage generates only the selected entries, loads
the existing full canonical artifact as the merge base, replaces only the
selected entries, validates the merged artifact, and then commits it.

If no full canonical artifact exists, rerun without filters or use
`--subset-output` to produce a separate partial artifact for inspection.

## State And Resume

Each stage writes:

```text
2-Runtime/1-Logs/
2-Runtime/2-State/
2-Runtime/3-Tmp/
```

Successful targets are recorded in `processed_documents`; failures are recorded
in `failed_documents`. Temporary work is preserved for resume unless the cache
key changed or `--overwrite` is supplied. Stale temp directories are cleared
when prompt/model/input metadata changes so old section outputs are not silently
reassembled under a new prompt contract.

## Image Feedback Loop

Image generation first classifies each slot:

```text
image slot -> coverage classification -> generate if COVERED -> backlog if NOT-COVERED
```

Every `NOT-COVERED` record is persisted to:

```text
4-Image-Generation/2-Runtime/2-State/image-backlog.json
```

Backlog records include slot identity, image description, missing information,
new visual elements, classifier report, cache key, and source artifact paths.
Use this backlog to cluster missing visual categories, update the style guide
and examples, then rerun image coverage.

## Concurrency

Safe parallelism:

- Module targets can run in parallel with `--module-workers`.
- Image topics can run in parallel with `--topic-workers`.
- Legacy per-slot image work can run with `--batch-scope slot`, but topic
  batching is preferred because it shares context and reduces token waste.

Constrained work:

- Tutorial/example and question sections within one topic remain sequential
  when previous section outputs are part of the context.
- Repair loops stay local to the failed worker.
- Prepared shared sessions are reused across workers where the stage supports it.

## Examples

Dry-run the whole lesson build:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --dry-run --limit 0
```

Explain cache decisions for one module:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --module 6.1 --cache-report --no-progress
```

Safely regenerate one topic and merge it into the full artifact:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --start 2 --module 6.1 --topic 3 --overwrite
```

Write a partial artifact without touching the canonical output:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --start 3 --module 6.1 --topic 3 --step 2 --subset-output
```

Regenerate image coverage only and update the image backlog:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --start 4 --coverage-only --module 6.1 --cache-report
```

Compile despite missing images:

```bash
python PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.py --start 5 --module 6.1 --allow-missing-images
```

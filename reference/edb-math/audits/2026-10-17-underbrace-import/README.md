# Brace-accent import defect

The misplaced braces in **17592186060895** were introduced during MathML conversion. The original source has correctly stretched, labeled underbraces. The converter treated the brace as a subscript character, and treated its label as another subscript. The same defect affects **1,615 current content items, 1,688 attributes, and 4,372 brace occurrences across 209 topic entities (208 distinct lesson titles)** at database basis **3625**.

This investigation changed no database content or production code. It saved read-only evidence and inventories in this directory.

## Cause and exact example

Entity **17592186060895** is the tutorial **“Justifying the Formula for the Derivative of Cosine”**, in MA topic **280**, “Differentiating Trigonometric Functions.” Its stable source identity is tutorial **2620**, UUID `40bcba62-6d88-5cfd-9d89-e773514e5a63`.

The source places an underbrace beneath each complete limit expression, labeling them 0 and 1. Its MathML contains an inner `munder` with an `mo` child containing **⏟**, then an outer `munder` containing the label. Structurally, the intended and imported TeX are:

```tex
\underbrace{EXPRESSION}_{0}
{{EXPRESSION}_{⏟}}_{0}
```

The legacy converter [lesson-json.py](/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py:504) emitted every `munder` as `BASE_(UNDER)`. Original archived HTML converted with that code reproduces the malformed JSON exactly. The Markdown importer then retained that damage.

The later [question-capture converter](/home/jake/Developer/Course_Academy/scripts/question_capture/dom.js:205) and the active [capture converter](/home/jake/Developer/Course_Academy/capture/scripts/browser/extract.js:197) instead emit `'{'+base+'}_{'+under+'}'`, but still fail to recognize the brace decoration. Both current implementations reproduce the current tutorial formula exactly, with **`errors: []`**. The analogous `mover` handling emits a literal **⏞** in `\overset`, without a stretched overbrace.

The source brace nodes have **no explicit `accentunder="true"` attribute**. A correction must recognize the operator glyph and node structure; testing only that attribute would miss this example. Ordinary operator limits and ordinary subscripts must retain their own semantics.

Original evidence: [archived HTML](/home/jake/Developer/MA/DATA/Lessons/280/Source/280.html:3744), [archived JSON](/home/jake/Developer/MA/DATA/Lessons/280/Source/280.json:728), [newer captured tutorial](/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/13931643/tutorial-2620.html:266). The [full trace](source-trace/REPORT.md), [reproduction outputs](source-trace/reproduction.json), and [current-lineage comparison](source-trace/current-lineage-history-comparison.json) retain the exact transformations and hashes.

## When it entered this database

| Current-lineage basis | UTC timestamp | Verified change |
| --- | --- | --- |
| 35 | 2026-10-11 08:30:17.307 | Initial value exactly matches the malformed archived JSON rendered to Markdown. |
| 126 | 2026-10-11 08:36:30.160 | Replacement exactly matches the newer captured import; its two braces remain malformed. |
| 3083 | 2026-10-17 00:46:34.280 | Added only 15 invisible U+2061 function-application markers; the braces did not change. |

Older retained import receipts show the corresponding stages at bases 32 and 123 on October 10, before the database was rebuilt. Those older numeric entity IDs and bases must not be confused with the current lineage. The trace matches stable UUID/source identity and exact values across both sets of evidence.

## All current locations

| Content kind | Distinct affected entities |
| --- | ---: |
| Practice questions | 1,374 |
| Canonical worked examples | 126 |
| Tutorials | 115 |
| **Total** | **1,615** |

Affected attributes comprise **1,466 worked solutions, 107 question prompts, and 115 tutorial bodies**. Some questions have both an affected prompt and solution. All affected entities resolve to lesson placements.

| Imported corruption | Current occurrences |
| --- | ---: |
| Underbrace emitted as `_{⏟}` | 3,175 |
| Overbrace emitted as `\overset{⏞}{…}` | 1,043 |
| Flattened underbrace emitted as `_(⏟)` | 126 |
| Flattened overbrace emitted as `^(⏞)` | 28 |
| **Total** | **4,372** |

These four patterns account for every current and retained historical brace-glyph match. Valid `\underbrace` and `\overbrace` commands were scanned separately and were not counted as defects. No affected answer values were found among **317,506** current answer values; feedback and multistep contexts also contain no matches.

- [Complete current inventory — TSV](current-affected.tsv): entity, attribute, source identity, kind, lessons, knowledge points, occurrence count, and an excerpt.
- [Complete current inventory — JSON](current-affected.json): also contains the exact current text, assertion transaction, source entity, and each matching offset.
- [Every affected lesson](lessons.md), [lesson TSV with all affected entity IDs](lessons.tsv), and [structured lesson inventory](lessons.json).

The sibling sine-derivative tutorial **17592186060894** has the same defect. Other heavily affected lessons include Definite Integrals of Piecewise Functions, LU Factorization of 2x2 and 3x3 Matrices, The “And” and “Or” Connectives, and The Image of an Affine Transformation. The complete tables above include all locations, not just these examples.

There are **209 distinct topic entities**, but **208 distinct lesson titles**: MA topics **375** and **6501** both use “Solving Quadratic Equations by Factoring.” Earlier progress counts grouped by title; this final inventory groups by identity.

## Historical reach and original source census

Retained EDB history through basis 3625 contains the defect on **1,743 distinct entities / 1,816 attributes**, across 215 topic entities. **128 entities** no longer contain it: 119 practice questions, four examples, and five tutorials. These are recorded separately so a repair will not target already corrected or superseded versions. Every current malformed assertion exactly matches a retained historical assertion, including value, transaction, and source.

- [All historically affected attributes — TSV](historically-affected.tsv) and [JSON](historically-affected.json).
- [The 128 historical-only entities](historical-only.json).
- [Independent aggregate verification](evidence/answer-native/verification.json).

The separate source census examined **all 2,964 original lesson JSON files and their 2,964 paired HTML files**. It found **620 corrupted brace conversions** in **268 content items across 153 original topics**: 120 tutorials, 130 examples, and 18 practice questions. All 620 normalized glyph occurrences reconcile to actual original MathML brace nodes by topic, item, and accent kind. All occur inside mathematics. Of those 268 source identities, 256 still have a matching defect in the current database and 12 no longer do.

The archive also contains **622 correctly preserved TeX brace commands** in different expressions. Those are a separate source population, not a before/after discrepancy. Some source formulas retained original TeX from SVG titles, while rendered MathML formulas took the lossy conversion path. No alternate under/overbracket or parenthesis-accent glyph variants were found in the original archive.

Source census: [method and verification](source-census/README.md), [all original affected source items](source-census/affected-source-items.tsv), [structured source item mapping](source-census/affected-source-items.json).

## Why validation missed it

Both converters accept `munder`/`mover` as supported nodes, so they report no conversion error. The result is syntactically valid TeX: a parser can render the wrong subscript or overset structure successfully. Balanced groups and absence of MathJax errors therefore do not establish faithful conversion.

An [actual local MathJax comparison](source-trace/overbrace-comparison.png) confirms both visual failures. The generic overset keeps a small fixed-width brace above the middle of a long sum; `\overbrace` spans the whole sum. The subscript form places its underbrace at the right edge; `\underbrace` spans the expression underneath. All eight render probes reported zero MathJax errors. [Rendered DOM and geometry evidence](source-trace/overbrace-render-check.json) is retained.

The earlier October 16 source audit included `munder` in its candidate search, but its [accent check](/home/jake/Developer/Course_Academy/reference/mathacademy/repairs/2026-10-16-import-root-cause/source/scan.py:134) inspected explicit `mover accent="true"` nodes and did not check brace operators under `munder`. This specific family escaped that check.

## Evidence scope and repair direction

The current scan covers all **29 string attributes**, including **450,923 instructional content fields**, at one pinned basis and lineage. Historical scans cover the six instructional payload attributes. Answer values and historical content were streamed through native AEVT cursors to completion; this avoids Datalog intermediate/output capacity limits. Query files, native source/build hashes, completed-stream counts, and original results are retained under [evidence](evidence/).

For the 1,688 current affected attributes, an additional bounded source join found **775 exact text matches**, **four matches after only U+2061/whitespace normalization**, **799 source-identity links**, and **110 attributes not linked by that join**. Raw saved HTML brace nodes were checked in matching field containers for 220 attributes. The defect inventory is exhaustive for the identified stored signatures; this is not a claim that every current formula has been visually compared with its raw source. See [source-link coverage](source-trace/SOURCE-LINK-COVERAGE.md) and [per-attribute links](source-trace/source-links.json).

A durable repair should first teach both maintained extractors to preserve labeled and unlabeled underbraces/overbraces, using real source fixtures and semantic layout checks. The stored inventory can then be repaired while preserving expression scope and labels. Flattened `_(⏟)` / `^(⏞)` variants have lost grouping information and need their original source structure; a global character replacement is insufficient. No repair transaction was prepared or submitted during this investigation.

Machine-readable totals: [summary.json](summary.json). Rebuild local reports with `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python reference/edb-math/audits/2026-10-17-underbrace-import/report.py`.

# Original-import extraction audit — October 16, 2026

**October 17 follow-up:** The [bulk source restoration](../2026-10-17-import-source-bulk/README.md) committed 2,859 field repairs at basis 3519, with exact readback verification. Two audit associations were proven false positives and left unchanged. The investigation record below describes the original read-only audit.

Tracing the extraction failure provides a repeatable way to find affected content across the original import. The audit identifies **312 current content fields across 160 lessons** that retain the original first-fragment extraction, with source evidence and unchanged original/current field values. These are strong repair candidates, not completed repairs. Additional structural findings are retained separately for review.

No database content, original source files, application code, generators, or capture-worker settings were changed during this investigation. Entirely missing solutions remain outside scope.

## Failure chain

1. The original browser capture saved the rendered page DOM. The retained HTML contains older SVG formula titles with newer MathJax fragments nested inside them.
2. The historical `lesson-json.py` extractor returned the **first descendant assistive MathML fragment** before reading the complete outer SVG title. Labels, operators, additional operands, and results could disappear. A complete `A = [matrix], x = [vector]` definition could become only the first matrix.
3. This truncated fragment was already present in archived JSON. The EDB importer rendered that JSON and faithfully stored the truncated result.
4. Import validation checked syntax, references, and agreement with prepared data. A lone matrix or variable is valid mathematics in isolation, so those checks did not detect missing source content.

The [offline reproduction](trigger/reproduction.json) demonstrates how default MathJax 3 environment processing inside SVG titles creates this exact nested structure, and how the historical selector then drops the surrounding expression. Excluding titles prevents that fixture's reprocessing. The historical site's exact configuration has not been recovered; the selector loss itself is established directly from archived HTML and JSON.

## Coverage and findings

All **2,964 archived lesson HTML/JSON pairs** were scanned with no scan errors. The database comparison is pinned to **basis 3291** and includes 449,174 current content fields. All 41 original archived-lesson import files passed their recorded SHA-256 checks; their 139,520 fields were joined to current entities by stable identity.

| Finding | Count | Meaning |
| --- | ---: | --- |
| Primary historical source witnesses | 3,491 | Exact old extraction found in archived JSON, with unambiguous content-attribute ownership; spans 600 source topics. |
| Primary current repair candidates | 312 fields | 95 tutorials, 88 prompts, and 129 existing worked solutions, across 300 entities and 160 lessons. The entire current field still equals its original imported value. |
| Primary changed-field occurrences | 3,025 | Later capture or editing occurred. These require contextual comparison; a change does not establish that the loss was repaired. |
| Primary unanchored render occurrences | 4 | Original rendered math could not be matched automatically and remains review-only. |
| Secondary structural candidates | 2,727 fields | Other historical conversion predicates, including lost equation rows, cancellation marks, column rules, percent signs, hidden content, and zero-bar fractions. This queue has not received the primary queue's independent review. |
| Deduplicated combined candidates | 2,861 fields | Primary and secondary queues overlap by 178 fields. Do not add their counts. |

These counts concern the original archived import. They do not certify every later capture, every changed field, or every possible prose, image, answer-key, or layout defect.

## Repair queue and verification

- [Primary affected fields](database/affected-fields.csv): current entity IDs, source IDs, owning topics, and unchanged/review states.
- [Primary candidate evidence](database/source-backed-candidates.jsonl): exact current content and occurrence-specific source references.
- [Secondary affected fields](database/secondary-affected-fields.csv): separate structural review queue.
- [Database summary](database/summary.json), [source report](source/README.md), and [independent QA](review/audit-quality.json).

Independent QA verified all 312 primary fields and their 462 matched source occurrences against the pinned export and original committed fields. Eight complete owner-field replays and twelve stratified source examples were also checked. The current extractor's 24 focused browser regressions passed. Eight source-detector controls and the offline trigger reproduction passed. One additional synthetic spacing-marker edge remains documented, with zero neutral-only occurrences in the final primary stream.

Recent tutorial repairs were explicitly checked and are absent from both unchanged-original candidate queues. Newer questions without an original archived baseline cannot enter those queues.

## Repair method

Recover each affected field from its complete retained source, preserving source formula order, labels, matrix cells, and answer-control positions. Verify source completeness before UI rendering. Apply only reviewed field changes with exact before-value guards and verify the saved result. Keep answer identities, correct links, difficulties, and learner state intact.

Do not use global replacement of a small surviving fragment: 735 primary historical occurrences share the same fragment value with another position in the same attribute. Those positions can require different restored expressions. Changed fields require a contextual merge so later corrections survive. This audit does not authorize a blind replay of the original import.

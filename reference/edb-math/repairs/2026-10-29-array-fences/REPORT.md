Fixed question 17592186551286 and the related database-wide table-fence defects. The three content transactions (T11477, T11521 and T11551) repaired **4,273 distinct fields on 3,862 entities**. Nineteen fields received further sizing repairs in the second pass, so transaction update counts exceed the distinct-field total.

The reported defect was stored TeX: ordinary brackets around augmented `array` matrices stayed at text height. Earlier repairs restored the array and its divider, but their detector handled `aligned`/`matrix` environments and skipped augmented arrays. Later checks established that the TeX parsed, without measuring fence height. The same renderer and CSS display the corrected source properly. See the [original diagnosis and before/after evidence](../2026-10-29-q17592186551286/FINDINGS.md).

The audit expanded from arrays to systems, piecewise expressions, proper matrix environments, function arguments, composite sums and sets, named delimiters, Unicode determinant/norm/angle glyphs, and one-sided braces. Repairs preserve every ordered cell, augmentation rule and mathematical expression. The only additional normalization changes Unicode delimiter spellings to their equivalent TeX tokens, which MathJax requires after sizing commands. Teaching annotations, optional macro arguments, conditional separators and deliberately sized delimiters remain distinct.

Distinct fields repaired:

| Attribute | Fields |
| --- | ---: |
| `question/problem` | 1,243 |
| `question/worked-solution` | 1,861 |
| `tutorial/content` | 42 |
| `answer/value` | 1,043 |
| `answer-field/key` | 81 |
| `multistep/context` | 3 |

The field keys are visible checkbox option labels. Blank identifiers were preserved. Changed answer values belong to authored radio choices, including one retained orphan radio field; noncanonical learner blank responses were excluded. Existing UUIDs, entity IDs, answer types, field links, correct-answer links, answer banks and learner history remain intact. Repairs use guarded CAS and native specifications with exact datom, provenance and readback verification.

Evidence:

- [First batch commit verification](batch-001/verification.json) and [second batch commit verification](../2026-10-29-matrix-outer-fences/batch-001/verification.json).
- [Combined full-database postscan](../2026-10-29-matrix-outer-fences/postscan.json): 3,044,006 current facts at T11551; all 4,273 repaired values and 2,721 complete question contracts verified; zero remaining authored defects recognized by the expanded fence check.
- [Independent fence-context scan](../2026-10-29-matrix-outer-fences/independent-final-verification.json): zero unexpected plain fences; 16 remaining contexts individually identified as math boundaries or conditional separators.
- Actual player rendering passed for all 2,289 first-batch fields and 2,002 second-batch fields. [Second-batch geometry review](../2026-10-29-matrix-outer-fences/geometry-final.json) includes 15,056 measurements. Twelve apparent low-height cases are existing angle glyph size limits or conditional separators; all are recorded, with no unresolved geometry candidates. Geometry uses actual table bodies, rather than inflated bounding boxes of enclosing delimiter assemblies.
- Native before/after selection grading matched: first batch 3,076 accepted and 10,818 rejected; second batch 2,376 accepted and 8,880 rejected. Pre-existing fields without canonical answers were recorded and preserved rather than silently completed. No learner activity, XP or exposure was created by QA.

Prevention is implemented in the shared capture/generation formatter, the publication validator, actual-renderer QA, and capture/generator instructions. Publication validation also checks rendered checkbox labels. Regression checks passed: 47 formatter tests, 43 publisher tests, five historical MathML tests and four actual-renderer geometry tests. No learner UI or CSS change was necessary.

The audit covered 39 registered generators and 303 records across 101 supported-band invocations. Seven generators reproduced the defect. Their immutable replacements retain original mathematical generator inputs byte-for-byte, normalize output presentation, then derive stable identities and remap correct-answer links. They were published and registered, and [live registrations plus installed CLI outputs were verified](../2026-10-29-matrix-outer-fences/generator-repair/installed-verification.json). Forty-five replacement records matched outputs from two relocated read-only package copies; their selection grading produced 51 accepted and 141 rejected results. The final [generator verification](../2026-10-29-matrix-outer-fences/generator-final-verification.json) has zero formatting failures. Sixteen calls outside source-backed supported difficulties are explicitly recorded; no additional difficulty bands were invented.

This result certifies this table-fence defect class, not every possible mathematical or visual defect in the database. Intermediate failed scans and probes remain as discovery evidence; the linked final verification files describe the repaired state.

# Underbrace import trace: tutorial 2620

The malformed brackets are a deterministic MathML-to-TeX conversion bug. The source contains a stretched underbrace attached below a whole expression, followed by another `munder` holding the label 0 or 1. The converters treat **every** `munder` as an ordinary subscript. Thus an intended `\underbrace{EXPRESSION}_{0}` becomes `{{EXPRESSION}_{⏟}}_{0}`. The Unicode brace is rendered as a small subscript at the expression's right edge, and its label becomes another subscript. This is semantic loss at conversion, not missing source data or database escaping.

The source is MA topic 280, “Differentiating Trigonometric Functions,” tutorial content ID2620, step12325, stable UUID `40bcba62-6d88-5cfd-9d89-e773514e5a63`. It is currently EDB entity17592186060895. Archived receipt EIDs differ because the database was rebuilt; match stable UUID/source ID, not numeric historical EID.

## Recovered source and archived receipt chain

1. Original source HTML: `/home/jake/Developer/MA/DATA/Lessons/280/Source/280.html`, step at line3480 and MathML at line3744. It contains two nested brace constructions. The rendered source also has `mjx-stretchy-h class="mjx-c23DF"` widths6.489em and4.657em, showing the original braces span the full respective expressions. The semantic MathML is saved as `original-mathml.xml` here. The specific `munder` nodes have no explicit `accentunder` attribute, so a fix must recognize the underbrace operator glyph/node structure; checking only `accentunder="true"` would miss them.
2. Legacy normalizer `/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py:504` emits every `munder` as `BASE_(UNDER)`. Reproduction with the actual source returns the exact `[MATH: ...lim_(h → 0)..._(⏟)_(0)...]` text recorded in `/home/jake/Developer/MA/DATA/Lessons/280/Source/280.json`, tutorial beginning line728. This converter code entered MA git in `f005af127e`, Apr10 2026; the source snapshot last recorded git change is `50bbca666d`, Apr11 2026. These are repository commit dates, not inferred capture times.
3. Archived import generator `reference/edb-math/bin/generate-ma-lessons-json.py:15` loads existing MA Markdown renderer `.../5-MD/md.py`; lines173–178 render the tutorial and write it unchanged to `:tutorial/content`. `md.py:672` normalizes math but does not reconstruct underbrace semantics. Its current rendering of that original source JSON exactly matches the content in the archived original receipt `reference/edb-math/imports/math-academy/lessons/receipts/lessons-0003.edn` (basis31→32, UTC2026-10-10T04:43:00.639Z).
4. Newer original capture: `reference/mathacademy/question-capture/13931643/tutorial-2620.html:266`, whose original rendered MathML still has the correct brace nodes. The occurrence in `reference/edb-math/imports/math-academy/newer-captures/tutorials.json` records file mtime UTC2026-10-04T07:29:23.238970Z, old basis347, `errors: []`, and the exact malformed content later replayed at T126 in the current lineage.
5. The later DOM extractor has the same mistake: `scripts/question_capture/dom.js:205` maps `munder` to `'{'+base+'}_{'+under+'}'`. Browser reproduction using original MathML and historical versions `cf225949d5` (Oct3), `ce3d56f1c0` (Oct4), `c6b4ab597c` (Oct8) reproduces both bad braces without reporting errors. The Oct8 and current versions reproduce the exact entire imported formula after removing the invisible U+2061 application marker. Earlier versions differ only in function-name operator markup.
6. Archived newer-capture receipt `reference/edb-math/imports/math-academy/newer-captures/receipts/052-tutorials-commit.edn` confirms replacement basis122→123 at UTC2026-10-10T07:47:04.718Z: its retracted value exactly matches old JSON rendering; its asserted value exactly matches the newer occurrence and T126 in the current lineage. Both generations therefore carried the bug. These receipt timestamps/bases belong to the archived import run; the current lineage replay timeline is listed below.
7. Active pipeline `capture/scripts/browser/extract.js:197` still has the same generic mapping. Reproduction with that actual extractor also outputs the same braces and `errors: []`. No code changes have been made in this investigation.

## Current database lineage history, verified separately

Current entity17592186060895 is the same stable tutorial UUID and MA ID as above. The parent captured live historical datoms and transaction metadata under `reference/edb-math/audits/2026-10-17-underbrace-import/evidence/target-history.json` and `target-history-metadata.json`. The following are **current-lineage** times and bases, separate from the older archived receipts. Basis values use the verified transaction partition offset13194139533312.

| Current basis | UTC assertion time | Exact source comparison |
| --- | --- | --- |
| T35 | 2026-10-11T08:30:17.307Z | Byte-for-byte identical to the original source JSON rendered by MA `md.py`; two `_(⏟)` braces. |
| T126 | 2026-10-11T08:36:30.160Z | Byte-for-byte identical to the newer-capture `tutorials.json` occurrence; two `_{⏟}` braces. |
| T3083 | 2026-10-17T00:46:34.280Z | Byte-for-byte identical to the current pull. Its only change from T126 is reinserting 15 actual U+2061 FUNCTION APPLICATION characters immediately after `\operatorname{cos}`/`\operatorname{sin}`. Removing those characters exactly restores T126. Both malformed braces are unchanged. |

All three assertions have source17592186045417, `:org/Math-Academy`. The raw formula emitted by both current JavaScript extractors matches the current T3083 formula **exactly**, including U+2061. The earlier newer-capture occurrence omitted these invisible markers, so its full text is not byte-for-byte equal to the current pull; its brace corruption is identical.

`current-lineage-history-comparison.json` records all exact-match predicates, SHA-256s and occurrence counts; `compare_live_history.py` reproduces these comparisons without any database writes. The current database history establishes that the corruption was already present at first import T35 and persisted through T126 and T3083. The latest update did not create the malformed braces.

## Why checks missed it

- Both converters whitelist `munder`, so this produces no unsupported-node warning.
- The generated TeX has balanced syntax and a valid subscript structure; ordinary parser/error checks do not know that it should have been a stretched underbrace.
- The Oct16 source/root-cause audit's candidate regex included `munder`, but `reference/mathacademy/repairs/2026-10-16-import-root-cause/source/scan.py:134` only examined explicit `mover accent="true"` nodes for accent loss. It never checked `munder` brace operators. Thus this family escaped that audit.

## Repair direction (not applied)

Translate source `munder`/`mover` brace decorations into `\underbrace`/`\overbrace`, preserve the complete decorated child and its separate label, and continue to distinguish ordinary limits/operators from decorations. Test nested labeled and unlabeled braces from actual source fixtures through both maintained JS extractors. A brace-glyph blacklist or syntax-only test is insufficient. Source-derived repair can precisely recover scope; blindly replacing every `munder` or every subscript would damage legitimate notation.

## Files in this evidence directory

- `reproduction.json`: actual conversion outputs and exact-match checks; original source SHA-256s.
- `original-mathml.xml`, `newer-source-mathml.xml`: complete original formulas, prettified.
- `archived-source-step.html`, `original-normalized-json-step.json`, `archived-json-rendered.md`: source→JSON→Markdown evidence.
- `newer-import-row.json`: extracted original import record.
- `archived-receipt-evidence.json`: relevant exact transaction datoms plus transaction metadata only.
- `current-lineage-history-comparison.json`: exact comparisons to live history and current pull.
- `reproduce.py`, `trace_receipts.py`, `compare_live_history.py`: read-only repeatable extraction scripts. Use MA `.venv/bin/python` for Playwright and BeautifulSoup.

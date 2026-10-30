# Vector-topic LaTeX and import repairs

Committed to `math` at **basis 11883**, source `:agent/codex`: **512 text fields across 376 entities** in the two requested vector topics. Exact committed readback matches the prepared compare-and-swap values.

- Position-vector topic **17592186048780**: 295 fields repaired. The 298 audit candidates included three scalar-only answers, which correctly remain unchanged.
- Vector-line topic **17592186049485**: 217 fields repaired.
- All **15 malformed arrow/bar occurrences in 12 fields** were corrected. Fixed-width overset decorations were replaced with proper spanning arrows/bars, and vector boldface was restored using original source or explicit local mathematical roles. Scalars, numeric values, minus signs and parameter bounds remain unchanged.

Only existing `question/problem`, `question/worked-solution`, `answer/value`, and `tutorial/content` values changed. The transaction adds no missing solutions or answer keys. Existing duplicate answer-field structures and the source-inherited square-root derivations were left untouched. Protected-structure and missing-solution queries match before and after at the committed basis.

## Verification

All 512 proposed fields pass the actual player's strict MathJax and structural checks. Each transformation independently preserves every byte after removing only the approved font/decoration differences; prose and image references are unchanged. Representative corrected screenshots were visually inspected. All known malformed arrow/bar patterns are absent from the audited topic snapshots after merging the verified repairs.

The user authorized the repair with “leave the empty questions alone for now, just fix any malformed latex or bad imports. don't wait for me.” Preparation refreshed the exact fields from basis 11880; per-field CAS guards protected against concurrent changes. The persisted request and committed receipt are retained. No answer-field membership, correct-answer link, or learner-progress attribute was changed.

## Importer prevention

The reproduced legacy importer at `/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py` discarded bold `mi` metadata and checked `accent=true` only on the parent mover, although the captured source also places it on the child operator. Its fallback emitted pseudo-TeX such as `PQ^(―)`.

The source now preserves bold vector tokens and emits proper TeX for arrow/bar accents, including child-operator accents. The exact guarded patch and source hashes are retained in [legacy-importer.patch](legacy-importer.patch) and [legacy-importer-change.json](legacy-importer-change.json). Four importer regression tests pass against the modified source.

The shared capture validator now rejects flattened `^(→)` / `^(―)` accents, and `check_math_rendering.py` runs structural checks as well as MathJax. All 48 math-format regression tests pass. Missing content is still handled independently of syntax validation.

## Records

- [Committed verification](verification.json)
- [Preparation and invariants](preparation.json)
- [Strict render results](render-verification.json)
- [Exact changes and evidence](changes.json)
- [Position-vector repair report](topic-17592186048780/report.md)
- [Vector-line repair report](topic-17592186049485/report.md)

Direct original-source matches and local role/diagram proofs are distinguished in the per-topic evidence. This repairs the content covered by the pinned audit; it does not assert that unrelated topics or future generated records have been audited.

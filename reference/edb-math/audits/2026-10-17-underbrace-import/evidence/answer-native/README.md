# Native read-only census and independent verification

All reads use database `math`, pinned to basis **3625**. The connection captured current basis 3627 and explicitly applied `as_of(3625)`. No transaction API is called. Programs compile against the deployed EDB library recorded by the build manifests.

`scan.rs` streams the entire current AEVT prefix for `:answer/value` (attribute 1080). It examined **317,506 datoms / 317,506 entities**, containing 6,579,308 UTF-8 value bytes. There were **zero** matches for `⏟`, `⏞`, `︷`, `︸`, `\underbrace`, or `\overbrace`. `matches.edn` is the complete empty result; `stats.json` records counts and completion.

`history.rs` streams historical AEVT prefixes through the same basis for tutorial content, question prompts/solutions, answer values/feedback, and multipart contexts. Every matching row is saved as `[entity attribute value transaction source added]`, with separate per-attribute statistics. No matching answer value, feedback, or multipart context has ever been recorded through this basis.

`verify.py` independently deduplicates existing current results and the historical rows, merges existing metadata and original-archive readback identities, classifies every brace occurrence, and checks that every current malformed assertion appears exactly in history. It performs no database reads. `verification.json` records:

| Measure | Current | Ever affected through basis 3625 |
|---|---:|---:|
| Content attributes | 1,688 | 1,816 |
| Content entities | 1,615 | 1,743 |
| Practice questions | 1,374 | 1,493 |
| Canonical examples | 126 | 130 |
| Tutorials | 115 | 120 |

Current content contains **4,372** malformed brace occurrences: 3,175 `_{⏟}`, 1,043 `\overset{⏞}`, 126 `_(⏟)`, and 28 `^(⏞)`. These four shapes cover every current and historical match. The historical census contains 4,234 matching datoms: 2,961 assertions and 1,273 retractions. Historical occurrence totals include repeated versions and retractions and must not be presented as unique mistakes.

Exactly **128 formerly affected entities/attributes are currently clean of these signatures**: 119 practice questions, four canonical examples, and five tutorials. This classification means the malformed signature is absent; it is not a new visual or mathematical audit of their replacement content.

`build.json` records the first answer-scanner build; `history-build.json` records the history-scanner build. `invocations.json` records the database/basis/commands and signature lists. Raw EDN files retain complete match values and provenance. The original source-archive census is separate from these live/history counts.

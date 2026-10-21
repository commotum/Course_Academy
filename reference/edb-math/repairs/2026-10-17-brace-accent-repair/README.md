# Brace-accent import repair — committed

The authorized repair committed to `math` at **basis 3646**, from basis 3645, with source `:agent/codex`. It fixes **4,372 malformed underbraces/overbraces in 1,688 attributes on 1,615 entities**. Complete committed readback matches the native preview, and the exhaustive post-commit scan found **zero remaining raw brace-accent defects among 451,098 current text values**.

The scope comes from the [original import audit](../../audits/2026-10-17-underbrace-import/README.md), including tutorial `17592186060895`.

## Transaction

| Attribute | Repaired fields |
|---|---:|
| `:question/worked-solution` | 1,466 |
| `:question/problem` | 107 |
| `:tutorial/content` | 115 |

The payload contains 1,688 compare-and-swap forms and 1,615 question/tutorial validation assertions. It changes no answer values, keys, choices, historical responses, difficulty, or curriculum links. Source HTML archives remain unchanged.

- [Exact transaction](transaction.edn), [human-readable diff](changes.diff), [plan](plan.json)
- [Saved request](request.json), [commit receipt](receipt.edn), [commit verification](commit-verification.json)
- Transaction SHA256: `bba925bab792827284cc735df23ef2f8bebec4069c1aecc5a45681a14e7112f8`
- Database lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`

## Recovery and prevention

The importers treated MathML brace accents as ordinary subscripts or oversets. Balanced TeX still retained the complete base and label for 4,218 accents in 1,605 fields. Their repair was independently checked for exact scope, labels, and byte-identical unrelated content: [structured verification](structured/verification.json).

The remaining 154 accents had flattened grouping. All 83 affected fields were recovered from original MathML with archived source paths, selectors, hashes, and replacement proofs: [source-recovery details](flattened/README.md), [proofs](flattened/changes.json). Independent review checked 150 replacement spans against 47 original source files.

Two source-specific corrections are documented in those proofs:

- `17592186224898`: moved the existing minus into the brace so `-5x-x` correctly carries the label `-6x`. The equation's visible algebra tokens are unchanged, and symbolic verification confirms the label.
- `17592186078326`: recovered two source equation rows where the flattened import also confused absolute-value bars with matrix delimiters inside the brace expression.

Fifteen labels containing source `[math]` wrappers retain their math/text and color boundaries.

The two maintained JavaScript converters and the historical Python importer now produce semantic `\underbrace`/`\overbrace` notation with complete bases and centered labels. Focused source/geometry tests and adjacent import regressions passed: **46 tests**. Operator-only brace styling that cannot be faithfully represented is explicitly flagged instead of silently discarded. These are local code changes; this repair did not deploy or Git-commit them.

## Verification and limits

- [Native preview verification](preview-verification.json): validators passed; exact intended datoms only; full question/tutorial projections match the saved input snapshot plus the intended text edits.
- [Committed verification](commit-verification.json): exact receipt and pinned readback at basis 3646, in seven batches of at most 250 records.
- [Browser validation](browser-validation.json): 6,752 before/after renders at desktop/mobile widths, plus 56 renders of the final 14 label-boundary refinements. No new parse errors, overflow, or lost math expressions. Six fields' existing brace-related parse errors were resolved. [Original requested tutorial screenshot](sample-0.png).
- [Post-commit census](post-commit-census/summary.json): all six content attributes scanned completely; zero matching defects. History intentionally retains the original values.

The browser comparison also records **20 fields with separate, pre-existing hat-accent parse errors** (`\overset{^}{...}`), and 24 fields with pre-existing overflow at one or both checked widths. These remain unchanged by the brace repair and are listed in [render findings](preexisting-render-findings.json). This report does not claim that all unrelated LaTeX in the database is clean.

## Reproducibility

`prepare.py` composes and validates the source-proved edits; `refresh.py` refreshes the pinned census and full snapshots while requiring identical repair scope. `verify.py` checks speculative or committed evidence. `submit.py` persists and reuses the exact authorized request identity for recovery. `native/census.rs` is the read-only exhaustive scanner. The initial snapshot at basis 3644 is preserved in `evidence-b3644/`; final preparation evidence is in `evidence/` at basis 3645.

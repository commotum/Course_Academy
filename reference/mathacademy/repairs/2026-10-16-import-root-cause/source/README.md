# Historical import loss: source forensics

Examined all **2,964 archived lesson HTML/JSON pairs**. The scanner made no changes to source files, capture code or EDB. It records exact source ownership, source hashes, replayed historical extraction and matching JSON fragment positions.

The primary stream contains **3,491 mixed-title occurrences in 600 source topics**, mapping to 2,036 source owner/attribute pairs. These counts are historical source witnesses. A separate fresh EDB comparison must establish what remains damaged today. 735 occurrences match more than one position within the same attribute and therefore cannot authorize a blind substring replacement.

## Proven failure chain

1. The archived topic capture opens the site, waits for the page, and saves `page.content()` in `topics.py:818–847`. It does not inject MathJax or invoke typesetting. The saved HTML already contains newer MathJax CHTML/assistive MathML nested inside older SVG titles.
2. `lesson-json.py:532–544` searches every descendant for the first `mjx-assistive-mml` and returns its MathML before reading the complete SVG title. In `A = [matrix] x = [vector]`, only the first matrix survives. The name, second operand and operators are still present in the archived title, proving the loss occurs at extraction.
3. The returned fragment is serialized as a `[MATH: ...]` span. Matching those exact spans in the archived JSON distinguishes an observed historical import from a hypothetical parser weakness.
4. The seed importer renders those JSON spans using `md.py`. A downstream renderer cannot infer missing operands or labels from the isolated first matrix. Separately, flattening MathML to semicolons/pipes loses roles, invisible content and annotations that Markdown heuristics cannot reliably reconstruct.

The parent’s offline MathJax reproduction (`../trigger/reproduction.json`) establishes that default MathJax 3 can process bare TeX environments inside SVG titles and create this mixed markup. The archived capture itself does not prove the exact historical site MathJax configuration, so that upstream origin remains a supported explanation rather than a claimed recovered server fact.

## Deterministic source predicates

| Mechanism | Source occurrences | Source topics | Matching archived JSON |
| --- | ---: | ---: | ---: |
| `mathml-cancellation-removed` | 539 | 227 | 539 |
| `mathml-cases-row-layout-lost` | 2,131 | 321 | 2,116 |
| `mathml-hidden-phantom-made-visible` | 1,281 | 267 | 1,261 |
| `mathml-literal-percent-not-escaped` | 1,566 | 155 | 1,566 |
| `mathml-matrix-column-separator-lost` | 353 | 72 | 353 |
| `mathml-padded-structure-flattened` | 163 | 61 | 163 |
| `mathml-parenthesized-matrix-layout-lost` | 14 | 6 | 14 |
| `mathml-zero-rule-fraction-made-visible` | 127 | 27 | 127 |
| `mixed-title-first-fragment` | 4,026 | 621 | 4,026 |
| `source-tex-comment-line-scope-lost` | 26 | 17 | 26 |

Counts overlap when one formula has several mechanisms. They are not additive database defect counts.

- **Comment line scope:** `md.py:775` calls `normalize_ws`, turning physical newlines into spaces. A real source `%` comment can then consume subsequent mathematics. This is distinct from MathML literal percent signs becoming unescaped TeX comments.
- **Rows and separators:** `lesson-json.py:518–524` changes tables into semicolon-separated rows and pipe-separated cells. Cases, parenthesized arrays and visible column rules lose information; square-bracket matrix reconstruction is a useful negative control.
- **Zero-rule fractions:** `mfrac` always becomes division at `lesson-json.py:441–447`, even when `linethickness="0"` explicitly says no fraction bar.
- **Invisible and annotated nodes:** `mphantom` and `menclose` are flattened at `lesson-json.py:432`; hidden values can become visible and cancellation marks disappear. Unsupported `mpadded` falls through to `get_text` at line529, which can discard descendant fraction/script structure.

## Scope and controls

The primary stream excludes pure TeX titles, single rendered fragments surrounded only by punctuation/HTML wrappers, package directives and neutral style/spacing, duplicated visible/assistive MathML within one container, unknown/closed source owners, and ambiguous cross-attribute JSON matches. The wider occurrence file retains source candidates separately and does not claim they are current corruption.

Eight focused controls pass in `tests.log`; independent source/DOM review is recorded by the render agent. Ordinary fractions and safe single-fragment wrappers are explicit negative controls. This scanner targets concrete historical math-conversion mechanisms; it does not certify every unrelated image, prose, table, answer key or capture.

## Reuse

Run `./.venv/bin/python reference/mathacademy/repairs/2026-10-16-import-root-cause/source/scan.py` from the repository root, followed by `report.py`. `--topic` restricts a diagnostic scan. The scanner writes only this evidence directory.

- `catalog.json`: all source topic IDs, item IDs, paths and input hashes.
- `primary-mixed-title.jsonl`: strong mixed-title source witnesses for the current database join.
- `occurrences.jsonl`: all implemented deterministic source predicates, including review-only ownership ambiguity.
- `summary.json`: mechanism counts, exact parser/renderer/scanner hashes and errors.
- `reproductions.json`: a compact real-source witness for every observed mechanism.
- `primary-summary.json`: primary coverage and same-attribute location ambiguity.

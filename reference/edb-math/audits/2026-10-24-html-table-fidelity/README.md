# Source-faithful HTML tables: global audit and tested proposal

**Recommendation:** preserve source table structure as sanitized HTML inside the existing Markdown content fields, with a small, shared table presentation layer. Keep real `td`/`th` roles, source row/column spans, sections, captions, alignment and grouping/shading. Use theme-aware presentation and an outer horizontal-scroll wrapper. Do not convert every table into a Markdown header table or center all tables globally.

This is a **read-only database investigation and working prototype**, not a deployed UI or committed content migration. All code and proposed replacements for this task are in this audit directory. No database, learner state, production importer, generator or UI code was changed.

## Database-wide findings

The audit captured `math` at **T6717** and scanned **1,382,557 current domain strings**. It found **10,627 table occurrences in 8,422 fields**: 9,460 Markdown tables and 1,167 HTML tables. Existing authored assignment tables and editable matrix layouts are included in the inventory, not assumed defective.

The source comparison examined all **2,964 archived lesson HTML files**. For relevant database identities, 530 pages supplied **4,505 source table records** across 2,605 source identities. Comparisons bind tables to their question/tutorial identity and content attribute, then compare actual cell contents. Empty Markdown padding is allowed only when it follows the source's literal physical cells. Different images are not treated as interchangeable. Repeated source layouts that disagree are held for review.

**2,941 Markdown table occurrences have source-confirmed fidelity losses**, across **2,453 fields, 2,220 entities and 451 source topics**. These counts overlap:

| Confirmed loss | Table occurrences |
| --- | ---: |
| Source table position and/or explicit cell alignment | 2,941 |
| Shaded label/group cells | 2,788 |
| First row incorrectly promoted to column headers | 1,963 |
| Flattened nested tables | 82 |
| Lost merged-cell spans | 68 |

The audit also matched 63 existing HTML tables that merit source-aware rendering review. **18 conflicting source-layout matches are explicitly unresolved.** Another 7,605 current table occurrences were not matched to a unique archived table by this conservative method; that number is not a defect count. Many tables have no matching archived source, use newer capture evidence, contain images whose identity needs further reconciliation, or differ in wording/structure. The confirmed count is a lower bound, not a claim that every other table is correct or corrupt.

Concrete examples show this is a general class:

| Entity | Table | Confirmed concern |
| --- | --- | --- |
| 17592186068570 | Change-of-limits example e-467 | Lost centering/shaded row-label column; invented header row |
| 17592186122073 | Transition-probability answer option q-35787 | Lost `From:`/`To:` merged labels and group shading |
| 17592186060438 | Statistical lookup tables q-93903 | Two nested lookup tables flattened into long runs of formulas |
| 17592186084417 | Degree/radian tutorial table | Wide layout, shaded labels and merged separator row |
| 17592186055191 | Editable sign chart q-277702 | Table alignment/shading around real dropdown fields |
| 17592186060148 | Editable truth table q-182581 | Column roles, shading and retained field identities |
| 17592186106233 | Geometry proof table q-244541 | Statement/reason columns with embedded dropdown fields |

## Why this representation is the best fit

Markdown requires a header row and cannot faithfully represent arbitrary row headers, `rowspan`, `colspan`, nested tables or shaded cell groups. CSS cannot recover metadata that was discarded before storage. Conversely, copying original inline CSS wholesale would preserve fixed pixel layouts and poor dark-theme contrast; the current player intentionally strips inline styles during sanitization.

The existing content strings already support sanitized HTML. **No database schema change or replacement renderer is needed.** A canonical table representation can retain:

- native table/row/cell structure, including actual header tags, spans and source sections;
- a small whitelist of typed presentation metadata such as table/cell alignment, rules/frame and validated source fill colors;
- existing mathematical cell text, prose, image links and `{{field-key}}` placeholders;
- source provenance in the repair evidence, rather than guessing roles from how values look.

The prototype stores this metadata as classes and `data-*` attributes, not arbitrary source CSS. The scoped UI helper resolves validated colors into light/dark fills with readable contrast. Small tables center when the source centers them; genuinely wide tables scroll horizontally without growing the page. Actual `th` roles stay headers; source `td` data stays data. A highlighted first column is not blindly reclassified as semantic headers.

Existing MathML arrays, ordinary Markdown tables with legitimate headers, and authored `.matrix-answer` editors should remain on their current paths unless source comparison shows a specific problem. Source HTML tables used for graph/image layouts need the same structural model, but reconstruction must retain the correct assets and grouping.

## Tested prototype

[presentation.js](presentation.js) and [presentation.css](presentation.css) implement the proposed table contract and scoped display behavior. The prototype uses the actual current player Markdown parser, DOMPurify, MathJax, MathLive/shared field controls, theme and stylesheet. It was tested against **11 real table examples in 66 light/dark and desktop/tablet/phone combinations**, at 1100, 768 and 390px.

Checks passed for:

- unchanged mathematical token sequences;
- exact source cell roles and row/column spans;
- source centering and label shading for the reported example;
- preserved field/control IDs and native blank/dropdown controls;
- readable shaded-cell text contrast, at least **5.46:1** in the tested cases;
- necessary horizontal scrolling for wide and nested tables, with no page overflow or unnecessary vertical scrolling;
- zero MathJax/page errors.

The actual nested lookup example was rebuilt by distributing its **existing math tokens** into source leaf cells in order, verifying each cell's contents and rejecting any leftover tokens. No original mathematical answer was substituted into a problem blank.

Previews:

- [Reported table — light](limits-table-light-1100.png), [dark/phone](limits-table-dark-390.png)
- [Merged direction labels](merged-direction-labels-light-1100.png)
- [Reconstructed nested lookup tables](nested-statistical-tables-light-1100.png)
- [Editable sign chart on a phone](editable-sign-chart-dark-390.png)
- [Wide degree/radian table](wide-degree-radian-table-light-390.png)

## Concrete migration proposal

**2,859 straightforward source-backed table replacements** have been drafted in [proposed-table-replacements.json](proposed-table-replacements.json), covering **2,412 fields on 2,180 entities**. They retain current cell content and restore source presentation/structure. This draft includes 66 non-nested merged-cell cases. Captions requiring independent content reconciliation are excluded from automatic drafting.

The 82 flattened nested-table cases and 18 ambiguous source-layout matches remain a separate review tier. One nested case is already proven by the prototype; graph/image-heavy and conflicting cases should not be guessed from a flat cell string. Drafts are not approved transactions: full-field CAS preparation, native validation and render/grading verification are still required before migration.

The proposed rollout is:

1. Introduce one shared table serialization contract for the historical Python importer, current DOM extractor, tutorial/activity HTML converter and newer browser capture path. Preserve real headers and spans; translate supported styles to typed metadata; flag unsupported layout features instead of silently flattening them.
2. Add the shared, scoped display helper to lessons/quizzes, assignments and activity history. Keep source semantics and grouping while adapting colors and scrolling to the app. Validate meaningful colored math separately as part of deployment; shaded-cell contrast does not alone prove every authored TeX foreground color is readable.
3. Prepare source-backed CAS batches that replace table spans only. Preserve IDs, mathematical values, links, response history and blank keys. Selection-answer table values may change display markup only when grading remains by the same answer ID. Recheck answer ownership and native field invariants at the fresh preflight basis.
4. Validate every final changed field through the actual UI, verify representative editable/wide/nested cases at both themes and narrow widths, commit under stable request keys, read back exact `db_after` values, and rerun the source-aware audit. Do not include unmatched or conflicting layouts merely because they resemble a table type.

## Evidence and limits

- [Database inventory](inventory-summary.json), [source inventory](source-summary.json), [confirmed matches](match-summary.json)
- [Source-bound table comparisons](source-matches.json), [ambiguous layouts](ambiguous-source-tables.json), [unmatched tables](unmatched-tables.json)
- [Prototype verification](prototype-verification.json), [representative cases](prototype-cases.json), [proposed spans](proposed-table-replacements.json), [answer-value safety review](proposal-answer-safety.json)

The source archive covers a substantial range of lessons and table forms, establishing the general failure mechanism. Before claiming a complete database repair, the remaining tables need either their newer capture provenance resolved or an explicit reviewed decision that no repair is required.

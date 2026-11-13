# Imported matrix/vector table census

Follow-up: this candidate list is the historical pre-repair census. The confirmed
repairs have now been published; see [the repair results](../../repairs/2026-11-11-imported-matrix-tables/README.md).

Read-only scan of current EDB math data at basis 14355 on 2026-11-11.
The database contains 78,329 imported questions and
6,124 imported tutorials. No database writes were made.

The search targets tables used to draw mathematical objects: lost bracket edge
cells, shifted answer rows, partially supplied matrices/vectors, and multiple
matrix operands embedded in layout tables. Ordinary labeled data tables remain
separate, even when the data happen to form a matrix.

There are **260 question candidates with Markdown tables**:

| Highest review priority per question | Questions |
| --- | ---: |
| Matches the known broken matrix-grid pattern | 49 |
| Strong layout candidates, including supplied entries and multiple operands | 178 |
| Matrix/vector-related table requiring source or visual review | 33 |

The supplemental HTML sweep brings the combined collection to **534 unique
questions across 49 topics**. At the question level, the disjoint priorities are
91 matching the known pattern, 350 strong candidates, and 93 needing review.
These are candidate counts, not a claim that every table is defective.

The combined collection comprises 727 table blocks. Counts of blocks differ from
counts of questions because a question can contain several tables, and a table
can occur in a prompt, solution, or answer option. Of the 534 questions, 522 are
linked to knowledge-point question pools and 12 are canonical examples.

Open [the question-level CSV](candidate-questions.csv) for a deduplicated review
list, or [the question JSON](candidate-questions.json). Each entry includes the
EDB ID, imported source ID, priority, format, knowledge points, topics and any
associated generator IDs. The `markdown_priority` column matches the Markdown-only
breakdown above; overall priority also considers HTML in the same question.
Indices refer to [table-level candidates](candidates.json),
which retain the actual rows, original table, surrounding text and reasons.
[Topic groups](topics.json) organize the same collection by lesson topic.

The most populated topic groups are:

- Matrix Exponentials: 46 questions.
- Matrix Functions: 33 questions.
- Solving Inhomogeneous Systems of ODEs Using Matrix Methods: 32 questions.
- Solving Systems of ODEs Using Variation of Parameters: 25 questions.
- The Chain Rule for Total Derivatives: 24 questions.
- Singular Value Decomposition of Larger Matrices: 23 questions.
- Newton's Method for Multivariable Functions: 23 questions.
- Solving Inhomogeneous Systems of ODEs: 23 questions.
- The Lotka-Volterra Model With Carrying Capacity: 18 questions.
- Expressing Inhomogeneous ODEs as First-Order Systems: 16 questions.

Examples include `17592186222006` (matrix exponential derivative, Markdown)
and `17592186204583` (matrix gradient with supplied entries, HTML). Original
source HTML for both shows selective cell borders used as matrix brackets;
those bracket borders were lost or became ordinary table borders in the import.
The [source spot checks](source-spot-checks.json) retain their source paths and
cell-border evidence. These spot checks establish representative failures;
they do not constitute individual source verification of every candidate.

[Detector controls](detector-controls.json) verify detection of all 27 known
bad layouts from the preceding lesson repair, exclusion of all 27 repaired
layouts, and exclusion of genuine labeled distance/Markov tables. The current
snapshot also classifies the two originally reported questions as repaired,
canonical matrix layouts rather than outstanding candidates.

Coverage and limits:

- The native export scans current content across prompts, worked solutions,
  answer values/feedback/keys, imported tutorials and multipart contexts.
  Imported ownership is resolved through answer fields, questions and lesson
  links. Only current facts at the captured basis are counted.
- [Every imported table](all-imported-tables.jsonl) is retained, including
  ordinary tables and already-correct matrix controls. The primary collection
  does not silently discard the broader search results.
- [Unlabeled mathematical arrays](weak-array-candidates.json) form a separate
  low-confidence queue of 738 blocks without enough matrix/vector evidence.
  They include genuine sign tables and other intentional arrays.
  [Other mathematical layouts](other-math-layouts.json) retain 163 possible
  fraction/system and similar layouts outside the primary matrix search.
- The detector cannot establish intent from markup alone. Ambiguous candidates
  need comparison with original source or visual inspection before repair.
  Images and flattened prose with no table markup are outside this search.
- This is a snapshot census. Later imports or edits require a fresh export.

The reusable detector is `scripts/audit_imported_matrix_tables.py`. The local
`export.rs` is read-only and pins `TABLE_AUDIT_BASIS`; its build command, log and
captured database status are saved beside the results. The compressed snapshot
retains all scanned table-bearing text and the metadata used to establish
imported ownership. Its integrity is checked in `snapshot-integrity.json`.

To repeat classification on this same captured snapshot:

```sh
.venv/bin/python scripts/audit_imported_matrix_tables.py \
  --snapshot reference/edb-math/audits/2026-11-11-imported-matrix-tables/snapshot.jsonl.gz \
  --output reference/edb-math/audits/2026-11-11-imported-matrix-tables
```

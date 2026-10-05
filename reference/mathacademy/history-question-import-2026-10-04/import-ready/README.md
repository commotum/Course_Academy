# Prepared historical questions

1506 of 1575 questions are prepared; 69 are deferred. The prepared batch was committed at database basis 552.

- `questions.json`: complete content records and answer fields.
- `deferred.json`: excluded records, evidence, and exact reasons.
- `answer-audit.json`: original and prepared answer fields.
- `transaction-draft.edn`: additive content-only draft using stable importer identities.
- `runtime-readiness.json`: exact native grader results for every prepared record.
- `engine-supported-questions.json` and `transaction-engine-supported-draft.edn`: subset accepted by the current grader.
- `asset-map.json` and `assets/`: local copies of referenced images, with hashes.
- `report.json`: counts, checks, and source fingerprints.

Original saved files are unchanged. Existing response fields and dropdown options are preserved. Missing-option numeric or symbolic questions are adapted to entered answers with explicit locations; their original prompts and derivations remain in preparation metadata. Quadrants, parity, yes/no, and three-statement questions use locally authored exhaustive choices, explicitly distinguished from unavailable original MA options. Regression-model, solid-name, and polynomial-classification questions use locally authored category choices. Explicit named outputs, matrix entries, coordinates, and ordered roots have separate fields. Observed difficulty remains the original MA rating, not a new rating of the adapted version.

This is content preparation, not a symbolic-grading implementation. The current engine rejects symbolic math blanks at serving time. The runtime readiness report identifies those records; the existing engine filters them out of practice selection, so they can remain stored with their KP links. Native database matching and a fresh basis-guarded preview are required before any import; the draft assumes these questions remain absent and their saved KP associations remain valid.

## Preview before the import

At database basis 551, all 1506 prepared question IDs were matched (0 already present). Both complete-content and current-engine-supported transactions passed native EDB `with` previews. Every proposed datom is an additive content fact or transaction metadata; there are no learner or engine-policy writes. No import was committed. These previews must be refreshed before a later import.

56 image-answer, reconstruction, or missing-asset questions and 13 interpretation/response-design questions remain outside the drafts. Fully saved diagrams used in otherwise straightforward questions are retained.

The current native grader accepts 801 prepared records; 705 need broader mathematical grading support (symbolic expressions, radicals, intervals, or units). The supported subset has its own content file and transaction; the current engine excludes unsupported blanks from practice even when their KP membership is stored.

### Interpretation cases left for later

- `q-69464`: Identifying Equal Vectors
- `q-112080`: Interpreting the Derivative of a Function in a Given Context
- `q-112088`: Interpreting the Derivative of a Function in a Given Context
- `q-112093`: Interpreting the Derivative of a Function in a Given Context
- `q-141138`: Identifying Multiplicity of a Root Given a Graph
- `q-141135`: Identifying Multiplicity of a Root Given a Graph
- `q-124052`: Determining Whether a Piecewise Infinite Series Converges or Diverges
- `q-112064`: Interpreting the Derivative of a Function
- `q-110741`: Interpreting the Derivative of a Function
- `q-48601`: Interpreting the Derivative of a Function in a Given Context
- `q-48687`: Interpreting the Derivative of a Function in a Given Context
- `q-120789`: Finding the Coordinates of the Points of Intersection of a Trigonometric Curve and a Horizontal Line
- `q-123335`: Determining Convergence Behavior of Geometric Sequences Written Recursively

## Database import

All 1506 prepared questions were committed at basis 551 → 552. Their prompts, solutions, difficulties, answer fields, and KP memberships were verified. Learner progress and engine configuration fingerprints are unchanged, and reimport produces no additions. 69 deferred questions remain outside this import.

The existing engine filters questions that fail its grader validation from KP selection and fresh-question supply checks. Storing the 705 unsupported math blanks with their KP links does not make them available for practice. No engine change or fabricated grading result was needed.

Durable intent, receipt, before/after reads, and verification are in `database-import/`.

# Identifying Singular Matrices (17592186059848)

Numeric 3×3 determinant calculation followed by a three-statement singularity classification. All three levels are implemented. Hard is an authored density/fraction/repeated-radical policy anchored to the observed moderate examples. No other matrix skill, database transaction, or plot is included.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059848.py --difficulty all --seed 13 --count 2
.venv/bin/python generate/scratch/17592186059848/validate.py
.venv/bin/python generate/scratch/17592186059848/write_review.py
```

The public functions are generate_easy, generate_moderate, generate_hard, and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Source replay uses source-cases.json through this same interface. Explicit invalid input fails. CLI supports --difficulty easy|moderate|hard|all, --seed, --count, --format markdown|json, --template and --profile.

source.json preserves math basis 1356 and lineage. recipes.json contains the extracted structure; build_evidence.py reproduces this read-only extraction from the fixed captures. review.md displays originals, parameterized replays, two generated variants per source field, and two authored hard examples; review.json holds the records. validation.json separates source banks/designations, independently parsed exact math, and actual native grading. engine-input.json and engine-report.json are memory-only native grader fixtures and results.

q-128490 has two identical raw banks at a duplicate field key and one missing legacy correct reference. The captured widget proves one five-choice assessment; normal generation emits one field. Both raw banks are replayed, but the missing original correct designation is reported as inferred, not matched. Arithmetic typography and malformed source bold are normalized and documented separately from complete bank matches.

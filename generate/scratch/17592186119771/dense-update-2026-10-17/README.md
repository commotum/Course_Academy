# Triangular matrix generator v3

Run current checks from the repository root:

```sh
.venv/bin/python generate/scratch/17592186119771/dense-update-2026-10-17/validate.py
```

Normal questions use 2×2 matrices for easy, 3×3 for moderate, and 4×4 for hard. Every diagonal entry is nonzero. A nondiagonal upper or lower triangular matrix has at least 1, 2, or 3 nonzero off-diagonal entries respectively. Every level supports upper, lower, and diagonal examples; difficulty no longer reveals the answer family. All normal matrices render with display `bmatrix` and growing brackets.

Independent draws weight lower/upper/diagonal 40/40/20. Unique batches choose structures before values, keep at most one diagonal contrast, and balance upper/lower as supply permits. Exclusions apply before that choice. A depleted two-question supply containing one triangular and one diagonal matrix remains usable. Exact proportions cannot persist after structural deduplication: there is one diagonal structure per size. The finite catalogs contain **3 easy, 9 moderate, and 85 hard** cases. Asking for more than the remaining capacity raises an explicit shortage; new numbers, signs, labels, layouts, or diagonal unit positions do not count as new tasks.

Raw source profiles preserve all ten frozen originals exactly after identity normalization, including legacy formatting, sparse matrices, ratings, missing keys, and the duplicate answer field. They require the exact original matrix, label, and layout and are evidence-only. Normal source profiles retain source size and family while applying current density/difficulty guards and display normalization. Sparse original parameters cannot bypass the normal policy through a source profile.

The current evidence covers the full structural catalog, 3,000 independent draws, every finite batch size, exclusions and depleted supplies, the rejected center-only matrix and other invalid inputs, raw fidelity, and native grading. Original v2 evidence in the parent directory remains historical; the parent `validate.py` main has obsolete v2 policy assertions. The current `capabilities.json` points here.

Native evidence is reused by this validator only if the entire serialized fixture set is unchanged. Renderer inspection and a second independent grader run are recorded separately by the review agent in the repair evidence.

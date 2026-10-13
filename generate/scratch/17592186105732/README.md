# Given-vector area generator

Run `.venv/bin/python generate/scratch/17592186105732/validate.py` from the repository root. Preview: `.venv/bin/python generate/scratch/17592186105732.py --difficulty all --seed 42 --count 2 --format markdown`.

The script exposes `generate_easy`, `generate_moderate`, `generate_hard` and the parameterized `generate(...)` API. `source-cases.json` contains every original practice case and its complete profile. The outer record uses plain knowledge-point keys; inner schema keys retain colons, UUIDs, enum strings and correct lookup refs. JSON is local review data.

Easy and moderate preserve given-vector parallelogram/triangle source tasks. Hard is authored dense signed primitive given-vector triangle arithmetic, bounded by existing determinant and magnitude prerequisites. Source scalar distractor patterns are explicitly limited to uniform scaling rays; defaults use a separate complete authored omission bank. q-20003 lacks a source key, difficulty and worked solution; its unique sqrt(3) key is independently inferred, and easy/full formal solution are authored. No missing designation is counted as a fidelity match. No database writes or shared files are changed.

Read `classification.md`, `template-extraction.md`, `plot-extraction.md`, `review.md`, `validation.json` and the native `engine-report.json`. Source fidelity is distinct from mathematical correctness and actual learner grading. Every math stage is read from the displayed prompt/solution, checked against independent hand-coordinate and Gram-determinant mathematics. Source solution sequence is checked byte-for-byte. The native grader also checks unreduced equivalent blank norms. Plot rating: none.

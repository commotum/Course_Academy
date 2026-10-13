# Cartesian supplied-potential FTLI generator

Local review artifacts only, immutable math basis 1356. No database writes or registrations.

Run `.venv/bin/python generate/scratch/17592186133890/validate.py` for independent checks of actual displayed prompts, parametrizations, endpoints, every arithmetic row, complete banks, identity and native radio grading. Cached read-only lark 1.2.2 supplies the LaTeX parser; it is not installed into or written to the environment.

Preview: `.venv/bin/python generate/scratch/17592186133890.py --difficulty all --seed 17 --count 2 --format json`.

API: generate_easy/generate_moderate/generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Explicit parameters reject invalid workloads and colliding whole banks.

Observed templates are named by their q-ID, with profile observed and parameter scale. Their complete banks use homogeneous coefficient replay; their error interpretations remain underidentified. Normal defaults authored_direct/easy, authored_inverse/moderate, authored_mixed/hard use authored_operations. The authored hard design and q-39749 minimal source repair are explained in classification.md and template-extraction.md. Every source and two coefficient variants, plus two examples per authored level, appear in review.md/review.json.

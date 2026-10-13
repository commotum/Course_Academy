# Parametric arc-length generator

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186092377/validate.py
.venv/bin/python generate/scratch/17592186092377.py --difficulty all --seed 23 --count 2 --format json
```

Local review only; no database writes or engine edits. Source math basis 1356. All 18 source questions, seven full radios and eleven blank fields are covered. Default generators exist at easy/moderate/hard, preserve full source solution prose/stages, and vary familiar-domain interval endpoints and positive uniform coordinate scales. Every source case uses explicit profile="observed". Scalar radio banks require explicit endpoint parameters because their error intent is unknown. Default blank prompts say Give an exact answer instead of Do not round; this documented presentation repair avoids the actual engine’s unintended round-substring normalize-only path while preserving source wording for evidence replay. `validation.json` separates bank fidelity, displayed mathematics, grading, formatting repairs and scope. The engine report uses the actual `learning::grade_field` entry point. Plot QA is documented in `plot-extraction.md`.

The exponential question preserves the source partial blank: field value is e^(2u)−1; c√5/2 is supplied outside the fragment. Original equivalent-blank grading failures are retained in native-equivalence.json; default exact-answer wording must accept meaningful equivalents. q-20907 receives a single documented parenthesis repair. Source assets remain read-only; generated assets are local.

Final checks: 18/18 complete source banks, 46/46 options, 28/28 distractors, 18/18 correct designations; 90 primary canonical accepts / 250 wrong rejections, plus six CLI accepts / fourteen wrong rejections. All 22 default and 22 boundary equivalent-blank probes pass; ten original Do not round prompts reject equivalent entries and are retained as capability failures. Available default inventory: 960 easy, 192 moderate, 95 hard assessed instances. Source-author scalar error intent remains unresolved in explicit observed profiles.

# Root-multiplicity graph generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186129253/validate.py
.venv/bin/python generate/scratch/17592186129253.py --difficulty all --seed 2 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129253.py --difficulty easy --profile raw-q-140411 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard convenience functions. Parameters are `roots`, `multiplicities` (representative1/2/3), `orientation`±1, `target` index. Explicit level guards are described in template-extraction.md. No database writes, registry changes or commits.

Seven original full banks35/35 options replay, five present solutions and five present correct designations. Raw profiles preserve the two unrated sources’ missing difficulty, solution and key. Completed profiles infer those two classifications from the original plots and explicitly author their fields/level/solution. Raw records are evidence-only. Moderate and hard are authored context/coordinate-reading extensions of one categorical target; exact higher exponents and complete polynomial recovery are outside scope. Review.json/Markdown show originals, changed original profiles, and at least three variants per level. Validation.json separates source fidelity, inferred completion, independent mathematics/raster checks and real native grader outcomes. Parent independent QA remains required.
